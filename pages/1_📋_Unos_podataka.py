import streamlit as st
import sys
import os
import pandas as pd
import datetime
import mariadb
import sqlalchemy
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.getcwd()))
from unos_u_bazu import unos_u_bazu
from mitosheet.streamlit.v1 import spreadsheet

load_dotenv()

st.set_page_config(
    page_title="Unos podataka",
    page_icon="📋",
    layout="wide"
)

def izracunaj_gorivo(litara, cijena):
    return float(litara*cijena)

datum = st.column_config.DateColumn(
            format="DD.MM.YYYY",
            default=datetime.date.today(),
            help="Izaberite datum",
            required=True
        )

gorivo_litara = st.column_config.NumberColumn(
            help="Utrošak goriva za turu",
            default=float(0),
            min_value=float(0),
            format="%.2f l",
        )
gorivo_cijena = st.column_config.NumberColumn(
            help="Aktuelna cijena goriva",
            default=float(0),
            min_value=float(0),
            format="%.2f KM",
        )
gorivo_iznos = st.column_config.NumberColumn(
            help="Cijena utrošenog goriva za turu",
            default=float(0),
            min_value=float(0),
            format="%.2f KM",
        )
naziv_klijenta = st.column_config.TextColumn(
            help="Ime fizičkog lica ili naziv pravnog subjekta",
            default="",
        )
startno_mjesto = st.column_config.TextColumn(
            help="Početna destinacija",
            default=""
        )
ciljno_mjesto = st.column_config.TextColumn(
            help="Krajnja destinacija",
            default=""
        )
kilometraza = st.column_config.NumberColumn(
            help="Dužina puta od startnog do ciljnog mjesta",
            default=float(0),
            min_value=float(0),
            format="%.2f km"
        )
iznos = st.column_config.NumberColumn(
            help="Iznos odabranog troška",
            default=float(0),
            min_value=float(0),
            format="%.2f KM"
        )
nacin_placanja = st.column_config.SelectboxColumn(
            help="Gotovina, žiralno ili kartica",
            default="Gotovina",
            options=[
                "Gotovina",
                "Žiralno",
                "Kartica"
            ],
            required=True
        )
# naplaceno = st.column_config.CheckboxColumn(
#            help="Da li je usluga naplaćena?",
#            default=False
#         )

naplaceno = st.column_config.SelectboxColumn(
           help="Da li je usluga naplaćena?",
           default="DA",
           options=[
               "DA",
               "NE",
               "GRATIS"
           ],
           required=True
        )
operativni_trosak = st.column_config.NumberColumn(
            help="Iznos operativnog troška",
            default=float(0),
            min_value=float(0),
            format="%.2f KM"
        )
neto_zarada = st.column_config.NumberColumn(
            help="Iznos neto zarade",
            default=float(0),
            format="%.2f KM"
        )
komentar = st.column_config.TextColumn(
            help="Komentar ili napomena",
            default=""
        )
benz_pumpa = st.column_config.TextColumn(
            help="Naziv benzinske pumpe",
            default=""
)

@st.cache_resource
def mariadb_connection():

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
    connection = mariadb.connect(**conn_params)
    return connection

@st.cache_resource
def experimental_connection():

    # Establish a connection
    connection = st.experimental_connection('mariadb', type='sql')
    return connection

@st.cache_resource
def sqlalchemy_connection():

    # sqlalchemy engine and connection
    engine = sqlalchemy.create_engine(
    f"mariadb+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_UNOS')}"
    )
    connection = engine.raw_connection()
    return connection

connection = sqlalchemy_connection()
cursor = connection.cursor()

st.title('Administracija finansija')
st.write("---")


# if 'df_usluga_dom_ino' not in st.session_state:
#     st.session_state.df_usluga_dom_ino = pd.DataFrame(
#             [
#                 {
#                 "Datum": datetime.date.today(), 
#                 "Trošak(opis)": "Usluga domaća", 
#                 "Naziv(ime) klijenta": "", 
#                 "Startno mjesto": "",
#                 "Ciljno mjesto": "", 
#                 "Kilometraža": float(0), 
#                 "Iznos": float(0), 
#                 "Način plaćanja": "Gotovina",
#                 "Naplaćeno?": False, 
#                 "Operativni trošak": float(0), 
#                 "Neto zarada": float(0),
#                 "Komentar/Napomena": ""}
#             ]
#         )
#     st.session_state.edited_df_usluga_dom_ino = st.session_state.df_usluga_dom_ino.copy()
# else:
#     st.session_state.edited_df_usluga_dom_ino = pd.read_sql('SELECT * FROM Unos.Usluga_DOM_INO', connection_1)

# if 'df_usluga_pro_bono' not in st.session_state:
#     st.session_state.df_usluga_pro_bono = pd.DataFrame(
#             [
#                 {
#                 "Datum": datetime.date.today(), 
#                 "Trošak(opis)": "Usluga probono (donacija)",
#                 "Naziv(ime) klijenta": "", 
#                 "Startno mjesto": "",
#                 "Ciljno mjesto": "",
#                 "Lokacija": "BiH", 
#                 "Kilometraža": float(0), 
#                 "Iznos": "Gratis", 
#                 "Operativni trošak": float(0), 
#                 "Neto zarada": float(0),
#                 "Komentar/Napomena": ""}
#             ]
#         )
#     st.session_state.edited_df_usluga_pro_bono = st.session_state.df_usluga_pro_bono.copy()
# else:
#     st.session_state.edited_df_usluga_pro_bono = pd.read_sql('SELECT * FROM Unos.Usluga_PRO_BONO', connection_1)
df_usluga_init = st.session_state.df_usluga = pd.DataFrame(
            [
                {
                "Datum": datetime.date.today(), 
                "Trošak(opis)": "Usluga naplativa", 
                "Naziv(ime) klijenta": "",
                "Lokacija": "BiH", 
                "Startno mjesto": "",
                "Ciljno mjesto": "", 
                "Kilometraža": float(0), 
                "Iznos": float(0), 
                "Način plaćanja": "Gotovina",
                "Naplaćeno?": "DA", 
                "Operativni trošak": float(0), 
                "Neto zarada": float(0),
                "Komentar/Napomena": ""}
            ]
        )
if 'df_usluga' not in st.session_state:
    st.session_state.df_usluga = df_usluga_init
    st.session_state.edited_df_usluga = st.session_state.df_usluga.copy()
# else:
#     st.session_state.df_usluga = pd.read_sql('SELECT * FROM Unos.Usluga', connection)
#     st.session_state.edited_df_usluga = pd.read_sql('SELECT * FROM Unos.Usluga', connection)


df_gorivo_init = pd.DataFrame(
            [
                {
                "Datum": datetime.date.today(), 
                "Trošak(opis)": "Gorivo",
                "Nasuta količina": float(0), 
                "Cijena goriva": float(0), 
                "Iznos": float(0), 
                "Način plaćanja": "Gotovina", 
                "Naziv benzinske pumpe": "",
                "Komentar/Napomena": ""}
            ]
        )
if 'df_gorivo' not in st.session_state:
    st.session_state.df_gorivo = df_gorivo_init
    st.session_state.edited_df_gorivo = st.session_state.df_gorivo.copy()
# else:
#     #st.session_state.df_gorivo = pd.read_sql('SELECT * FROM Unos.Gorivo', connection)
#     st.session_state.edited_df_gorivo = pd.read_sql('SELECT * FROM Unos.Gorivo', connection)


df_troskovi_odrzavanja_init = pd.DataFrame(
            [
                {
                "Datum": datetime.date.today(), 
                "Trošak(opis)": "Servis",
                "Dodatni opis (opciono)": "",
                "Kilometraža": float(0),
                "Iznos": float(0),
                "Način plaćanja": "Gotovina", 
                "Komentar/Napomena": ""}
            ]
        )
if 'df_troskovi_odrzavanja' not in st.session_state:
    st.session_state.df_troskovi_odrzavanja = df_troskovi_odrzavanja_init
    st.session_state.edited_df_troskovi_odrzavanja = st.session_state.df_troskovi_odrzavanja.copy()
# else:
#     #st.session_state.df_troskovi_odrzavanja = pd.read_sql('SELECT * FROM Unos.Troskovi_odrzavanja', connection)
#     st.session_state.edited_df_troskovi_odrzavanja = pd.read_sql('SELECT * FROM Unos.Troskovi_odrzavanja', connection)

df_terenski_troskovi_init = pd.DataFrame(
            [
                {
                "Datum": datetime.date.today(), 
                "Trošak(opis)": "Putarina",
                "Dodatni opis (opciono)": "",
                "Iznos": float(0),
                "Način plaćanja": "Gotovina", 
                "Komentar/Napomena": ""}
            ]
        )
if 'df_terenski_troskovi' not in st.session_state:
    st.session_state.df_terenski_troskovi = df_terenski_troskovi_init
    st.session_state.edited_df_terenski_troskovi = st.session_state.df_terenski_troskovi.copy()
# else:
#     #st.session_state.df_terenski_troskovi = pd.read_sql('SELECT * FROM Unos.Terenski_troskovi', connection)
#     st.session_state.edited_df_terenski_troskovi = pd.read_sql('SELECT * FROM Unos.Terenski_troskovi', connection)

def save_edits():
    st.session_state.df_usluga = st.session_state.edited_df_usluga.copy()
    st.session_state.df_gorivo = st.session_state.edited_df_gorivo.copy()
    st.session_state.df_troskovi_odrzavanja = st.session_state.edited_df_troskovi_odrzavanja.copy()
    st.session_state.df_terenski_troskovi = st.session_state.edited_df_terenski_troskovi.copy()

df_usluga = st.session_state.df_usluga
df_gorivo = st.session_state.df_gorivo
df_troskovi_odrzavanja = st.session_state.df_troskovi_odrzavanja
df_terenski_troskovi = st.session_state.df_terenski_troskovi

def call_mitosheet(vrsta_troska):

    if vrsta_troska == "Usluga":
        st.session_state.edited_df_usluga = spreadsheet(df_usluga)


#@st.cache_data
def call_data_editor(vrsta_troska):
    
    ############### USLUGA DOMACA ILI USLUGA INOSTRANSTVO ###############
    if vrsta_troska == "Usluga":
        df = df_usluga
        st.session_state.edited_df_usluga = st.data_editor(
        df,
        column_config={
            "Datum": datum,
            "Trošak(opis)": st.column_config.SelectboxColumn(help="Vrsta troška", 
                                                             width="medium", 
                                                             default="Usluga naplativa",
                                                             options=["Usluga naplativa", "Usluga pro-bono"],
                                                             required=True), 
            "Naziv(ime) klijenta": naziv_klijenta,
            "Lokacija": st.column_config.SelectboxColumn(help="Domaća ili inostranstvo",
                                                         width="medium",
                                                         default="BiH",
                                                         options=["BiH", "Inostranstvo"],
                                                         required=True),
            "Startno mjesto": startno_mjesto,
            "Ciljno mjesto": ciljno_mjesto,
            "Kilometraža": kilometraza,
            "Iznos": iznos,
            "Način plaćanja": st.column_config.SelectboxColumn(help="Gotovina, žiralno, ili gratis",
                                                               default="Gotovina",
                                                               options=["Gotovina","Žiralno", "Gratis"],
                                                               required=True),
            "Naplaćeno?": naplaceno,
            "Operativni trošak": operativni_trosak,
            "Neto zarada": neto_zarada,
            "Komentar/Napomena": komentar
        },
        num_rows="dynamic",
        use_container_width=True,
    )
        return st.session_state.edited_df_usluga

    ############### DONACIJA (USLUGA PROBONO) ###############   
    # elif vrsta_troska == "Usluga probono (donacija)":
    #     df = df_usluga_pro_bono
    #     st.session_state.edited_df_usluga_pro_bono = st.data_editor(
    #     df,
    #     column_config={
    #         "Datum": datum,
    #         "Trošak(opis)": st.column_config.TextColumn(help="Vrsta troška", width="medium", default=vrsta_troska, disabled=True), 
    #         "Naziv(ime) klijenta": naziv_klijenta,
    #         "Startno mjesto": startno_mjesto,
    #         "Ciljno mjesto": ciljno_mjesto,
    #         "Lokacija": st.column_config.SelectboxColumn(help="BiH ili inostranstvo", width="medium", default="BiH", 
    #                                                      options=["BiH", "Inostranstvo"], required=True),
    #         "Kilometraža": kilometraza,
    #         "Iznos": st.column_config.TextColumn(help="Iznos odabranog troška", width="medium", default="Gratis", disabled=True),
    #         "Operativni trošak": operativni_trosak,
    #         "Neto zarada": neto_zarada,
    #         "Komentar/Napomena": komentar
    #     },
    #     num_rows="dynamic",
    #     use_container_width=True,
    # )
    #     return st.session_state.edited_df_usluga_pro_bono

    ############### GORIVO ###############    
    elif vrsta_troska == "Gorivo":
        df = df_gorivo
        st.session_state.edited_df_gorivo = st.data_editor(
        df,
        column_config={
            "Datum": datum,
            "Trošak(opis)": st.column_config.TextColumn(help="Vrsta troška", default=vrsta_troska, disabled=True), 
            "Nasuta količina": gorivo_litara,
            "Cijena goriva": gorivo_cijena,
            "Iznos": gorivo_iznos,
            "Način plaćanja": nacin_placanja,
            "Naziv benzinske pumpe": benz_pumpa,
            "Komentar/Napomena": komentar
        },
        num_rows="dynamic",
        use_container_width=True,
    )
        return st.session_state.edited_df_gorivo

    ############### TROSKOVI ODRZAVANJA ###############
    elif vrsta_troska == "Troškovi održavanja (servis, registracija, gume)":
        df = df_troskovi_odrzavanja
        st.session_state.edited_df_troskovi_odrzavanja = st.data_editor(
        df,
        column_config={
            "Datum": datum,
            "Trošak(opis)": st.column_config.SelectboxColumn(help="Vrsta troška", 
                                                             width="medium", 
                                                             default="Servis",
                                                             options=["Servis",
                                                                      "Registracija",
                                                                      "Gume"],
                                                             required=True),
            "Dodatni opis (opciono)": st.column_config.TextColumn(help="Dodatni opis troška", default=""),
            "Kilometraža": st.column_config.NumberColumn(help="Kilometraža vozila",
                                                         default=float(0),
                                                         required=True,
                                                         min_value=float(0),
                                                         format="%.2f km"),
            "Iznos": iznos,
            "Način plaćanja": nacin_placanja,
            "Komentar/Napomena": komentar
        },
        num_rows="dynamic",
        use_container_width=True,
    )
        return st.session_state.edited_df_troskovi_odrzavanja

    ############### TERENSKI TROSKOVI ###############    
    elif vrsta_troska == "Terenski troškovi (osiguranje, saobraćajne kazne...)":
        df = df_terenski_troskovi
        st.session_state.edited_df_terenski_troskovi = st.data_editor(
        df,
        column_config={
            "Datum": datum,
            "Trošak(opis)": st.column_config.SelectboxColumn(help="Vrsta troška", 
                                                             width="medium", 
                                                             default="Putarina",
                                                             options=["Putarina",
                                                                      "Terminal",
                                                                      "Mostarina",
                                                                      "Osiguranje",
                                                                      "Saobraćajne kazne",
                                                                      "Telefon",
                                                                      "Privatno",
                                                                      "Pranje vozila",
                                                                      "Ostalo"],
                                                             required=True),
            "Dodatni opis (opciono)": st.column_config.TextColumn(help="Dodatni opis troška", default=""), 
            "Iznos": iznos,
            "Način plaćanja": nacin_placanja,
            "Komentar/Napomena": komentar
        },
        num_rows="dynamic",
        use_container_width=True,
    )

        return st.session_state.edited_df_terenski_troskovi


vrsta_troska = st.selectbox("Odaberite vrstu troška", 
                            options=[
                                    "Usluga",
                                    "Gorivo",
                                    "Troškovi održavanja (servis, registracija, gume)",
                                    "Terenski troškovi (osiguranje, saobraćajne kazne...)"],
                            on_change=save_edits)
#with st.container():

st.write("Unesite podatke u tabelu")

dfs, _ = spreadsheet(df_usluga,df_gorivo,df_troskovi_odrzavanja,df_terenski_troskovi)
df = list(dfs)[0]
    #df = call_data_editor(vrsta_troska)
    #print(df)
    #submitted = st.button("Potvrda", help="Potvrdite unos podataka u bazu")
    #brojac = 0
    # if submitted:
    #     unos_u_bazu(vrsta_troska, cursor, connection, df)
        #brojac += 1



