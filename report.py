import os
import pdfkit
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# path_wkhtmltopdf = 'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


def generate_report(pocetni_datum, krajnji_datum, administracija_engine):
    # Load data
    with administracija_engine.connect() as connection:
        df_usluga = pd.read_sql(f"SELECT * FROM Promet WHERE Datum BETWEEN '{pocetni_datum}' AND '{krajnji_datum}'", con=connection)
        df_gorivo = pd.read_sql(f"SELECT * FROM Gorivo WHERE Datum BETWEEN '{pocetni_datum}' AND '{krajnji_datum}'", con=connection)
        df_servis = pd.read_sql(f"SELECT * FROM `Servis-Gume-Registracija` WHERE Datum BETWEEN '{pocetni_datum}' AND '{krajnji_datum}'", con=connection)
        df_kazne = pd.read_sql(f"SELECT * FROM Kazne WHERE Datum BETWEEN '{pocetni_datum}' AND '{krajnji_datum}'", con=connection)
        df_trosak = pd.read_sql(f"SELECT * FROM Trošak WHERE Datum BETWEEN '{pocetni_datum}' AND '{krajnji_datum}'", con=connection)


    # Prepare data for the Jinja2 template
    template_data = {
        'current_date': datetime.today().strftime("%d.%m.%Y"),
        'pocetni_datum': str(datetime.strftime(pocetni_datum, '%d.%m.%Y')),
        'krajnji_datum': str(datetime.strftime(krajnji_datum, '%d.%m.%Y')),
        'promet_gotovina': "{:.2f}".format(df_usluga['Iznos gotovina (KM)'].sum()),
        'promet_ziralno': "{:.2f}".format(df_usluga['Iznos žiralno (KM)'].sum()),
        'ukupno_promet': "{:.2f}".format(df_usluga['Iznos gotovina (KM)'].sum() + df_usluga['Iznos žiralno (KM)'].sum()),
        'nenaplaceno': "{:.2f}".format(df_usluga[df_usluga['Plaćeno'] == 'NE']['Iznos gotovina (KM)'].sum() + df_usluga[df_usluga['Plaćeno'] == 'NE']['Iznos žiralno (KM)'].sum()),
        'broj_gratis': len(df_usluga[df_usluga['Plaćeno'] == 'GRATIS']),
        'gratis_rows': df_usluga[df_usluga['Plaćeno'] == 'GRATIS'].to_dict(orient='records'),

        # Data for GORIVO DataFrame
        'gorivo_predjena_kilometraza': "{:.2f}".format(df_usluga['Kilometraža'].sum()),
        'gorivo_prosjecna_cijena': "{:.2f}".format(df_gorivo['Cijena goriva (KM)'].mean()),
        'gorivo_nasuta_kolicina': "{:.2f}".format(df_gorivo['Nasuta količina (l)'].sum()),
        'gorivo_ukupno_placeno': "{:.2f}".format(df_gorivo['Iznos (KM)'].sum()),

        # Data for KAZNE DataFrame
        'kazne_broj_prekrsaja': len(df_kazne),
        'kazne_ukupan_trosak': "{:.2f}".format(df_kazne['Iznos (KM)'].sum()),
        'kazne_rows': df_kazne.to_dict(orient='records'),

        # Data for SERVIS DataFrame
        'servis_broj_servisa': len(df_servis),
        'servis_trosak_servisa': "{:.2f}".format(df_servis[df_servis["Opis"] == "Servis"]['Iznos (KM)'].sum()),
        'servis_trosak_gume': "{:.2f}".format(df_servis[df_servis["Opis"] == "Gume"]['Iznos (KM)'].sum()),
        'servis_trosak_registracija': "{:.2f}".format(df_servis[df_servis["Opis"] == "Registracija"]['Iznos (KM)'].sum()),
        'servis_rows': df_servis.to_dict(orient='records'),

        # Data for TROSKOVI DataFrame
        'trosak_ukupan_iznos': round(df_trosak['Iznos (KM)'].sum(), 2),
        'trosak_rows': df_trosak.to_dict(orient='records')
    }

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')

    # Render the template with data
    rendered_html = template.render(template_data)

    html_filename = f'Izvještaj_{pocetni_datum}-{krajnji_datum}.html'
    # Save the report to a file (or send it as an email, etc.)
    with open(html_filename, 'w', encoding='utf-8') as report_file:
        report_file.write(rendered_html)
    
    # Create a PDF from the rendered HTML
    pdfkit.from_file(html_filename, f'Izvještaj_{pocetni_datum}-{krajnji_datum}.pdf')#, configuration=config)

    # Check if the file exists before attempting to delete
    if os.path.exists(html_filename):
        os.remove(html_filename)
    else:
        pass