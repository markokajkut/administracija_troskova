import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
from weather import get_weather_data
from report import generate_report, delete_pdf_after_download

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Logo prikaz
def img():
    _, _, _, _, _, _, _, _, _, col10 = st.columns(10)
    with col10:
        st.image(f"{parent_dir}/app/templates/logo.jpg")

# Ciscenje st.session_state varijabli
def clear_cache():
    keys = list(st.session_state.keys())
    keys.remove("authentication_status")
    for key in keys:
        st.session_state.pop(key)

# Pocetna stranica, prije login-a
def landing_page():
    
    img()
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
    
# SQL engine
@st.cache_resource
def engine_sqlalchemy(table):

    # sqlalchemy engine
    engine = create_engine(
    f"mariadb+mariadbconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv(table)}",
    poolclass=QueuePool, pool_size=5, max_overflow=10)
    
    return engine

# Provjera duzine dataframe-ova
def check_df_len(unos_engine):

    with unos_engine.connect() as unos_connection:
        len_df_usluga = len(pd.read_sql('SELECT * FROM Usluga', unos_connection))
        len_df_gorivo = len(pd.read_sql('SELECT * FROM Gorivo', unos_connection))
        len_df_troskovi_odrzavanja = len(pd.read_sql('SELECT * FROM Troskovi_odrzavanja', unos_connection))
        len_df_terenski_troskovi = len(pd.read_sql('SELECT * FROM Terenski_troskovi', unos_connection))
       
        return len_df_usluga, len_df_gorivo, len_df_troskovi_odrzavanja, len_df_terenski_troskovi
    
# Forma za kreiranje izvjestaja
def report_form():
    administracija_engine = engine_sqlalchemy("DB_ADMINISTRACIJA")

    # Skidanje izvjestaja
    def on_click_download():
        st.session_state.report_generated_status = False
    
    pdf_filename = None
    _, _, _, _, _, _, _, col8 = st.columns(8)
    with col8:
        with st.form("izvjestaj", clear_on_submit=False):
            st.write("Generiši izvještaj")
            donja_datum = st.date_input("Od", format="DD.MM.YYYY")
            gornja_datum = st.date_input("Do", format="DD.MM.YYYY")
            if st.form_submit_button("Potvrda"):
                try:
                    with st.spinner('Generisanje...'):
                        pdf_filename = generate_report(donja_datum, gornja_datum, administracija_engine)
                        if pdf_filename == "empty":
                            raise Exception("Ne postoje potpuni podaci")
                        elif pdf_filename == "datum greska":
                            raise Exception("Datumi nisu validni.")
                        else:
                            st.session_state.report_generated_status = True
                            st.success('Izvještaj generisan!')
                except Exception as e:
                   st.error(f"Greška pri generisanju. Pokušajte ponovo. {e}")
        if st.session_state.report_generated_status == True:
                    with open(pdf_filename, "rb") as file:
                        st.download_button(label="Preuzmite izvještaj",
                                                       data=file,
                                                       file_name=pdf_filename.split("/")[-1],
                                                       on_click=on_click_download
                                                       )
                        delete_pdf_after_download(pdf_filename)
