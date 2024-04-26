import os
import pdfkit
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
#path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    
def generate_report(pocetni_datum, krajnji_datum, administracija_engine):

    if pocetni_datum > krajnji_datum:
        return "datum greska"
    else:
        # Load data
        with administracija_engine.connect() as connection:
            df_usluga = pd.read_sql(f"SELECT * FROM Promet WHERE Datum BETWEEN '{pocetni_datum}' AND '{krajnji_datum}'", con=connection)
            df_gorivo = pd.read_sql(f"SELECT * FROM Gorivo WHERE Datum BETWEEN '{pocetni_datum}' AND '{krajnji_datum}'", con=connection)
            df_servis = pd.read_sql(f"SELECT * FROM `Servis-Gume-Registracija` WHERE Datum BETWEEN '{pocetni_datum}' AND '{krajnji_datum}'", con=connection)
            df_kazne = pd.read_sql(f"SELECT * FROM Kazne WHERE Datum BETWEEN '{pocetni_datum}' AND '{krajnji_datum}'", con=connection)
            df_trosak = pd.read_sql(f"SELECT * FROM Trošak WHERE Datum BETWEEN '{pocetni_datum}' AND '{krajnji_datum}'", con=connection)
            
        dfs = [df_usluga, df_gorivo, df_servis, df_kazne, df_trosak]
        l = []
        for df in dfs:
            if df.empty:
                l.append("empty")
            else:
                l.append("not empty")
        if set(l) == {"empty"}:
            return "empty"
        
        df_usluga['Datum'] = pd.to_datetime(df_usluga['Datum'], format="%d.%m.%Y")
        df_gorivo['Datum'] = pd.to_datetime(df_gorivo['Datum'], format="%d.%m.%Y")
        df_servis['Datum'] = pd.to_datetime(df_servis['Datum'], format="%d.%m.%Y")
        df_kazne['Datum'] = pd.to_datetime(df_kazne['Datum'], format="%d.%m.%Y")
        df_trosak['Datum'] = pd.to_datetime(df_trosak['Datum'], format="%d.%m.%Y")

        df_usluga['Datum'] = df_usluga['Datum'].dt.strftime("%d.%m.%Y")
        df_gorivo['Datum'] = df_gorivo['Datum'].dt.strftime("%d.%m.%Y")
        df_servis['Datum'] = df_servis['Datum'].dt.strftime("%d.%m.%Y")
        df_kazne['Datum'] = df_kazne['Datum'].dt.strftime("%d.%m.%Y")
        df_trosak['Datum'] = df_trosak['Datum'].dt.strftime("%d.%m.%Y")
            
        if not (df_servis.empty and df_gorivo.empty):
            combined_gorivo_servis = pd.concat([df_gorivo, df_servis]).reset_index(drop=True)
            km_sat_stanje = int(combined_gorivo_servis["Kilometraža na satu (km)"].max())
        else:
            km_sat_stanje = "Nema podataka"
        
        pocetni_datum_format = str(pocetni_datum.strftime("%d-%m-%Y"))
        krajnji_datum_format = str(krajnji_datum.strftime("%d-%m-%Y"))
        
        # Prepare data for the Jinja2 template
        template_data = {
            'current_date': datetime.today().strftime("%d.%m.%Y"),
            'pocetni_datum': str(datetime.strftime(pocetni_datum, '%d.%m.%Y')),
            'krajnji_datum': str(datetime.strftime(krajnji_datum, '%d.%m.%Y')),
            'promet_gotovina': "{:.2f}".format(df_usluga['Iznos gotovina (KM)'].sum()) if not df_usluga.empty else "Nema podataka",
            'promet_ziralno': "{:.2f}".format(df_usluga['Iznos žiralno (KM)'].sum()) if not df_usluga.empty else "Nema podataka",
            'ukupno_promet': "{:.2f}".format(df_usluga['Iznos gotovina (KM)'].sum() + df_usluga['Iznos žiralno (KM)'].sum()) if not df_usluga.empty else "Nema podataka",
            'nenaplaceno': "{:.2f}".format(df_usluga[df_usluga['Plaćeno'] == 'NE']['Iznos gotovina (KM)'].sum() + df_usluga[df_usluga['Plaćeno'] == 'NE']['Iznos žiralno (KM)'].sum()) \
                           if not df_usluga.empty else "Nema podataka",
            'broj_gratis': len(df_usluga[df_usluga['Plaćeno'] == 'GRATIS']) if not df_usluga.empty else 0,
            'gratis_rows': df_usluga[df_usluga['Plaćeno'] == 'GRATIS'].to_dict(orient='records'),
            'predjeno_kilometara': "{:.2f}".format(df_usluga['Kilometraža pređena (km)'].sum()) if not df_usluga.empty else "Nema podataka",
            'prosjecna_cijena_po_gazenom_km': "{:.2f}".format(df_usluga['Cijena po gaženom kilometru (KM/km)'].mean()) if not df_usluga.empty else "Nema podataka",

            # Data for GORIVO DataFrame
            'gorivo_predjena_kilometraza': "{:.2f}".format(df_usluga['Kilometraža pređena (km)'].sum()) if not df_usluga.empty else "Nema podataka",
            'gorivo_prosjecna_cijena': "{:.2f}".format(df_gorivo['Cijena goriva (KM/l)'].mean()) if not df_gorivo.empty else "Nema podataka",
            'gorivo_nasuta_kolicina': "{:.2f}".format(df_gorivo['Nasuta količina (l)'].sum()) if not df_gorivo.empty else "Nema podataka",
            'gorivo_ukupno_placeno': "{:.2f}".format(df_gorivo['Iznos (KM)'].sum()) if not df_gorivo.empty else "Nema podataka",
            'gorivo_potrosnja': "{:.2f}".format((df_gorivo['Nasuta količina (l)'].sum()/df_usluga['Kilometraža pređena (km)'].sum())*100) if not df_usluga.empty else "Nema podataka",
            'gorivo_prosjecna_cijena_potrosnje': "{:.2f}".format(df_gorivo['Cijena goriva (KM/l)'].mean()*(df_gorivo['Nasuta količina (l)'].sum()/df_usluga['Kilometraža pređena (km)'].sum()*100)) \
                                                 if not df_usluga.empty else "Nema podataka",

            # Data for KAZNE DataFrame
            'kazne_broj_prekrsaja': len(df_kazne) if not df_kazne.empty else 0,
            'kazne_ukupan_trosak': "{:.2f}".format(df_kazne['Iznos (KM)'].sum()) if not df_kazne.empty else "Nema podataka",
            'kazne_rows': df_kazne.to_dict(orient='records'),

            # Data for SERVIS DataFrame
            'servis_broj_servisa': len(df_servis) if not df_servis.empty else 0,
            'servis_trosak_servisa': "{:.2f}".format(df_servis[df_servis["Opis"] == "Servis"]['Iznos (KM)'].sum()) if not df_servis.empty else "Nema podataka",
            'servis_trosak_gume': "{:.2f}".format(df_servis[df_servis["Opis"] == "Gume"]['Iznos (KM)'].sum()) if not df_servis.empty else "Nema podataka",
            'servis_trosak_registracija': "{:.2f}".format(df_servis[df_servis["Opis"] == "Registracija"]['Iznos (KM)'].sum()) if not df_servis.empty else "Nema podataka",
            'servis_rows': df_servis.to_dict(orient='records'),

            # Data for TROSKOVI DataFrame
            'trosak_ukupan_iznos': round(df_trosak['Iznos (KM)'].sum(), 2) if not df_trosak.empty else 0,
            'trosak_rows': df_trosak.to_dict(orient='records'),
            
            # Ostalo
            'stanje_na_satu': km_sat_stanje,
            'gorivo_potroseno_privatno': abs((df_gorivo["Kilometraža na satu (km)"].values[-1] - df_gorivo["Kilometraža na satu (km)"].values[0]) - df_usluga['Kilometraža pređena (km)'].sum()) \
                                         if not df_gorivo.empty else "Nema podataka",
        }

        env = Environment(loader=FileSystemLoader(f'{parent_dir}/templates'))
        template = env.get_template(f'{parent_dir}/templates/report_template.html')

        # Render the template with data
        rendered_html = template.render(template_data)

        html_filename = f'{parent_dir}/templates/Izvještaj_{pocetni_datum_format}-{krajnji_datum_format}.html'
        # Save the report to a file (or send it as an email, etc.)
        with open(html_filename, 'w', encoding='utf-8') as report_file:
            report_file.write(rendered_html)
        
        pdf_filename = f'{parent_dir}/reports/Izvještaj_{pocetni_datum_format}-{krajnji_datum_format}.pdf'
        options = {
            "enable-local-file-access": True,
            "encoding": "UTF-8"
        }
        # Create a PDF from the rendered HTML
        pdfkit.from_file(html_filename, f'{parent_dir}/reports/{pdf_filename}', configuration=config, options=options, verbose=True)
        # pdfkit.from_file(html_filename, pdf_filename, configuration=config, options=options, verbose=True)

        # Check if the file exists before attempting to delete
        if os.path.exists(html_filename):
            os.remove(html_filename)
        else:
            pass
        
        return pdf_filename

def delete_pdf_after_download(pdf_filename):

    # Check if the file exists before attempting to delete
    if os.path.exists(f'{parent_dir}/reports/{pdf_filename}'):
        os.remove(f'{parent_dir}/reports/{pdf_filename}')
    else:
        pass
