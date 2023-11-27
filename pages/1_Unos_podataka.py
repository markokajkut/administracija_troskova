import streamlit as st
import sys
import os
import pandas as pd
import datetime
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
from weather import get_weather_data
sys.path.append(os.path.dirname(os.getcwd()))
from unos_u_bazu import unos_u_bazu_administracija, unos_u_bazu_unos
from app_skelet_unos import call_data_editor

load_dotenv()

footer="""<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: right;
left: -40px;
}
</style>
<div class="footer">
<p>By Marko Kajkut, markokajkut1@gmail.com <a style='display: block; text-align: center;'</p>
</div>
"""

st.set_page_config(
    page_title="Unos podataka",
    page_icon="📋",
    layout="wide"
)
st.markdown(footer,unsafe_allow_html=True)

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None

def landing_page():
    col1, col2, col3, col4, col5 = st.columns(5)
    datum, dan, vrijeme, sky, temp = get_weather_data()
    if datum.split(".")[1] in ["01", "02", "11", "12"]:
        st.snow()
    else:
        st.balloons()
    col1.metric("Datum", datum)
    col2.metric("Dan", dan)
    col3.metric("Vrijeme", vrijeme)
    col4.metric("Stanje vremena", sky)
    col5.metric("Temperatura", temp)


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
administracija_engine = administracija_sqlalchemy()[0]

def check_df_len():

    with unos_engine.connect() as unos_connection:
        len_df_usluga = len(pd.read_sql('SELECT * FROM Usluga', unos_connection))
        len_df_gorivo = len(pd.read_sql('SELECT * FROM Gorivo', unos_connection))
        len_df_troskovi_odrzavanja = len(pd.read_sql('SELECT * FROM Troskovi_odrzavanja', unos_connection))
        len_df_terenski_troskovi = len(pd.read_sql('SELECT * FROM Terenski_troskovi', unos_connection))
       
        return len_df_usluga, len_df_gorivo, len_df_troskovi_odrzavanja, len_df_terenski_troskovi

len_df_usluga, len_df_gorivo, len_df_troskovi_odrzavanja, len_df_terenski_troskovi = check_df_len()


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

def main():

    st.title('Administracija finansija')
    st.subheader("Unos podataka")
    st.write("---")
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
        st.session_state.df_usluga = df_usluga_init
        st.session_state.edited_df_usluga = st.session_state.df_usluga.copy()

        df_gorivo_init = None
        if len_df_gorivo == 0:
            df_gorivo_init = pd.DataFrame(
                    [
                        {
                        "Datum": datetime.date.today(), 
                        "Trošak(opis)": "Gorivo",
                        "Kilometraža": float(0),
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
        st.session_state.df_gorivo = df_gorivo_init
        st.session_state.edited_df_gorivo = st.session_state.df_gorivo.copy()

        df_troskovi_odrzavanja_init = None
        if len_df_troskovi_odrzavanja == 0:
            df_troskovi_odrzavanja_init = pd.DataFrame(
                    [
                        {
                        "Datum": datetime.date.today(), 
                        "Trošak(opis)": "Servis",
                        "Kilometraža": float(0),
                        "Iznos": float(0),
                        "Način plaćanja": "Gotovina", 
                        "Komentar/Napomena": ""}
                    ]
                )
        else:
            df_troskovi_odrzavanja_init = pd.read_sql('SELECT * FROM Troskovi_odrzavanja', unos_connection)
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
            unos_u_bazu_administracija(vrsta_troska, administracija_engine, df, df_troskovi_odrzavanja, df_terenski_troskovi)
            unos_u_bazu_unos(unos_engine, df, vrsta_troska)
    if vrsta_troska == "Usluga":
        st.warning("Prilikom biranja 'Usluga pro-bono' u koloni 'Trošak(opis)', potrebno je podesiti kolonu 'Način plaćanja' na 'Gratis', kao i kolonu 'Naplaćeno?' na 'GRATIS', kako bi podaci bili pravilno unešeni u bazu.",
                icon="⚠️")
        st.warning("Prilikom biranja 'Usluga naplativa' u koloni 'Trošak(opis)', kolona 'Način plaćanja' ne smije 'Gratis', a kolona 'Naplaćeno?' ne smije biti 'GRATIS', kako bi podaci bili pravilno unešeni u bazu.",
                icon="⚠️")
    


if st.session_state["authentication_status"]:
    main()
elif st.session_state["authentication_status"] == False or st.session_state["authentication_status"] == None:
    landing_page()
    with st.sidebar:
        st.warning('Niste prijavljeni.')

