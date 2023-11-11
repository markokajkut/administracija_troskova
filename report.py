

from jinja2 import Environment, FileSystemLoader
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from weasyprint import HTML
#import wget
from requests import request
# import matplotlib.pyplot as plt
# import seaborn as sns


ch = "\u010D".encode('utf-8')
print(ch)
#import lorem

from fpdf import FPDF
from datetime import datetime

# cell height
ch = 8

#font_file_url = "http://dejavu.svn.sourceforge.net/viewvc/dejavu/trunk/dejavu-fonts/langcover.txt"
#filename = wget.download(font_file_url, "./font")

class PDF(FPDF):
    def __init__(self):
        super().__init__()
    def header(self):
        #self.add_font()
        self.set_font('Arial', '', 12)
        self.cell(0, 8, 'Futuris & SB, Sinisa Borjanic', 0, 1, 'C')
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 12)
        #self.cell(0, 8, f'Page {self.page_no()}', 0, 0, 'C')

# # Load or prepare pandas DataFrame
# df = pd.DataFrame({'feature 1' : ['cat 1', 'cat 2', 'cat 3', 'cat 4'], 'feature 2' : [400, 300, 200, 100]})

# # Save figures to use in the PDF
# fig, ax = plt.subplots(1,1, figsize = (6, 4))
# sns.barplot(data =  df, x = 'feature 1', y = 'feature 2')
# plt.title("Chart")
# plt.savefig('./example_chart.png', transparent=False,  facecolor='white', bbox_inches="tight")
# plt.close()

# def generate_report(pocetni_datum, krajnji_datum, administracija_engine):
    
#     # Load data
#     with administracija_engine.connect() as connection:
        
#         df_usluga = pd.read_sql(f'SELECT * FROM Promet WHERE Datum BETWEEN {pocetni_datum} AND {krajnji_datum}', connection)
#         df_gorivo = pd.read_sql(f'SELECT * FROM Gorivo WHERE Datum BETWEEN {pocetni_datum} AND {krajnji_datum}', connection)
#         df_servis = pd.read_sql(f'SELECT * FROM Servis WHERE Datum BETWEEN {pocetni_datum} AND {krajnji_datum}', connection)
#         df_kazne = pd.read_sql(f'SELECT * FROM Kazne WHERE Datum BETWEEN {pocetni_datum} AND {krajnji_datum}', connection)
#         df_trosak = pd.read_sql(f'SELECT * FROM Trošak WHERE Datum BETWEEN {pocetni_datum} AND {krajnji_datum}', connection)
    
#     # Generate PDF
#     pdf = PDF()
#     #DejaVuSansCondensed.ttf
#     #pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)

#     #pdf.add_font('DejaVuSans', fname='./DejaVuSans.ttf', uni=True)
#     #pdf.add_font('DejaVuSans', '', os.path.join(request.folder,'static','fonts/DejaVuSans.ttf'), uni=True)
#     #pdf.set_encoding('UTF-8')
#     pdf.add_page()
#     pdf.set_font('Arial', 'B', 24)
#     pdf.cell(w=0, h=20, txt="Izvjestaj", ln=1)

#     pdf.set_font('Arial', '', 16)
#     pdf.cell(w=30, h=ch, txt="Datum: ", ln=0)
#     pdf.cell(w=30, h=ch, txt=datetime.today().strftime("%d.%m.%Y"), ln=1)
#     pdf.cell(w=30, h=ch, txt="Za period: ", ln=0)
#     pdf.cell(w=30, h=ch, txt=f"{str(datetime.strftime(pocetni_datum, '%d.%m.%Y'))} - {str(datetime.strftime(krajnji_datum, '%d.%m.%Y'))}", ln=1)

#     pdf.ln(ch)
#     pdf.set_font('Arial', 'B', 20)
#     pdf.cell(w=30, h=ch, txt="PROMET", ln=0)
#     pdf.set_font('Arial', '', 16)
#     pdf.ln(ch)
#     pdf.cell(w=75, h=ch, txt="Promet gotovinski: ", ln=0)
#     pdf.cell(w=75, h=ch, txt=f"{df_usluga['Iznos gotovina (KM)'].sum()} KM", ln=1)
#     pdf.cell(w=75, h=ch, txt=u"Promet ziralno: ", ln=0)
#     pdf.cell(w=75, h=ch, txt=f"{df_usluga['Iznos žiralno (KM)'].sum()} KM", ln=1)
#     pdf.cell(w=75, h=ch, txt="Ukupno promet: ", ln=0)
#     pdf.cell(w=75, h=ch, txt=f"{df_usluga['Iznos gotovina (KM)'].sum()+df_usluga['Iznos žiralno (KM)'].sum()} KM", ln=1)
#     pdf.cell(w=75, h=ch, txt="Od toga nenaplaceno: ", ln=0)
#     pdf.cell(w=75, h=ch, txt=f"{df_usluga[df_usluga['Plaćeno']=='NE']['Iznos gotovina (KM)'].sum()+df_usluga[df_usluga['Plaćeno']=='NE']['Iznos žiralno (KM)'].sum()} KM", ln=1)
#     pdf.cell(w=75, h=ch, txt="Broj gratis/pro-bono usluga: ", ln=0)
#     pdf.cell(w=75, h=ch, txt=f"{len(df_usluga[df_usluga['Plaćeno']=='GRATIS'])}", ln=1)
#     pdf.ln(ch)
#     print(len(df_usluga[df_usluga['Plaćeno']=='GRATIS']))
#     if len(df_usluga[df_usluga['Plaćeno']=='GRATIS']) > 0:
#         # Table Header
#         pdf.set_font('Arial', 'B', 16)
#         pdf.cell(40, ch, 'Datum', 1, 0, 'C')
#         pdf.cell(40, ch, 'Naziv(ime) klijenta', 1, 1, 'C')
#         pdf.cell(40, ch, 'Kilometraza', 1, 2, 'C')
#         pdf.cell(40, ch, 'Startno mjesto', 1, 3, 'C')
#         pdf.cell(40, ch, 'Ciljno mjesto', 1, 4, 'C')
#         pdf.cell(40, ch, 'Operativni trosak', 1, 5, 'C')
#         pdf.cell(40, ch, 'Komentar/Napomena', 1, 6, 'C')
#         # Table contents
#         pdf.set_font('Arial', '', 16)
#         for i in range(0, len(df_usluga[df_usluga['Plaćeno']=='GRATIS'])):
#             pdf.cell(40, ch, df_usluga[df_usluga['Plaćeno']=='GRATIS']['Datum'].iloc[i].astype(str), 1, 0, 'C')
#             pdf.cell(40, ch, df_usluga[df_usluga['Plaćeno']=='GRATIS']['Naziv(ime) klijenta'].iloc[i], 1, 1, 'C')
#             pdf.cell(40, ch, f"{df_usluga[df_usluga['Plaćeno']=='GRATIS']['Kilometraža'].iloc[i]} km", 1, 2, 'C')
#             pdf.cell(40, ch, df_usluga[df_usluga['Plaćeno']=='GRATIS']['Startno mjesto'].iloc[i], 1, 3, 'C')
#             pdf.cell(40, ch, df_usluga[df_usluga['Plaćeno']=='GRATIS']['Ciljno mjesto'].iloc[i], 1, 4, 'C')
#             pdf.cell(40, ch, f"{df_usluga[df_usluga['Plaćeno']=='GRATIS']['Operativni trošak (KM)'].iloc[i]} KM", 1, 5, 'C')
#             pdf.cell(40, ch, df_usluga[df_usluga['Plaćeno']=='GRATIS']['Komentar/Napomena'].iloc[i], 1, 6, 'C')
#         pdf.ln(ch)

#     pdf.set_font('Arial', 'B', 20)
#     pdf.cell(w=30, h=ch, txt="KILOMETRAZA", ln=0)
#     pdf.set_font('Arial', '', 16)
#     pdf.ln(ch)

#     pdf.set_font('Arial', 'B', 20)
#     pdf.cell(w=30, h=ch, txt="GORIVO", ln=0)
#     pdf.set_font('Arial', '', 16)
#     pdf.ln(ch)
#     pdf.cell(w=30, h=ch, txt="Predjena kilometraza za odabrani period: ", ln=0)
#     pdf.cell(w=30, h=ch, txt=f"{df_usluga['Kilometraža'].sum()} km", ln=1)
#     pdf.cell(w=30, h=ch, txt="Po prosjecnoj cijeni: ", ln=0)
#     pdf.cell(w=30, h=ch, txt=f"{df_gorivo['Cijena goriva (KM)'].mean()} KM/l", ln=1)
#     pdf.cell(w=30, h=ch, txt="Nasuta kolicina: ", ln=0)
#     pdf.cell(w=30, h=ch, txt=f"{df_gorivo['Nasuta količina (l)'].sum()} l", ln=1)
#     pdf.cell(w=30, h=ch, txt="Ukupno placeno: ", ln=0)
#     pdf.cell(w=30, h=ch, txt=f"{df_gorivo['Iznos (KM)'].sum()} KM", ln=1)
#     pdf.ln(ch)

#     pdf.set_font('Arial', 'B', 20)
#     pdf.cell(w=30, h=ch, txt="KAZNE", ln=0)
#     pdf.set_font('Arial', '', 16)
#     pdf.ln(ch)
#     pdf.cell(w=30, h=ch, txt="Broj napravljenih prekrsaja: ", ln=0)
#     pdf.cell(w=30, h=ch, txt=f"{len(df_kazne)}", ln=1)
#     pdf.cell(w=30, h=ch, txt="Ukupan trosak: ", ln=0)
#     pdf.cell(w=30, h=ch, txt=f"{df_kazne['Iznos (KM)'].sum()}", ln=1)
#     pdf.ln(ch)
#     if len(df_kazne) > 0:
#         # Table Header
#         pdf.set_font('Arial', 'B', 16)
#         pdf.cell(40, ch, 'Datum', 1, 0, 'C')
#         pdf.cell(40, ch, 'Prekrsaj', 1, 1, 'C')
#         pdf.cell(40, ch, 'Iznos', 1, 2, 'C')
#         pdf.cell(40, ch, 'Komentar/Napomena', 1, 3, 'C')
#         # Table contents
#         pdf.set_font('Arial', '', 16)
#         for i in range(0, len(df_kazne)):
#             pdf.cell(40, ch, df_kazne['Datum'].iloc[i].astype(str), 1, 0, 'C')   
#             pdf.cell(40, ch, df_kazne['Prekršaj'].iloc[i], 1, 1, 'C')
#             pdf.cell(40, ch, f"{df_kazne['Iznos (KM)'].iloc[i]} KM", 1, 2, 'C')   
#             pdf.cell(40, ch, df_kazne['Komentar/Napomena'].iloc[i], 1, 3, 'C')
#         pdf.ln(ch)

#     pdf.set_font('Arial', 'B', 20)
#     pdf.cell(w=30, h=ch, txt="SERVIS", ln=0)
#     pdf.set_font('Arial', '', 16)
#     pdf.ln(ch)
#     pdf.cell(w=30, h=ch, txt="Broj napravljenih servisa: ", ln=0)
#     pdf.cell(w=30, h=ch, txt=f"{len(df_servis)}", ln=1)
#     pdf.ln(ch)
#     if len(df_servis) > 0:
#         # Table Header
#         pdf.set_font('Arial', 'B', 16)
#         pdf.cell(40, ch, 'Datum', 1, 0, 'C')
#         pdf.cell(40, ch, 'Opis', 1, 1, 'C')
#         pdf.cell(40, ch, 'Iznos', 1, 2, 'C')
#         pdf.cell(40, ch, 'Komentar/Napomena', 1, 3, 'C')
#         # Table contents
#         pdf.set_font('Arial', '', 16)
#         for i in range(0, len(df_servis)):
#             pdf.cell(40, ch, df_servis['Datum'].iloc[i].astype(str), 1, 0, 'C')   
#             pdf.cell(40, ch, df_servis['Opis'].iloc[i], 1, 1, 'C')
#             pdf.cell(40, ch, f"{df_servis['Iznos (KM)'].iloc[i]} KM", 1, 2, 'C')   
#             pdf.cell(40, ch, df_servis['Komentar/Napomena'].iloc[i], 1, 3, 'C')
#         pdf.ln(ch)

#     pdf.set_font('Arial', 'B', 20)
#     pdf.cell(w=30, h=ch, txt="TROSKOVI", ln=0)
#     pdf.set_font('Arial', '', 16)
#     pdf.ln(ch)
#     pdf.cell(w=30, h=ch, txt="Iznos troskova za odabrani period: ", ln=0)
#     pdf.cell(w=30, h=ch, txt=f"{df_trosak['Iznos (KM)'].sum()} KM", ln=1)
#     pdf.ln(ch)
#     if len(df_trosak) > 0:
#         # Table Header
#         pdf.set_font('Arial', 'B', 16)
#         pdf.cell(40, ch, 'Datum', 1, 0, 'C')
#         pdf.cell(40, ch, 'Opis', 1, 1, 'C')
#         pdf.cell(40, ch, 'Iznos (KM)', 1, 2, 'C')
#         pdf.cell(40, ch, 'Komentar/Napomena', 1, 3, 'C')
#         # Table contents
#         pdf.set_font('Arial', '', 16)
#         for i in range(0, len(df_trosak)):
#             pdf.cell(40, ch, df_trosak['Datum'].iloc[i].astype(str), 1, 0, 'C')   
#             pdf.cell(40, ch, df_servis['Opis'].iloc[i], 1, 1, 'C')
#             pdf.cell(40, ch, f"{df_servis['Iznos (KM)'].iloc[i]} KM", 1, 2, 'C')   
#             pdf.cell(40, ch, df_servis['Komentar/Napomena'].iloc[i], 1, 3, 'C')
#         pdf.ln(ch)

#     pdf.output(f'./example.pdf', 'F')


def generate_report(pocetni_datum, krajnji_datum, administracija_engine):
    # Load data
    with administracija_engine.connect() as connection:
        df_usluga = pd.read_sql(f'SELECT * FROM Promet WHERE Datum BETWEEN {pocetni_datum} AND {krajnji_datum}', connection)
        df_gorivo = pd.read_sql(f'SELECT * FROM Gorivo WHERE Datum BETWEEN {pocetni_datum} AND {krajnji_datum}', connection)
        df_servis = pd.read_sql(f'SELECT * FROM Servis WHERE Datum BETWEEN {pocetni_datum} AND {krajnji_datum}', connection)
        df_kazne = pd.read_sql(f'SELECT * FROM Kazne WHERE Datum BETWEEN {pocetni_datum} AND {krajnji_datum}', connection)
        df_trosak = pd.read_sql(f'SELECT * FROM Trošak WHERE Datum BETWEEN {pocetni_datum} AND {krajnji_datum}', connection)
        # Load other DataFrames (df_gorivo, df_servis, df_kazne, df_trosak) similarly

    # Prepare data for the Jinja2 template
    template_data = {
        'current_date': datetime.today().strftime("%d.%m.%Y"),
        'pocetni_datum': str(datetime.strftime(pocetni_datum, '%d.%m.%Y')),
        'krajnji_datum': str(datetime.strftime(krajnji_datum, '%d.%m.%Y')),
        'promet_gotovina': df_usluga['Iznos gotovina (KM)'].sum(),
        'promet_ziralno': df_usluga['Iznos žiralno (KM)'].sum(),
        'ukupno_promet': df_usluga['Iznos gotovina (KM)'].sum() + df_usluga['Iznos žiralno (KM)'].sum(),
        'nenaplaceno': df_usluga[df_usluga['Plaćeno'] == 'NE']['Iznos gotovina (KM)'].sum() + df_usluga[df_usluga['Plaćeno'] == 'NE']['Iznos žiralno (KM)'].sum(),
        'broj_gratis': len(df_usluga[df_usluga['Plaćeno'] == 'GRATIS']),
        'gratis_rows': df_usluga[df_usluga['Plaćeno'] == 'GRATIS'].to_dict(orient='records'),

        # Data for GORIVO DataFrame
        'gorivo_predjena_kilometraza': df_usluga['Kilometraža'].sum(),
        'gorivo_prosjecna_cijena': df_gorivo['Cijena goriva (KM)'].mean(),
        'gorivo_nasuta_kolicina': df_gorivo['Nasuta količina (l)'].sum(),
        'gorivo_ukupno_placeno': df_gorivo['Iznos (KM)'].sum(),

        # Data for KAZNE DataFrame
        'kazne_broj_prekrsaja': len(df_kazne),
        'kazne_ukupan_trosak': df_kazne['Iznos (KM)'].sum(),

        # Data for SERVIS DataFrame
        'servis_broj_servisa': len(df_servis),

        # Data for TROSKOVI DataFrame
        'trosak_ukupan_iznos': df_trosak['Iznos (KM)'].sum(),
        # Add other data for KILOMETRAZA, GORIVO, KAZNE, SERVIS, and TROSKOVI as needed
    }

    # Load the Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')

    # Render the template with data
    rendered_html = template.render(template_data)

    # Save the report to a file (or send it as an email, etc.)
    with open('example_report.html', 'w') as report_file:
        report_file.write(rendered_html)
    # Create a PDF from the rendered HTML
    HTML(string=rendered_html).write_pdf(f'Izvještaj_{pocetni_datum}-{krajnji_datum}.pdf')
