import streamlit as st
import mariadb
import datetime
import os
import pandas as pd
import subprocess
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

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

# Establish a connection
# connection_1 = mariadb.connect(**conn_params)
# connection = st.experimental_connection('mariadb', type='sql')
# cursor = connection_1.cursor()

#danas = datetime.date.today()
#danas = danas.strftime("%d.%m.%Y")

st.title('Administracija finansija')
st.subheader("Pregled podataka")
st.write("---")

# if 'donja_datum' not in st.session_state:
#     st.session_state.donja_datum = None
# if 'gornja_datum' not in st.session_state:
#     st.session_state.gornja_datum = None
# if 'naziv_klijenta' not in st.session_state:
#     st.session_state.naziv_klijenta = None
# if 'donja_kilometraza' not in st.session_state:
#     st.session_state.donja_kilometraza = None
# if 'gornja_kilometraza' not in st.session_state:
#     st.session_state.gornja_kilometraza = None
# if 'startno_mjesto' not in st.session_state:
#     st.session_state.startno_mjesto = None
# if 'ciljno_mjesto' not in st.session_state:
#     st.session_state.ciljno_mjesto = None
# if 'lokacija' not in st.session_state:
#     st.session_state.lokacija = None
# if 'donja_iznos_gotovina' not in st.session_state:
#     st.session_state.donja_iznos_gotovina = None
# if 'gornja_iznos_gotovina' not in st.session_state:
#     st.session_state.gornja_iznos_gotovina = None
# if 'donja_iznos_ziralno' not in st.session_state:
#     st.session_state.donja_iznos_ziralno = None
# if 'gornja_iznos_ziralno' not in st.session_state:
#     st.session_state.gornja_iznos_ziralno = None
# if 'placeno' not in st.session_state:
#     st.session_state.placeno = None
# if 'donja_op_trosak' not in st.session_state:
#     st.session_state.donja_op_trosak = None
# if 'gornja_op_trosak' not in st.session_state:
#     st.session_state.gornja_op_trosak = None
# if 'donja_neto_zarada' not in st.session_state:
#     st.session_state.donja_neto_zarada = None
# if 'gornja_neto_zarada' not in st.session_state:
#     st.session_state.gornja_neto_zarada = None
# if 'komentar' not in st.session_state:
#     st.session_state.komentar = None


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
    values = {}
    vals = []
    with sidebar:
        st.header(f"Filtriranje pretrage za tabelu {odabir_tabele}")
        
        
        donja_datum = None
        gornja_datum = None
        if 'donja_datum' not in st.session_state:
            st.session_state.donja_datum = donja_datum
        if 'gornja_datum' not in st.session_state:
            st.session_state.gornja_datum = gornja_datum
        query_part_datum = ""
        with st.form("_datum", clear_on_submit=False):
            st.write("Unesite raspon datuma")
            donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
            gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
            if st.form_submit_button("Potvrda"):
                donja_datum = donja_datum
                gornja_datum = gornja_datum
                #if 'donja_datum' not in st.session_state:
                st.session_state.donja_datum = donja_datum
                #if 'gornja_datum' not in st.session_state:
                st.session_state.gornja_datum = gornja_datum
                #st.session_state.donja_datum = donja_datum
                #st.session_state.gornja_datum = gornja_datum
        if st.session_state.donja_datum != None and st.session_state.gornja_datum != None:
            query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum}" AND "{st.session_state.gornja_datum}"'
        rest_of_query = rest_of_query + " " + query_part_datum
    
        
        konacan_naziv = ""
        if 'naziv_klijenta' not in st.session_state:
            st.session_state.naziv_klijenta = konacan_naziv
        query_part_naziv = ""
        with st.form("_naziv_klijenta", clear_on_submit=False):
            unos_naziv_klijenta = st.text_input("Naziv (ime) klijenta", "")
            if st.form_submit_button("Potvrda"):
                konacan_naziv = unos_naziv_klijenta
                #if 'naziv_klijenta' not in st.session_state:
                st.session_state.naziv_klijenta = konacan_naziv
                #st.session_state.naziv_klijenta = konacan_naziv
        if st.session_state.naziv_klijenta != "":
            query_part_naziv = f'AND `Naziv(ime) klijenta` = "{st.session_state.naziv_klijenta}"'
        rest_of_query = rest_of_query + " " + query_part_naziv


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
                #if 'donja_kilometraza' not in st.session_state:
                st.session_state.donja_kilometraza = donja_kilometraza
                #if 'gornja_kilometraza' not in st.session_state:
                st.session_state.gornja_kilometraza = gornja_kilometraza
                #st.session_state.donja_kilometraza = donja_kilometraza
                #st.session_state.gornja_kilometraza = gornja_kilometraza
        if st.session_state.donja_kilometraza != None and st.session_state.gornja_kilometraza != None:
            query_part_kilometraza = f'AND Kilometraža BETWEEN {st.session_state.donja_kilometraza} AND {st.session_state.gornja_kilometraza}'
        rest_of_query = rest_of_query + " " + query_part_kilometraza
        
        
        startno_mjesto_konacno = ""
        if 'startno_mjesto' not in st.session_state:
            st.session_state.startno_mjesto = startno_mjesto_konacno
        query_part_start = ""
        with st.form("_startno_mjesto", clear_on_submit=False):
            startno_mjesto = st.text_input("Startno mjesto", "")
            if st.form_submit_button("Potvrda"):
                startno_mjesto_konacno = startno_mjesto
                #if 'startno_mjesto' not in st.session_state:
                st.session_state.startno_mjesto = startno_mjesto_konacno
                #st.session_state.startno_mjesto = startno_mjesto_konacno
        if st.session_state.startno_mjesto != "":
            query_part_start = f'AND `Startno mjesto` = "{st.session_state.startno_mjesto}"'
        rest_of_query = rest_of_query + " " + query_part_start

        
        ciljno_mjesto_konacno = ""
        if 'ciljno_mjesto' not in st.session_state:
            st.session_state.ciljno_mjesto = ciljno_mjesto_konacno
        query_part_cilj = ""
        with st.form("_ciljno_mjesto", clear_on_submit=False):
            ciljno_mjesto = st.text_input("Ciljno mjesto", "")
            if st.form_submit_button("Potvrda"):
                ciljno_mjesto_konacno = ciljno_mjesto
                #if 'ciljno_mjesto' not in st.session_state:
                st.session_state.ciljno_mjesto = ciljno_mjesto_konacno
                #st.session_state.ciljno_mjesto = ciljno_mjesto_konacno
        if st.session_state.ciljno_mjesto != "":
            query_part_cilj = f'AND `Ciljno mjesto` = "{st.session_state.ciljno_mjesto}"'
        rest_of_query = rest_of_query + " " + query_part_cilj


        lokacija_konacno = ""
        if 'lokacija' not in st.session_state:
            st.session_state.lokacija = lokacija_konacno
        query_part_lokacija = ""
        with st.form("_lokacija", clear_on_submit=False):
            lokacija = st.selectbox(label="Lokacija", options=("BiH", "Inostranstvo"))
            if st.form_submit_button("Potvrda"):
                lokacija_konacno = lokacija
                #if 'lokacija' not in st.session_state:
                st.session_state.lokacija = lokacija_konacno
                #st.session_state.lokacija = lokacija_konacno
        if st.session_state.lokacija != "":
            query_part_lokacija = f'AND Lokacija = "{st.session_state.lokacija}"'
        rest_of_query = rest_of_query + " " + query_part_lokacija


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
                #if 'donja_iznos_gotovina' not in st.session_state:
                st.session_state.donja_iznos_gotovina = donja_iznos_gotovina
                #if 'gornja_iznos_gotovina' not in st.session_state:
                st.session_state.gornja_iznos_gotovina = gornja_iznos_gotovina
                #st.session_state.donja_iznos_gotovina = donja_iznos_gotovina
                #st.session_state.gornja_iznos_gotovina = gornja_iznos_gotovina
        if st.session_state.donja_iznos_gotovina != None and st.session_state.gornja_iznos_gotovina != None:
            query_part_iznos_gotovina = f'AND `Iznos gotovina (KM)` BETWEEN {st.session_state.donja_iznos_gotovina} AND {st.session_state.gornja_iznos_gotovina}'
        rest_of_query = rest_of_query + " " + query_part_iznos_gotovina


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
                #if 'donja_iznos_ziralno' not in st.session_state:
                st.session_state.donja_iznos_ziralno = donja_iznos_ziralno
                #if 'gornja_iznos_ziralno' not in st.session_state:
                st.session_state.gornja_iznos_ziralno = gornja_iznos_ziralno
                #st.session_state.donja_iznos_ziralno = donja_iznos_ziralno
                #st.session_state.gornja_iznos_ziralno = gornja_iznos_ziralno
        if st.session_state.donja_iznos_ziralno != None and st.session_state.gornja_iznos_ziralno != None:
            query_part_iznos_ziralno = f'AND `Iznos žiralno (KM)` BETWEEN {st.session_state.donja_iznos_ziralno} AND {st.session_state.gornja_iznos_ziralno}'
        rest_of_query = rest_of_query + " " + query_part_iznos_ziralno


        placeno_konacno = ""
        if 'placeno' not in st.session_state:
            st.session_state.placeno = placeno_konacno
        query_part_placeno = ""
        with st.form("_placeno", clear_on_submit=False):
            placeno = st.selectbox(label="Plaćeno", options=("DA", "NE", "GRATIS"))
            if st.form_submit_button("Potvrda"):
                placeno_konacno = placeno
                #if 'placeno' not in st.session_state:
                st.session_state.placeno = placeno_konacno
                #st.session_state.placeno = placeno_konacno
        if st.session_state.placeno != "":
            query_part_placeno = f'AND Plaćeno = "{st.session_state.placeno}"'
        rest_of_query = rest_of_query + " " + query_part_placeno


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
                #if 'donja_op_trosak' not in st.session_state:
                st.session_state.donja_op_trosak = donja_op_trosak
                #if 'gornja_op_trosak' not in st.session_state:
                st.session_state.gornja_op_trosak = gornja_op_trosak
                #st.session_state.donja_op_trosak = donja_op_trosak
                #st.session_state.gornja_op_trosak = gornja_op_trosak
        if st.session_state.donja_op_trosak != None and st.session_state.gornja_op_trosak != None:
            query_part_op_trosak = f'AND `Operativni trošak (KM)` BETWEEN {st.session_state.donja_op_trosak} AND {st.session_state.gornja_op_trosak}'
        rest_of_query = rest_of_query + " " + query_part_op_trosak


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
                #if 'donja_neto_zarada' not in st.session_state:
                st.session_state.donja_neto_zarada = donja_neto_zarada
                #if 'gornja_neto_zarada' not in st.session_state:
                st.session_state.gornja_neto_zarada = gornja_neto_zarada
                #st.session_state.donja_neto_zarada = donja_neto_zarada
                #st.session_state.gornja_neto_zarada = gornja_neto_zarada
        if st.session_state.donja_neto_zarada != None and st.session_state.donja_neto_zarada != None:
            query_part_neto_zarada = f'AND `Neto zarada (KM)` BETWEEN {st.session_state.donja_neto_zarada} AND {st.session_state.gornja_neto_zarada}'
        rest_of_query = rest_of_query + " " + query_part_neto_zarada


        komentar_konacno = ""
        if 'komentar' not in st.session_state:
            st.session_state.komentar = komentar_konacno
        query_part_komentar = ""
        with st.form("_komentar", clear_on_submit=False):
            komentar = st.text_input("Komentar/Napomena", "")
            if st.form_submit_button("Potvrda"):
                komentar_konacno = komentar
                #if 'komentar' not in st.session_state:
                st.session_state.komentar = komentar_konacno
                #st.session_state.komentar = komentar_konacno
        if st.session_state.komentar != "":
            query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar}"'
        rest_of_query = rest_of_query + " " + query_part_komentar



    if rest_of_query.strip() != "":
        rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
        query = f'SELECT * from {odabir_tabele} WHERE {rest_of_query};'
        with administracija_engine.connect() as administracija_connection:
            df = pd.read_sql(query, administracija_connection)
        #df = pd.DataFrame(connection.query(query, ttl=600))
    # df = pd.DataFrame(connection.query(f"""SELECT * from {odabir_tabele} WHERE Datum = "{datum}" 
    #                                                                     AND `Naziv(ime) klijenta` = {konacan_naziv}
    #                                                                     AND Kilometraža BETWEEN {donja_kilometraza} AND {gornja_kilometraza}
    #                                                                     AND `Startno mjesto` = {startno_mjesto};'
    #                                     """,
    #                                     ttl=600))

    # unos_lokacija = st.selectbox(label="Lokacija", options=("BiH", "Inostranstvo"))
    # unos_placeno = st.selectbox(label="Plaćeno", options=("DA", "NE"))


#df = connection.query(f'SELECT * from {odabir_tabele} WHERE Datum = "{datum}";', ttl=600)
# df = connection.query(f'SELECT * from {odabir_tabele};', ttl=600)

# df = pd.DataFrame(df)
#df.style.format('{:.0f}').set_table_styles([cell_hover, index_names, headers])

#st.header("Pregled podataka")
st.subheader(f"{odabir_tabele}")
tabela = st.dataframe(data=df, use_container_width=True, hide_index=True)

imena_kolona_query = f"""
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = '{os.getenv("DB_DATABASE")}'
    AND TABLE_NAME = '{odabir_tabele}';
"""
# imena_kolona = connection.query(imena_kolona_query).values
# lista_kolona = [imena_kolona[i][0] for i in range(len(imena_kolona))]
#print(lista_kolona)

all_queries=[]
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

