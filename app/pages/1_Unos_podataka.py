import os
import datetime
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from unos_u_bazu import unos_u_bazu_administracija, unos_u_bazu_unos
from app_skelet_unos import call_data_editor
from helpers import landing_page, engine_sqlalchemy, check_df_len, img

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

load_dotenv()

footer = """<style>
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
<p>By <i>Marko Kajkut</i>, <i>markokajkut1@gmail.com</i> <a style='display: block; text-align: center;'</p>
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

# Inicijalizacija engine-a za rad sa bazom
unos_engine = engine_sqlalchemy("DB_UNOS")
administracija_engine = engine_sqlalchemy("DB_ADMINISTRACIJA")

# Provjera duzine dataframe-a
len_df_usluga, len_df_gorivo, len_df_troskovi_odrzavanja, len_df_terenski_troskovi = check_df_len(unos_engine)

# Inicijalizacija "session_state" varijabli za dataframe-ove za unos
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

    img()
    
    st.title('Administracija finansija')
    st.subheader("Unos podataka")
    st.write("---")

    with unos_engine.connect() as unos_connection:
        # Inicijalizacija "Usluga" tabele ili ucitavanje iz baze ako vec postoje podaci
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
                        "Kilometraža na satu START": float(0),
                        "Kilometraža na satu KRAJ": float(0), 
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

        # Inicijalizacija "Gorivo" tabele ili ucitavanje iz baze ako vec postoje podaci
        df_gorivo_init = None
        if len_df_gorivo == 0:
            df_gorivo_init = pd.DataFrame(
                    [
                        {
                        "Datum": datetime.date.today(), 
                        "Trošak(opis)": "Gorivo",
                        "Kilometraža na satu": float(0),
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

        # Inicijalizacija "Troskovi_odrzavanja" tabele ili ucitavanje iz baze ako vec postoje podaci
        df_troskovi_odrzavanja_init = None
        if len_df_troskovi_odrzavanja == 0:
            df_troskovi_odrzavanja_init = pd.DataFrame(
                    [
                        {
                        "Datum": datetime.date.today(), 
                        "Trošak(opis)": "Servis",
                        "Kilometraža na satu": float(0),
                        "Iznos": float(0),
                        "Način plaćanja": "Gotovina", 
                        "Komentar/Napomena": ""}
                    ]
                )
        else:
            df_troskovi_odrzavanja_init = pd.read_sql('SELECT * FROM Troskovi_odrzavanja', unos_connection)
        st.session_state.df_troskovi_odrzavanja = df_troskovi_odrzavanja_init
        st.session_state.edited_df_troskovi_odrzavanja = st.session_state.df_troskovi_odrzavanja.copy()

        # Inicijalizacija "Terenski_troskovi" tabele ili ucitavanje iz baze ako vec postoje podaci
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

    # Cuvanje izmjena u data editoru
    def save_edits():
        st.session_state.df_usluga = st.session_state.edited_df_usluga.copy()
        st.session_state.df_gorivo = st.session_state.edited_df_gorivo.copy()
        st.session_state.df_troskovi_odrzavanja = st.session_state.edited_df_troskovi_odrzavanja.copy()
        st.session_state.df_terenski_troskovi = st.session_state.edited_df_terenski_troskovi.copy()

    # Trenutne vrijednosti dataframe-ova
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
        # Unosenje podataka u data editor i cuvanje stanja data editora azuriranim
        df = call_data_editor(vrsta_troska, df_usluga, df_gorivo, df_troskovi_odrzavanja, df_terenski_troskovi)
        submitted = st.button("Potvrda", help="Potvrdite unos podataka u bazu")
        if submitted:
            try:
                unos_u_bazu_administracija(vrsta_troska, administracija_engine, df)
                unos_u_bazu_unos(unos_engine, df, vrsta_troska)
            except:
                st.error("Greška prilikom unosa podataka u bazu. Provjerite unešene vrijednosti.")
            
    # Upozorenja za "Usluga" data editor, radi pravilnog unosenja u bazu
    if vrsta_troska == "Usluga":
        with st.sidebar:
            st.warning("Prilikom biranja 'Usluga pro-bono' u koloni 'Trošak(opis)', potrebno je podesiti kolonu 'Način plaćanja' na 'Gratis', kao i kolonu 'Naplaćeno?' na 'GRATIS', kako bi podaci bili pravilno unešeni u bazu.",
                    icon="⚠️")
            st.warning("Prilikom biranja 'Usluga naplativa' u koloni 'Trošak(opis)', kolona 'Način plaćanja' ne smije biti 'Gratis', a kolona 'Naplaćeno?' ne smije biti 'GRATIS', kako bi podaci bili pravilno unešeni u bazu.",
                    icon="⚠️")
    
# Nakon logovanja
if st.session_state["authentication_status"]:
    main()
# Prije logovanja
elif st.session_state["authentication_status"] == False or st.session_state["authentication_status"] == None:
    landing_page()
    with st.sidebar:
        st.warning('Niste prijavljeni.')

