import streamlit as st
import sys
import os
sys.path.append("C:\\Users\\PC\\Desktop\\Sinisa Borjanic")###

#sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))###
#print(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
import pandas as pd
import datetime
import mariadb
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.getcwd()))
from unos_u_bazu import unos_u_bazu_administracija, unos_u_bazu_unos
from mitosheet.streamlit.v1 import spreadsheet
from app_skelet_unos import call_data_editor
#sys.path.append("C:\Users\PC\Desktop\Sinisa Borjanic")###
load_dotenv()

st.set_page_config(
    page_title="Unos podataka",
    page_icon="📋",
    layout="wide"
)



@st.cache_resource()
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

@st.cache_resource()
def experimental_connection():

    # Establish a connection
    connection = st.experimental_connection('mariadb', type='sql')
    return connection

@st.cache_resource
def unos_sqlalchemy():

    # sqlalchemy engine and connection
    engine = create_engine(
    f"mariadb+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_UNOS')}",
    poolclass=QueuePool, pool_size=5, max_overflow=10)
    connection = engine.raw_connection()
    return engine, connection


@st.cache_resource
def administracija_sqlalchemy():

    # sqlalchemy engine and connection
    engine = create_engine(
    f"mariadb+mariadbconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}",
    poolclass=QueuePool, pool_size=5, max_overflow=10)
    connection = engine.raw_connection()
    return engine, connection

unos_engine = unos_sqlalchemy()[0]
#unos_connection = unos_sqlalchemy()[1]
#unos_cursor = unos_connection.cursor()

#experimental_connection = experimental_connection()

administracija_engine = administracija_sqlalchemy()[0]
#administracija_cursor = administracija_connection.cursor()

def check_df_len():

    with unos_engine.connect() as unos_connection:
        len_df_usluga = len(pd.read_sql('SELECT * FROM Usluga', unos_connection))
        len_df_gorivo = len(pd.read_sql('SELECT * FROM Gorivo', unos_connection))
        len_df_troskovi_odrzavanja = len(pd.read_sql('SELECT * FROM Troskovi_odrzavanja', unos_connection))
        len_df_terenski_troskovi = len(pd.read_sql('SELECT * FROM Terenski_troskovi', unos_connection))
       
        return len_df_usluga, len_df_gorivo, len_df_troskovi_odrzavanja, len_df_terenski_troskovi

len_df_usluga, len_df_gorivo, len_df_troskovi_odrzavanja, len_df_terenski_troskovi = check_df_len()
#st.write(len_df_usluga, len_df_gorivo, len_df_troskovi_odrzavanja, len_df_terenski_troskovi)
#print(len_df_usluga, len_df_gorivo, len_df_troskovi_odrzavanja, len_df_terenski_troskovi)
st.title('Administracija finansija')
st.subheader("Unos podataka")
st.write("---")

if 'df_usluga' not in st.session_state:
    st.session_state.df_usluga = None
    st.session_state.edited_df_usluga = None
if 'df_gorivo' not in st.session_state:
    st.session_state.df_gorivo = None
    st.session_state.edited_df_gorivo = None
if 'df_troskovi_odrzavanja' not in st.session_state:
    st.session_state.df_troskovi_odrzavanja = None
    st.session_state.edited_df_troskovi_odrzavanja = None
if 'df_terenski_troskovi' not in st.session_state:
    st.session_state.df_terenski_troskovi = None
    st.session_state.edited_df_terenski_troskovi = None

with unos_engine.connect() as unos_connection:
    df_usluga_init = None
    if len_df_usluga == 0:
        df_usluga_init = pd.DataFrame(
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
    else:
        df_usluga_init = pd.read_sql('SELECT * FROM Usluga', unos_connection)
    #if 'df_usluga' not in st.session_state:
    st.session_state.df_usluga = df_usluga_init
    st.session_state.edited_df_usluga = st.session_state.df_usluga.copy()

    df_gorivo_init = None
    if len_df_gorivo == 0:
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
    else:
        df_gorivo_init = pd.read_sql('SELECT * FROM Gorivo', unos_connection)
    #if 'df_gorivo' not in st.session_state:
    st.session_state.df_gorivo = df_gorivo_init
    st.session_state.edited_df_gorivo = st.session_state.df_gorivo.copy()

    df_troskovi_odrzavanja_init = None
    if len_df_troskovi_odrzavanja == 0:
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
    else:
        df_troskovi_odrzavanja_init = pd.read_sql('SELECT * FROM Troskovi_odrzavanja', unos_connection)
    #if 'df_troskovi_odrzavanja' not in st.session_state:
    st.session_state.df_troskovi_odrzavanja = df_troskovi_odrzavanja_init
    st.session_state.edited_df_troskovi_odrzavanja = st.session_state.df_troskovi_odrzavanja.copy()

    df_terenski_troskovi_init = None
    if len_df_terenski_troskovi == 0:
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
    else:
        df_terenski_troskovi_init = pd.read_sql('SELECT * FROM Terenski_troskovi', unos_connection)
    #if 'df_terenski_troskovi' not in st.session_state:
    st.session_state.df_terenski_troskovi = df_terenski_troskovi_init
    st.session_state.edited_df_terenski_troskovi = st.session_state.df_terenski_troskovi.copy()

def save_edits():
    st.session_state.df_usluga = st.session_state.edited_df_usluga.copy()
    st.session_state.df_gorivo = st.session_state.edited_df_gorivo.copy()
    st.session_state.df_troskovi_odrzavanja = st.session_state.edited_df_troskovi_odrzavanja.copy()
    st.session_state.df_terenski_troskovi = st.session_state.edited_df_terenski_troskovi.copy()

df_usluga = st.session_state.df_usluga
df_gorivo = st.session_state.df_gorivo
df_troskovi_odrzavanja = st.session_state.df_troskovi_odrzavanja
df_terenski_troskovi = st.session_state.df_terenski_troskovi


vrsta_troska = st.selectbox("Odaberite vrstu troška", 
                            options=[
                                    "Usluga",
                                    "Gorivo",
                                    "Troškovi održavanja (servis, registracija, gume)",
                                    "Terenski troškovi (osiguranje, saobraćajne kazne...)"],
                            on_change=save_edits)
with st.container():

    st.write("Unesite podatke u tabelu")

    df = call_data_editor(vrsta_troska, df_usluga, df_gorivo, df_troskovi_odrzavanja, df_terenski_troskovi)
    submitted = st.button("Potvrda", help="Potvrdite unos podataka u bazu")
    if submitted:
        #try:
        unos_u_bazu_administracija(vrsta_troska, administracija_engine, df, df_troskovi_odrzavanja, df_terenski_troskovi)
        unos_u_bazu_unos(unos_engine, df, vrsta_troska)
        # except:
        #     st.error('Došlo je do greške, provjerite unešene vrijednosti u tabeli.', icon="🚨")
        
        #st.experimental_rerun()

# administracija_cursor.close()
# administracija_connection.close()
# unos_connection.close()


