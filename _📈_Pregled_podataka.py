import streamlit as st
import mariadb
import datetime
import os
import pandas as pd
import subprocess
import streamlit_nested_layout
import streamlit_authenticator as stauth
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
from report import generate_report

load_dotenv()

st.set_page_config(
    page_title="Pregled podataka",
    page_icon="📈",
    layout="wide"
)

#find_db_ip_command = ["docker", "inspect", "-f", "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}", "db"]
#db_ip_output = subprocess.check_output(find_db_ip_command, universal_newlines=True).strip()

# cell_hover = {  # for row hover use <tr> instead of <td>
#     'selector': 'td:hover',
#     'props': [('background-color', '#ffffb3')]
# }
# index_names = {
#     'selector': '.index_name',
#     'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
# }
# headers = {
#     'selector': 'th:not(.index_name)',
#     'props': 'background-color: #000066; color: white;'
# }


@st.cache_resource
def administracija_sqlalchemy():

    # sqlalchemy engine and connection
    engine = create_engine(
    f"mariadb+mariadbconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}",
    poolclass=QueuePool, pool_size=5, max_overflow=10)
    return engine

administracija_engine = administracija_sqlalchemy()

db_host = os.getenv("DB_HOST")
#db_host = db_ip_output
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# secrets_path = "./.streamlit"
# if not os.path.exists(secrets_path):
#     # Create the directory
#     os.makedirs(secrets_path)
#     with open(f"{secrets_path}/secrets.toml", "w") as file:
#         file.write("[connections.mariadb]\n")
#         file.write('dialect="mariadb"\n')
#         file.write(f'host="{db_host}"\n')
#         file.write(f'port={db_port}\n')
#         file.write(f'database="{db_database}"\n')
#         file.write(f'username="{db_user}"\n')
#         file.write(f'password="{db_password}"')
#         file.close()



# connection parameters
conn_params = {
    "user" : os.getenv('DB_USER'),
    "password" : os.getenv('DB_PASSWORD'),
    "host" : os.getenv('DB_HOST'),
    #"host": db_host,
    "port" : int(os.getenv('DB_PORT')),
    "database" : os.getenv('DB_DATABASE')
}

def clear_cache():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)


# Establish a connection
# connection_1 = mariadb.connect(**conn_params)
# connection = st.experimental_connection('mariadb', type='sql')
# cursor = connection_1.cursor()

#danas = datetime.date.today()
#danas = danas.strftime("%d.%m.%Y")

st.title('Administracija finansija')
st.subheader("Pregled podataka")
st.write("---")


sidebar = st.sidebar
with sidebar:

    #datum = st.date_input("Unesite datum", format="DD.MM.YYYY")
    #st.write(type(datum))
    odabir_tabele = st.selectbox("Odaberite tabelu iz baze podataka", ("Promet", "Gorivo", "Servis", "Kazne", "Trošak"))
    st.info(f"Odabrali ste tabelu {odabir_tabele}.")
base_query = f'SELECT * from {odabir_tabele};'
rest_of_query = ""

with administracija_engine.connect() as administracija_connection:
    df = pd.read_sql(base_query, administracija_connection)

if odabir_tabele == "Promet":

    with sidebar:
        
        st.header(f"Filtriranje pretrage za tabelu {odabir_tabele}")
        st.button("Poništi filtere", on_click=clear_cache)

        # DATUM
        donja_datum = None
        gornja_datum = None
        if 'donja_datum_promet' not in st.session_state:
            st.session_state.donja_datum_promet = donja_datum
        if 'gornja_datum_promet' not in st.session_state:
            st.session_state.gornja_datum_promet = gornja_datum
        query_part_datum = ""
        with st.form("_datum", clear_on_submit=False):
            st.write("Unesite raspon datuma")
            donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
            gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
            if st.form_submit_button("Potvrda"):
                donja_datum = donja_datum
                gornja_datum = gornja_datum
                st.session_state.donja_datum_promet = donja_datum
                st.session_state.gornja_datum_promet = gornja_datum
        if st.session_state.donja_datum_promet != None and st.session_state.gornja_datum_promet != None:
            query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum_promet}" AND "{st.session_state.gornja_datum_promet}"'
        rest_of_query = rest_of_query + " " + query_part_datum
    
        # NAZIV KLIJENTA
        konacan_naziv = ""
        if 'naziv_klijenta' not in st.session_state:
            st.session_state.naziv_klijenta = konacan_naziv
        query_part_naziv = ""
        with st.form("_naziv_klijenta", clear_on_submit=False):
            unos_naziv_klijenta = st.text_input("Naziv (ime) klijenta", "")
            if st.form_submit_button("Potvrda"):
                konacan_naziv = unos_naziv_klijenta
                st.session_state.naziv_klijenta = konacan_naziv
        if st.session_state.naziv_klijenta != "":
            query_part_naziv = f'AND `Naziv(ime) klijenta` = "{st.session_state.naziv_klijenta}"'
        rest_of_query = rest_of_query + " " + query_part_naziv

        # KILOMETRAZA
        donja_kilometraza = None
        gornja_kilometraza = None
        if 'donja_kilometraza' not in st.session_state:
            st.session_state.donja_kilometraza = donja_kilometraza
        if 'gornja_kilometraza' not in st.session_state:
            st.session_state.gornja_kilometraza = gornja_kilometraza
        query_part_kilometraza = "" 
        with st.form("_raspon_kilometraze", clear_on_submit=False):
            st.write("Unesite raspon kilometraže")
            donja_kilometraza = st.number_input("Donja granica", min_value=float(0))
            gornja_kilometraza = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_kilometraza = donja_kilometraza
                gornja_kilometraza = gornja_kilometraza
                st.session_state.donja_kilometraza = donja_kilometraza
                st.session_state.gornja_kilometraza = gornja_kilometraza
        if st.session_state.donja_kilometraza != None and st.session_state.gornja_kilometraza != None:
            query_part_kilometraza = f'AND Kilometraža BETWEEN {st.session_state.donja_kilometraza} AND {st.session_state.gornja_kilometraza}'
        rest_of_query = rest_of_query + " " + query_part_kilometraza
        
        # STARTNO MJESTO
        startno_mjesto_konacno = ""
        if 'startno_mjesto' not in st.session_state:
            st.session_state.startno_mjesto = startno_mjesto_konacno
        query_part_start = ""
        with st.form("_startno_mjesto", clear_on_submit=False):
            startno_mjesto = st.text_input("Startno mjesto", "")
            if st.form_submit_button("Potvrda"):
                startno_mjesto_konacno = startno_mjesto
                st.session_state.startno_mjesto = startno_mjesto_konacno
        if st.session_state.startno_mjesto != "":
            query_part_start = f'AND `Startno mjesto` = "{st.session_state.startno_mjesto}"'
        rest_of_query = rest_of_query + " " + query_part_start

        # CILJNO MJESTO
        ciljno_mjesto_konacno = ""
        if 'ciljno_mjesto' not in st.session_state:
            st.session_state.ciljno_mjesto = ciljno_mjesto_konacno
        query_part_cilj = ""
        with st.form("_ciljno_mjesto", clear_on_submit=False):
            ciljno_mjesto = st.text_input("Ciljno mjesto", "")
            if st.form_submit_button("Potvrda"):
                ciljno_mjesto_konacno = ciljno_mjesto
                st.session_state.ciljno_mjesto = ciljno_mjesto_konacno
        if st.session_state.ciljno_mjesto != "":
            query_part_cilj = f'AND `Ciljno mjesto` = "{st.session_state.ciljno_mjesto}"'
        rest_of_query = rest_of_query + " " + query_part_cilj

        # LOKACIJA
        lokacija_konacno = ""
        if 'lokacija' not in st.session_state:
            st.session_state.lokacija = lokacija_konacno
        query_part_lokacija = ""
        with st.form("_lokacija", clear_on_submit=False):
            lokacija = st.selectbox(label="Lokacija", options=("BiH", "Inostranstvo"))
            if st.form_submit_button("Potvrda"):
                lokacija_konacno = lokacija
                st.session_state.lokacija = lokacija_konacno
        if st.session_state.lokacija != "":
            query_part_lokacija = f'AND Lokacija = "{st.session_state.lokacija}"'
        rest_of_query = rest_of_query + " " + query_part_lokacija

        # IZNOS GOTOVINA
        donja_iznos_gotovina = None
        gornja_iznos_gotovina = None
        if 'donja_iznos_gotovina' not in st.session_state:
            st.session_state.donja_iznos_gotovina = donja_iznos_gotovina
        if 'gornja_iznos_gotovina' not in st.session_state:
            st.session_state.gornja_iznos_gotovina = gornja_iznos_gotovina
        query_part_iznos_gotovina = "" 
        with st.form("_iznos_gotovina", clear_on_submit=False):
            st.write("Unesite raspon iznosa u gotovini")
            donja_iznos_gotovina = st.number_input("Donja granica", min_value=float(0))
            gornja_iznos_gotovina = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_iznos_gotovina = donja_iznos_gotovina
                gornja_iznos_gotovina = gornja_iznos_gotovina
                st.session_state.donja_iznos_gotovina = donja_iznos_gotovina
                st.session_state.gornja_iznos_gotovina = gornja_iznos_gotovina
        if st.session_state.donja_iznos_gotovina != None and st.session_state.gornja_iznos_gotovina != None:
            query_part_iznos_gotovina = f'AND `Iznos gotovina (KM)` BETWEEN {st.session_state.donja_iznos_gotovina} AND {st.session_state.gornja_iznos_gotovina}'
        rest_of_query = rest_of_query + " " + query_part_iznos_gotovina

        # IZNOS ZIRALNO
        donja_iznos_ziralno = None
        gornja_iznos_ziralno = None
        if 'donja_iznos_ziralno' not in st.session_state:
            st.session_state.donja_iznos_ziralno = donja_iznos_ziralno
        if 'gornja_iznos_ziralno' not in st.session_state:
            st.session_state.gornja_iznos_ziralno = gornja_iznos_ziralno
        query_part_iznos_ziralno = "" 
        with st.form("_iznos_ziralno", clear_on_submit=False):
            st.write("Unesite raspon žiralnog iznosa")
            donja_iznos_ziralno = st.number_input("Donja granica", min_value=float(0))
            gornja_iznos_ziralno = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_iznos_ziralno = donja_iznos_ziralno
                gornja_iznos_ziralno = gornja_iznos_ziralno
                st.session_state.donja_iznos_ziralno = donja_iznos_ziralno
                st.session_state.gornja_iznos_ziralno = gornja_iznos_ziralno
        if st.session_state.donja_iznos_ziralno != None and st.session_state.gornja_iznos_ziralno != None:
            query_part_iznos_ziralno = f'AND `Iznos žiralno (KM)` BETWEEN {st.session_state.donja_iznos_ziralno} AND {st.session_state.gornja_iznos_ziralno}'
        rest_of_query = rest_of_query + " " + query_part_iznos_ziralno

        # PLACENO
        placeno_konacno = ""
        if 'placeno' not in st.session_state:
            st.session_state.placeno = placeno_konacno
        query_part_placeno = ""
        with st.form("_placeno", clear_on_submit=False):
            placeno = st.selectbox(label="Plaćeno", options=("DA", "NE", "GRATIS"))
            if st.form_submit_button("Potvrda"):
                placeno_konacno = placeno
                st.session_state.placeno = placeno_konacno
        if st.session_state.placeno != "":
            query_part_placeno = f'AND Plaćeno = "{st.session_state.placeno}"'
        rest_of_query = rest_of_query + " " + query_part_placeno

        # OPERATIVNI TROSAK
        donja_op_trosak = None
        gornja_op_trosak = None
        if 'donja_op_trosak' not in st.session_state:
            st.session_state.donja_op_trosak = donja_op_trosak
        if 'gornja_op_trosak' not in st.session_state:
            st.session_state.gornja_op_trosak = gornja_op_trosak
        query_part_op_trosak = "" 
        with st.form("_op_trosak", clear_on_submit=False):
            st.write("Unesite raspon operativnog troška")
            donja_op_trosak = st.number_input("Donja granica", min_value=float(0))
            gornja_op_trosak = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_op_trosak = donja_op_trosak
                gornja_op_trosak = gornja_op_trosak
                st.session_state.donja_op_trosak = donja_op_trosak
                st.session_state.gornja_op_trosak = gornja_op_trosak
        if st.session_state.donja_op_trosak != None and st.session_state.gornja_op_trosak != None:
            query_part_op_trosak = f'AND `Operativni trošak (KM)` BETWEEN {st.session_state.donja_op_trosak} AND {st.session_state.gornja_op_trosak}'
        rest_of_query = rest_of_query + " " + query_part_op_trosak

        # NETO ZARADA
        donja_neto_zarada = None
        gornja_neto_zarada = None
        if 'donja_neto_zarada' not in st.session_state:
            st.session_state.donja_neto_zarada = donja_neto_zarada
        if 'gornja_neto_zarada' not in st.session_state:
            st.session_state.gornja_neto_zarada = gornja_neto_zarada
        query_part_neto_zarada = "" 
        with st.form("_neto_zarada", clear_on_submit=False):
            st.write("Unesite raspon neto zarade")
            donja_neto_zarada = st.number_input("Donja granica", min_value=float(0))
            gornja_neto_zarada = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_neto_zarada = donja_neto_zarada
                gornja_neto_zarada = gornja_neto_zarada
                st.session_state.donja_neto_zarada = donja_neto_zarada
                st.session_state.gornja_neto_zarada = gornja_neto_zarada
        if st.session_state.donja_neto_zarada != None and st.session_state.donja_neto_zarada != None:
            query_part_neto_zarada = f'AND `Neto zarada (KM)` BETWEEN {st.session_state.donja_neto_zarada} AND {st.session_state.gornja_neto_zarada}'
        rest_of_query = rest_of_query + " " + query_part_neto_zarada

        # KOMENTAR
        komentar_konacno = ""
        if 'komentar_promet' not in st.session_state:
            st.session_state.komentar_promet = komentar_konacno
        query_part_komentar = ""
        with st.form("_komentar_promet", clear_on_submit=False):
            komentar = st.text_input("Komentar/Napomena", "")
            if st.form_submit_button("Potvrda"):
                komentar_konacno = komentar
                st.session_state.komentar_promet = komentar_konacno
        if st.session_state.komentar_promet != "":
            query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar_promet}"'
        rest_of_query = rest_of_query + " " + query_part_komentar

    # QUERY
    if rest_of_query.strip() != "":
        rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
        query = f'SELECT * from {odabir_tabele} WHERE {rest_of_query};'
        with administracija_engine.connect() as administracija_connection:
            df = pd.read_sql(query, administracija_connection)
        

if odabir_tabele == "Gorivo":

    with sidebar:
        
        st.header(f"Filtriranje pretrage za tabelu {odabir_tabele}")
        st.button("Poništi filtere", on_click=clear_cache)

        # DATUM
        donja_datum = None
        gornja_datum = None
        if 'donja_datum_gorivo' not in st.session_state:
            st.session_state.donja_datum_gorivo = donja_datum
        if 'gornja_datum_gorivo' not in st.session_state:
            st.session_state.gornja_datum_gorivo = gornja_datum
        query_part_datum = ""
        with st.form("_datum_gorivo", clear_on_submit=False):
            st.write("Unesite raspon datuma")
            donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
            gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
            if st.form_submit_button("Potvrda"):
                donja_datum = donja_datum
                gornja_datum = gornja_datum
                st.session_state.donja_datum_gorivo = donja_datum
                st.session_state.gornja_datum_gorivo = gornja_datum
        if st.session_state.donja_datum_gorivo != None and st.session_state.gornja_datum_gorivo != None:
            query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum_gorivo}" AND "{st.session_state.gornja_datum_gorivo}"'
        rest_of_query = rest_of_query + " " + query_part_datum

        # NASUTA KOLICINA
        donja_nasuta_kolicina = None
        gornja_nasuta_kolicina = None
        if 'donja_nasuta_kolicina' not in st.session_state:
            st.session_state.donja_nasuta_kolicina = donja_nasuta_kolicina
        if 'gornja_nasuta_kolicina' not in st.session_state:
            st.session_state.gornja_nasuta_kolicina = gornja_nasuta_kolicina
        query_part_nasuta_kolicina = "" 
        with st.form("_raspon_nasute_kolicine", clear_on_submit=False):
            st.write("Unesite raspon nasute količine goriva")
            donja_nasuta_kolicina = st.number_input("Donja granica", min_value=float(0))
            gornja_nasuta_kolicina = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_nasuta_kolicina = donja_nasuta_kolicina
                gornja_nasuta_kolicina = gornja_nasuta_kolicina
                st.session_state.donja_nasuta_kolicina = donja_nasuta_kolicina
                st.session_state.gornja_nasuta_kolicina = gornja_nasuta_kolicina
        if st.session_state.donja_nasuta_kolicina != None and st.session_state.gornja_nasuta_kolicina != None:
            query_part_nasuta_kolicina = f'AND `Nasuta količina (l)` BETWEEN {st.session_state.donja_nasuta_kolicina} AND {st.session_state.gornja_nasuta_kolicina}'
        rest_of_query = rest_of_query + " " + query_part_nasuta_kolicina

        # CIJENA GORIVA
        donja_cijena_goriva = None
        gornja_cijena_goriva = None
        if 'donja_cijena_goriva' not in st.session_state:
            st.session_state.donja_cijena_goriva = donja_cijena_goriva
        if 'gornja_cijena_goriva' not in st.session_state:
            st.session_state.gornja_cijena_goriva = gornja_cijena_goriva
        query_part_cijena_goriva = "" 
        with st.form("_raspon_cijene_goriva", clear_on_submit=False):
            st.write("Unesite raspon cijene goriva")
            donja_cijena_goriva = st.number_input("Donja granica", min_value=float(0))
            gornja_cijena_goriva = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_cijena_goriva = donja_cijena_goriva
                gornja_cijena_goriva = gornja_cijena_goriva
                st.session_state.donja_cijena_goriva = donja_cijena_goriva
                st.session_state.gornja_cijena_goriva = gornja_cijena_goriva
        if st.session_state.donja_cijena_goriva != None and st.session_state.gornja_cijena_goriva != None:
            query_part_cijena_goriva = f'AND `Cijena goriva (KM)` BETWEEN {st.session_state.donja_cijena_goriva} AND {st.session_state.gornja_cijena_goriva}'
        rest_of_query = rest_of_query + " " + query_part_cijena_goriva

        # IZNOS GORIVO
        donja_iznos_gorivo = None
        gornja_iznos_gorivo = None
        if 'donja_iznos_gorivo' not in st.session_state:
            st.session_state.donja_iznos_gorivo = donja_iznos_gorivo
        if 'gornja_iznos_gorivo' not in st.session_state:
            st.session_state.gornja_iznos_gorivo = gornja_iznos_gorivo
        query_part_iznos_gorivo = "" 
        with st.form("_iznos_gorivo", clear_on_submit=False):
            st.write("Unesite raspon iznosa goriva")
            donja_iznos_gorivo = st.number_input("Donja granica", min_value=float(0))
            gornja_iznos_gorivo = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_iznos_gorivo = donja_iznos_gorivo
                gornja_iznos_gorivo = gornja_iznos_gorivo
                st.session_state.donja_iznos_gorivo = donja_iznos_gorivo
                st.session_state.gornja_iznos_gorivo = gornja_iznos_gorivo
        if st.session_state.donja_iznos_gorivo != None and st.session_state.gornja_iznos_gorivo != None:
            query_part_iznos_gorivo = f'AND `Iznos (KM)` BETWEEN {st.session_state.donja_iznos_gorivo} AND {st.session_state.gornja_iznos_gorivo}'
        rest_of_query = rest_of_query + " " + query_part_iznos_gorivo

        # NACIN PLACANJA
        nacin_placanja_konacno = ""
        if 'nacin_placanja_gorivo' not in st.session_state:
            st.session_state.nacin_placanja_gorivo = nacin_placanja_konacno
        query_part_nacin_placanja = ""
        with st.form("_nacin_placanja_gorivo", clear_on_submit=False):
            nacin_placanja = st.selectbox(label="Način plaćanja", options=('Gotovina', 'Žiralno', 'Kartica'))
            if st.form_submit_button("Potvrda"):
                nacin_placanja_konacno = nacin_placanja
                st.session_state.nacin_placanja_gorivo = nacin_placanja_konacno
        if st.session_state.nacin_placanja_gorivo != "":
            query_part_nacin_placanja = f'AND `Način plaćanja` = "{st.session_state.nacin_placanja_gorivo}"'
        rest_of_query = rest_of_query + " " + query_part_nacin_placanja

        # BENZINSKA PUMPA
        benz_pumpa_konacno = ""
        if 'benz_pumpa' not in st.session_state:
            st.session_state.benz_pumpa = benz_pumpa_konacno
        query_part_benz_pumpa = ""
        with st.form("_benz_pumpa", clear_on_submit=False):
            benz_pumpa = st.text_input("Naziv benzinske pumpe", "")
            if st.form_submit_button("Potvrda"):
                benz_pumpa_konacno = benz_pumpa
                st.session_state.benz_pumpa = benz_pumpa_konacno
        if st.session_state.benz_pumpa != "":
            query_part_benz_pumpa = f'AND `Benzinska pumpa` = "{st.session_state.benz_pumpa}"'
        rest_of_query = rest_of_query + " " + query_part_benz_pumpa

        # KOMENTAR
        komentar_konacno = ""
        if 'komentar_gorivo' not in st.session_state:
            st.session_state.komentar_gorivo = komentar_konacno
        query_part_komentar = ""
        with st.form("_komentar_gorivo", clear_on_submit=False):
            komentar = st.text_input("Komentar/Napomena", "")
            if st.form_submit_button("Potvrda"):
                komentar_konacno = komentar
                st.session_state.komentar_gorivo = komentar_konacno
        if st.session_state.komentar_gorivo != "":
            query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar_gorivo}"'
        rest_of_query = rest_of_query + " " + query_part_komentar

    # QUERY
    if rest_of_query.strip() != "":
        rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
        query = f'SELECT * from {odabir_tabele} WHERE {rest_of_query};'
        with administracija_engine.connect() as administracija_connection:
            df = pd.read_sql(query, administracija_connection)


if odabir_tabele == "Servis":

    with sidebar:

        st.header(f"Filtriranje pretrage za tabelu {odabir_tabele}")
        st.button("Poništi filtere", on_click=clear_cache)

        # DATUM
        donja_datum = None
        gornja_datum = None
        if 'donja_datum_servis' not in st.session_state:
            st.session_state.donja_datum_servis = donja_datum
        if 'gornja_datum_servis' not in st.session_state:
            st.session_state.gornja_datum_servis = gornja_datum
        query_part_datum = ""
        with st.form("_datum_servis", clear_on_submit=False):
            st.write("Unesite raspon datuma")
            donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
            gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
            if st.form_submit_button("Potvrda"):
                donja_datum = donja_datum
                gornja_datum = gornja_datum
                st.session_state.donja_datum_servis = donja_datum
                st.session_state.gornja_datum_servis = gornja_datum
        if st.session_state.donja_datum_servis != None and st.session_state.gornja_datum_servis != None:
            query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum_servis}" AND "{st.session_state.gornja_datum_servis}"'
        rest_of_query = rest_of_query + " " + query_part_datum

        # OPIS
        konacan_opis = ""
        if 'opis_servis' not in st.session_state:
            st.session_state.opis_servis = konacan_opis
        query_part_opis = ""
        with st.form("_opis_servis", clear_on_submit=False):
            opis = st.text_input("Opis", "")
            if st.form_submit_button("Potvrda"):
                konacan_opis = opis
                st.session_state.opis_servis = konacan_opis
        if st.session_state.opis_servis != "":
            query_part_opis = f'AND Opis = "{st.session_state.opis_servis}"'
        rest_of_query = rest_of_query + " " + query_part_opis

        # KILOMETRAZA
        donja_kilometraza = None
        gornja_kilometraza = None
        if 'donja_kilometraza_servis' not in st.session_state:
            st.session_state.donja_kilometraza_servis = donja_kilometraza
        if 'gornja_kilometraza_servis' not in st.session_state:
            st.session_state.gornja_kilometraza_servis = gornja_kilometraza
        query_part_kilometraza = "" 
        with st.form("_raspon_kilometraze_servis", clear_on_submit=False):
            st.write("Unesite raspon kilometraže")
            donja_kilometraza = st.number_input("Donja granica", min_value=float(0))
            gornja_kilometraza = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_kilometraza = donja_kilometraza
                gornja_kilometraza = gornja_kilometraza
                st.session_state.donja_kilometraza_servis = donja_kilometraza
                st.session_state.gornja_kilometraza_servis = gornja_kilometraza
        if st.session_state.donja_kilometraza_servis != None and st.session_state.gornja_kilometraza_servis != None:
            query_part_kilometraza = f'AND Kilometraža BETWEEN {st.session_state.donja_kilometraza_servis} AND {st.session_state.gornja_kilometraza_servis}'
        rest_of_query = rest_of_query + " " + query_part_kilometraza  

        # IZNOS
        donja_iznos = None
        gornja_iznos = None
        if 'donja_iznos_servis' not in st.session_state:
            st.session_state.donja_iznos_servis = donja_iznos
        if 'gornja_iznos_servis' not in st.session_state:
            st.session_state.gornja_iznos_servis = gornja_iznos
        query_part_iznos = "" 
        with st.form("_iznos_servis", clear_on_submit=False):
            st.write("Unesite raspon iznosa")
            donja_iznos = st.number_input("Donja granica", min_value=float(0))
            gornja_iznos = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_iznos = donja_iznos
                gornja_iznos = gornja_iznos
                st.session_state.donja_iznos_servis = donja_iznos
                st.session_state.gornja_iznos_servis = gornja_iznos
        if st.session_state.donja_iznos_servis != None and st.session_state.gornja_iznos_servis != None:
            query_part_iznos = f'AND `Iznos (KM)` BETWEEN {st.session_state.donja_iznos_servis} AND {st.session_state.gornja_iznos_servis}'
        rest_of_query = rest_of_query + " " + query_part_iznos

        # NACIN PLACANJA
        nacin_placanja_konacno = ""
        if 'nacin_placanja_servis' not in st.session_state:
            st.session_state.nacin_placanja_servis = nacin_placanja_konacno
        query_part_nacin_placanja = ""
        with st.form("_nacin_placanja_servis", clear_on_submit=False):
            nacin_placanja = st.selectbox(label="Način plaćanja", options=('Gotovina', 'Žiralno', 'Kartica'))
            if st.form_submit_button("Potvrda"):
                nacin_placanja_konacno = nacin_placanja
                st.session_state.nacin_placanja_servis = nacin_placanja_konacno
        if st.session_state.nacin_placanja_servis != "":
            query_part_nacin_placanja = f'AND `Način plaćanja` = "{st.session_state.nacin_placanja_servis}"'
        rest_of_query = rest_of_query + " " + query_part_nacin_placanja

        # KOMENTAR
        komentar_konacno = ""
        if 'komentar_servis' not in st.session_state:
            st.session_state.komentar_servis = komentar_konacno
        query_part_komentar = ""
        with st.form("_komentar_servis", clear_on_submit=False):
            komentar = st.text_input("Komentar/Napomena", "")
            if st.form_submit_button("Potvrda"):
                komentar_konacno = komentar
                st.session_state.komentar_servis = komentar_konacno
        if st.session_state.komentar_servis != "":
            query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar_servis}"'
        rest_of_query = rest_of_query + " " + query_part_komentar

    # QUERY
    if rest_of_query.strip() != "":
        rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
        query = f'SELECT * from {odabir_tabele} WHERE {rest_of_query};'
        with administracija_engine.connect() as administracija_connection:
            df = pd.read_sql(query, administracija_connection)

if odabir_tabele == "Kazne":

    with sidebar:
        
        st.header(f"Filtriranje pretrage za tabelu {odabir_tabele}")
        st.button("Poništi filtere", on_click=clear_cache)

        # DATUM
        donja_datum = None
        gornja_datum = None
        if 'donja_datum_kazne' not in st.session_state:
            st.session_state.donja_datum_kazne = donja_datum
        if 'gornja_datum_kazne' not in st.session_state:
            st.session_state.gornja_datum_kazne = gornja_datum
        query_part_datum = ""
        with st.form("_datum_kazne", clear_on_submit=False):
            st.write("Unesite raspon datuma")
            donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
            gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
            if st.form_submit_button("Potvrda"):
                donja_datum = donja_datum
                gornja_datum = gornja_datum
                st.session_state.donja_datum_kazne = donja_datum
                st.session_state.gornja_datum_kazne = gornja_datum
        if st.session_state.donja_datum_kazne != None and st.session_state.gornja_datum_kazne != None:
            query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum_kazne}" AND "{st.session_state.gornja_datum_kazne}"'
        rest_of_query = rest_of_query + " " + query_part_datum

        # PREKRSAJ
        prekrsaj_konacno = ""
        if 'prekrsaj' not in st.session_state:
            st.session_state.prekrsaj = prekrsaj_konacno
        query_part_prekrsaj = ""
        with st.form("_prekrsaj", clear_on_submit=False):
            prekrsaj = st.text_input("Prekršaj", "")
            if st.form_submit_button("Potvrda"):
                prekrsaj_konacno = prekrsaj
                st.session_state.prekrsaj = prekrsaj_konacno
        if st.session_state.prekrsaj != "":
            query_part_prekrsaj = f'AND Prekršaj = "{st.session_state.prekrsaj}"'
        rest_of_query = rest_of_query + " " + query_part_prekrsaj

        # IZNOS
        donja_iznos = None
        gornja_iznos = None
        if 'donja_iznos_kazne' not in st.session_state:
            st.session_state.donja_iznos_kazne = donja_iznos
        if 'gornja_iznos_kazne' not in st.session_state:
            st.session_state.gornja_iznos_kazne = gornja_iznos
        query_part_iznos = "" 
        with st.form("_iznos_kazne", clear_on_submit=False):
            st.write("Unesite raspon iznosa")
            donja_iznos = st.number_input("Donja granica", min_value=float(0))
            gornja_iznos = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_iznos = donja_iznos
                gornja_iznos = gornja_iznos
                st.session_state.donja_iznos_kazne = donja_iznos
                st.session_state.gornja_iznos_kazne = gornja_iznos
        if st.session_state.donja_iznos_kazne != None and st.session_state.gornja_iznos_kazne != None:
            query_part_iznos = f'AND `Iznos (KM)` BETWEEN {st.session_state.donja_iznos_kazne} AND {st.session_state.gornja_iznos_kazne}'
        rest_of_query = rest_of_query + " " + query_part_iznos

        # KOMENTAR
        komentar_konacno = ""
        if 'komentar_kazne' not in st.session_state:
            st.session_state.komentar_kazne = komentar_konacno
        query_part_komentar = ""
        with st.form("_komentar_kazne", clear_on_submit=False):
            komentar = st.text_input("Komentar/Napomena", "")
            if st.form_submit_button("Potvrda"):
                komentar_konacno = komentar
                st.session_state.komentar_kazne = komentar_konacno
        if st.session_state.komentar_kazne != "":
            query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar_kazne}"'
        rest_of_query = rest_of_query + " " + query_part_komentar

    # QUERY
    if rest_of_query.strip() != "":
        rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
        query = f'SELECT * from {odabir_tabele} WHERE {rest_of_query};'
        with administracija_engine.connect() as administracija_connection:
            df = pd.read_sql(query, administracija_connection)


if odabir_tabele == "Trošak":

    with sidebar:
        
        st.header(f"Filtriranje pretrage za tabelu {odabir_tabele}")
        st.button("Poništi filtere", on_click=clear_cache)

        # DATUM
        donja_datum = None
        gornja_datum = None
        if 'donja_datum_trosak' not in st.session_state:
            st.session_state.donja_datum_trosak = donja_datum
        if 'gornja_datum_trosak' not in st.session_state:
            st.session_state.gornja_datum_trosak = gornja_datum
        query_part_datum = ""
        with st.form("_datum_trosak", clear_on_submit=False):
            st.write("Unesite raspon datuma")
            donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
            gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
            if st.form_submit_button("Potvrda"):
                donja_datum = donja_datum
                gornja_datum = gornja_datum
                st.session_state.donja_datum_trosak = donja_datum
                st.session_state.gornja_datum_trosak = gornja_datum
        if st.session_state.donja_datum_trosak != None and st.session_state.gornja_datum_trosak != None:
            query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum_trosak}" AND "{st.session_state.gornja_datum_trosak}"'
        rest_of_query = rest_of_query + " " + query_part_datum

        # OPIS
        konacan_opis = ""
        if 'opis_trosak' not in st.session_state:
            st.session_state.opis_trosak = konacan_opis
        query_part_opis = ""
        with st.form("_opis_trosak", clear_on_submit=False):
            opis = st.text_input("Opis", "")
            if st.form_submit_button("Potvrda"):
                konacan_opis = opis
                st.session_state.opis_trosak = konacan_opis
        if st.session_state.opis_trosak != "":
            query_part_opis = f'AND Opis = "{st.session_state.opis_trosak}"'
        rest_of_query = rest_of_query + " " + query_part_opis

        # DODATNI OPIS
        konacan_dodatni_opis = ""
        if 'dodatni_opis_trosak' not in st.session_state:
            st.session_state.dodatni_opis_trosak = konacan_dodatni_opis
        query_part_dodatni_opis = ""
        with st.form("_dodatni_opis_trosak", clear_on_submit=False):
            dodatni_opis = st.text_input("Opis", "")
            if st.form_submit_button("Potvrda"):
                konacan_dodatni_opis = dodatni_opis
                st.session_state.dodatni_opis_trosak = konacan_dodatni_opis
        if st.session_state.dodatni_opis_trosak != "":
            query_part_dodatni_opis = f'AND `Dodatni opis (opciono)` = "{st.session_state.dodatni_opis_trosak}"'
        rest_of_query = rest_of_query + " " + query_part_dodatni_opis

        # IZNOS
        donja_iznos = None
        gornja_iznos = None
        if 'donja_iznos_trosak' not in st.session_state:
            st.session_state.donja_iznos_trosak = donja_iznos
        if 'gornja_iznos_trosak' not in st.session_state:
            st.session_state.gornja_iznos_trosak = gornja_iznos
        query_part_iznos = "" 
        with st.form("_iznos_trosak", clear_on_submit=False):
            st.write("Unesite raspon iznosa")
            donja_iznos = st.number_input("Donja granica", min_value=float(0))
            gornja_iznos = st.number_input("Gornja granica", min_value=float(0))
            if st.form_submit_button("Potvrda"):
                donja_iznos = donja_iznos
                gornja_iznos = gornja_iznos
                st.session_state.donja_iznos_trosak = donja_iznos
                st.session_state.gornja_iznos_trosak = gornja_iznos
        if st.session_state.donja_iznos_trosak != None and st.session_state.gornja_iznos_trosak != None:
            query_part_iznos = f'AND `Iznos (KM)` BETWEEN {st.session_state.donja_iznos_trosak} AND {st.session_state.gornja_iznos_trosak}'
        rest_of_query = rest_of_query + " " + query_part_iznos

        # NACIN PLACANJA
        nacin_placanja_konacno = ""
        if 'nacin_placanja_trosak' not in st.session_state:
            st.session_state.nacin_placanja_trosak = nacin_placanja_konacno
        query_part_nacin_placanja = ""
        with st.form("_nacin_placanja_trosak", clear_on_submit=False):
            nacin_placanja = st.selectbox(label="Način plaćanja", options=('Gotovina', 'Žiralno', 'Kartica'))
            if st.form_submit_button("Potvrda"):
                nacin_placanja_konacno = nacin_placanja
                st.session_state.nacin_placanja_trosak = nacin_placanja_konacno
        if st.session_state.nacin_placanja_trosak != "":
            query_part_nacin_placanja = f'AND `Način plaćanja` = "{st.session_state.nacin_placanja_trosak}"'
        rest_of_query = rest_of_query + " " + query_part_nacin_placanja

        # KOMENTAR
        komentar_konacno = ""
        if 'komentar_trosak' not in st.session_state:
            st.session_state.komentar_trosak = komentar_konacno
        query_part_komentar = ""
        with st.form("_komentar_trosak", clear_on_submit=False):
            komentar = st.text_input("Komentar/Napomena", "")
            if st.form_submit_button("Potvrda"):
                komentar_konacno = komentar
                st.session_state.komentar_trosak = komentar_konacno
        if st.session_state.komentar_trosak != "":
            query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar_trosak}"'
        rest_of_query = rest_of_query + " " + query_part_komentar

    # QUERY
    if rest_of_query.strip() != "":
        rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
        query = f'SELECT * from {odabir_tabele} WHERE {rest_of_query};'
        with administracija_engine.connect() as administracija_connection:
            df = pd.read_sql(query, administracija_connection)




#df = connection.query(f'SELECT * from {odabir_tabele} WHERE Datum = "{datum}";', ttl=600)
# df = connection.query(f'SELECT * from {odabir_tabele};', ttl=600)

# df = pd.DataFrame(df)
#df.style.format('{:.0f}').set_table_styles([cell_hover, index_names, headers])

#st.header("Pregled podataka")
st.subheader(f"{odabir_tabele}")
#print(df)
tabela = st.dataframe(data=df.drop(columns=["Redni broj"]), use_container_width=True, hide_index=False)

columns = st.columns([5, 5])

with st.columns([1, 1])[1]:
    with st.columns([1, 1])[1]:
        with st.columns([1, 1])[1]:
            
            with st.form("izvjestaj", clear_on_submit=True):
                st.write("Generiši izvještaj")
                donja_datum = st.date_input("Od", format="DD.MM.YYYY")
                gornja_datum = st.date_input("Do", format="DD.MM.YYYY")
                if st.form_submit_button("Potvrda"):
                    generate_report(donja_datum, gornja_datum, administracija_engine)

# imena_kolona_query = f"""
# SELECT COLUMN_NAME
# FROM INFORMATION_SCHEMA.COLUMNS
# WHERE TABLE_SCHEMA = '{os.getenv("DB_DATABASE")}'
#     AND TABLE_NAME = '{odabir_tabele}';
# """
# imena_kolona = connection.query(imena_kolona_query).values
# lista_kolona = [imena_kolona[i][0] for i in range(len(imena_kolona))]
#print(lista_kolona)

#all_queries=[]
# with sidebar:

#     with st.container():
#         st.header(f"Filtriranje pretrage za tabelu {odabir_tabele}")
#         with st.form("unos_podataka", clear_on_submit=True):
#             for kol in lista_kolona:
#                 if kol == 'Datum':
#                     unos = st.date_input("Unesite datum", format="DD.MM.YYYY")
#                     unos_dict = {f"`{kol}`" : f"STR_TO_DATE('{unos.strftime('%d.%m.%Y')}', '%d.%m.%Y')"}
#                     all_queries.append(unos_dict)
                
#                 elif kol == 'Lokacija':
#                     unos = st.selectbox(label="Lokacija", options=("BiH", "Inostranstvo"))
#                     unos_dict = {f"`{kol}`" : f"'{unos}'"}
#                     all_queries.append(unos_dict)
                
#                 elif kol == 'Plaćeno':
#                     unos = st.selectbox(label="Plaćeno", options=("DA", "NE"))
#                     unos_dict = {f"`{kol}`" : f"'{unos}'"}
#                     all_queries.append(unos_dict)
                
#                 elif kol in ['Kilometraža', 'Iznos gotovina', 'Iznos žiralno', 'Utrošak goriva (L)', 'Cijena', 'Iznos']:
#                     unos = st.number_input(kol)
#                     unos_dict = {f"`{kol}`" : str(unos)}
#                     all_queries.append(unos_dict)
                
#                 elif kol == 'Opis':
#                     unos = st.selectbox(label="Lokacija", options=("Svakodnevni trošak", "Terminal", "Autoput", "Mostarina"))
#                     unos_dict = {f"`{kol}`" : f"'{unos}'"}
#                     all_queries.append(unos_dict)
                
#                 else:
#                     unos = st.text_input(kol, "")
#                     unos_dict = {f"`{kol}`" : f"'{unos}'"}
#                     all_queries.append(unos_dict)
            
#             key_strings = []
#             value_strings = []
#             for query in all_queries:
#                 key_strings.append(f"{', '.join(query.keys())}")
#                 value_strings.append(f"{', '.join(query.values())}")
#             insert_query = f"INSERT INTO {odabir_tabele} ({', '.join(key_strings)}) VALUES ({', '.join(value_strings)});"
#             #print(insert_query)
#             #print(unos, type(unos))
#             #print(unos.strftime('%d.%m.%Y'), type(unos.strftime('%d.%m.%Y')))
#             submitted = st.form_submit_button("Potvrda")
#             if submitted:
#                 cursor.execute(insert_query)
#                 connection_1.commit()
#                 cursor.close()
#                 connection_1.close()
#                 st.experimental_rerun()

