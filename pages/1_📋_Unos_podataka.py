import streamlit as st
import pandas as pd
import datetime
import os
import mariadb
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Unos podataka",
    page_icon="📋",
    layout="wide"
)

datum = st.column_config.DateColumn(
            format="DD.MM.YYYY",
            default=datetime.date.today(),
            help="Izaberite datum",
            required=True
        )
# trosak = st.column_config.SelectboxColumn(
#             help="Vrsta troška",
#             width="medium",
#             default="Usluga domaća",
#             required=True,
#             options=[
#                 "Usluga domaća",
#                 "Usluga inostranstvo",
#                 "Gorivo",
#                 "Servis",
#                 "Gume",
#                 "Osiguranje",
#                 "Registracija",
#                 "Saobraćajne kazne",
#                 "Terminal",
#                 "Putarina",
#                 "Mostarina",
#                 "Telefon",
#                 "Privatno",
#                 "Pranje vozila",
#                 "Donacija(usluga probono)"
#             ]
#         )
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
naplaceno = st.column_config.CheckboxColumn(
           help="Da li je usluga naplaćena?"
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

def izracunaj_gorivo(litara, cijena):
    return float(litara*cijena)

@st.cache_resource
def init_connection():
    
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
    connection_1 = mariadb.connect(**conn_params)
    connection = st.experimental_connection('mariadb', type='sql')
    return connection, connection_1

connection, connection_1 = init_connection()
cursor = connection_1.cursor()

st.title('Administracija finansija')
st.write("---")


if 'df_usluga_dom_ino' not in st.session_state:
    st.session_state.df_usluga_dom_ino = pd.DataFrame(
            [
                {
                "Datum": datetime.date.today(), 
                "Trošak(opis)": "Usluga domaća", 
                "Naziv(ime) klijenta": "", 
                "Startno mjesto": "",
                "Ciljno mjesto": "", 
                "Kilometraža": float(0), 
                "Iznos": float(0), 
                "Način plaćanja": "Gotovina",
                "Naplaćeno?": False, 
                "Operativni trošak": float(0), 
                "Neto zarada": float(0),
                "Komentar/Napomena": ""}
            ]
        )
    st.session_state.edited_df_usluga_dom_ino = st.session_state.df_usluga_dom_ino.copy()

if 'df_usluga_pro_bono' not in st.session_state:
    st.session_state.df_usluga_pro_bono = pd.DataFrame(
            [
                {
                "Datum": datetime.date.today(), 
                "Trošak(opis)": "Usluga probono (donacija)",
                "Naziv(ime) klijenta": "", 
                "Startno mjesto": "",
                "Ciljno mjesto": "",
                "Lokacija": "BiH", 
                "Kilometraža": float(0), 
                "Iznos": "Gratis", 
                "Operativni trošak": float(0), 
                "Neto zarada": float(0),
                "Komentar/Napomena": ""}
            ]
        )
    st.session_state.edited_df_usluga_pro_bono = st.session_state.df_usluga_pro_bono.copy()

if 'df_gorivo' not in st.session_state:
    st.session_state.df_gorivo = pd.DataFrame(
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
    st.session_state.edited_df_gorivo = st.session_state.df_gorivo.copy()

if 'df_troskovi_odrzavanja' not in st.session_state:
    st.session_state.df_troskovi_odrzavanja = pd.DataFrame(
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
    st.session_state.edited_df_troskovi_odrzavanja = st.session_state.df_troskovi_odrzavanja.copy()

if 'df_terenski_troskovi' not in st.session_state:
    st.session_state.df_terenski_troskovi = pd.DataFrame(
            [
                {
                "Datum": datetime.date.today(), 
                "Trošak(opis)": "Putarina",
                "Iznos": float(0),
                "Način plaćanja": "Gotovina", 
                "Komentar/Napomena": ""}
            ]
        )
    st.session_state.edited_df_terenski_troskovi = st.session_state.df_terenski_troskovi.copy()

def save_edits():
    st.session_state.df_usluga_dom_ino = st.session_state.edited_df_usluga_dom_ino.copy()
    st.session_state.df_usluga_pro_bono = st.session_state.edited_df_usluga_pro_bono.copy()
    st.session_state.df_gorivo = st.session_state.edited_df_gorivo.copy()
    st.session_state.df_troskovi_odrzavanja = st.session_state.edited_df_troskovi_odrzavanja.copy()
    st.session_state.df_terenski_troskovi = st.session_state.edited_df_terenski_troskovi.copy()

df_usluga_dom_ino = st.session_state.df_usluga_dom_ino
df_usluga_pro_bono = st.session_state.df_usluga_pro_bono
df_gorivo = st.session_state.df_gorivo
df_troskovi_odrzavanja = st.session_state.df_troskovi_odrzavanja
df_terenski_troskovi = st.session_state.df_terenski_troskovi


#@st.cache_data
def call_data_editor(vrsta_troska):
    
    ############### USLUGA DOMACA ILI USLUGA INOSTRANSTVO ###############
    if vrsta_troska == "Usluga (domaća, inostranstvo)":
        df = df_usluga_dom_ino
        st.session_state.edited_df_usluga_dom_ino = st.data_editor(
        df,
        column_config={
            "Datum": datum,
            "Trošak(opis)": st.column_config.SelectboxColumn(help="Vrsta troška", 
                                                             width="medium", 
                                                             default="Usluga domaća",
                                                             options=["Usluga domaća", "Usluga inostranstvo"],
                                                             required=True), 
            "Naziv(ime) klijenta": naziv_klijenta,
            "Startno mjesto": startno_mjesto,
            "Ciljno mjesto": ciljno_mjesto,
            "Kilometraža": kilometraza,
            "Iznos": iznos,
            "Način plaćanja": st.column_config.SelectboxColumn(help="Gotovina ili žiralno",
                                                               default="Gotovina",
                                                               options=["Gotovina","Žiralno"],
                                                               required=True),
            "Naplaćeno?": naplaceno,
            "Operativni trošak": operativni_trosak,
            "Neto zarada": neto_zarada,
            "Komentar/Napomena": komentar
        },
        num_rows="dynamic",
        use_container_width=True,
    )

    ############### DONACIJA (USLUGA PROBONO) ###############   
    elif vrsta_troska == "Usluga probono (donacija)":
        df = df_usluga_pro_bono
        st.session_state.edited_df_usluga_pro_bono = st.data_editor(
        df,
        column_config={
            "Datum": datum,
            "Trošak(opis)": st.column_config.TextColumn(help="Vrsta troška", width="medium", default=vrsta_troska, disabled=True), 
            "Naziv(ime) klijenta": naziv_klijenta,
            "Startno mjesto": startno_mjesto,
            "Ciljno mjesto": ciljno_mjesto,
            "Lokacija": st.column_config.SelectboxColumn(help="BiH ili inostranstvo", width="medium", default="BiH", 
                                                         options=["BiH", "Inostranstvo"], required=True),
            "Kilometraža": kilometraza,
            "Iznos": st.column_config.TextColumn(help="Iznos odabranog troška", width="medium", default="Gratis", disabled=True),
            "Operativni trošak": operativni_trosak,
            "Neto zarada": neto_zarada,
            "Komentar/Napomena": komentar
        },
        num_rows="dynamic",
        use_container_width=True,
    )

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
            "Iznos": iznos,
            "Način plaćanja": nacin_placanja,
            "Komentar/Napomena": komentar
        },
        num_rows="dynamic",
        use_container_width=True,
    )

    return df


vrsta_troska = st.selectbox("Odaberite vrstu troška", 
                            options=[
                                    "Usluga (domaća, inostranstvo)",
                                    "Usluga probono (donacija)",
                                    "Gorivo",
                                    "Troškovi održavanja (servis, registracija, gume)",
                                    "Terenski troškovi (osiguranje, saobraćajne kazne...)"],
                            on_change=save_edits)
with st.container():

    st.write("Unesite podatke u tabelu")
    df = call_data_editor(vrsta_troska)
    submitted = st.button("Potvrda", help="Potvrdite unos podataka u bazu")

    naplaceno_map = {True: 'DA', False: 'NE'}
    lokacija_map = {'Usluga domaća': 'BiH', 'Usluga inostranstvo': 'Inostranstvo'}
    if submitted:
        if vrsta_troska == "Usluga (domaća, inostranstvo)":
            for index, row in df.iterrows():
                if row["Trošak(opis)"] == "Usluga domaća" and row["Način plaćanja"] == "Gotovina":
                    query = """
                    INSERT INTO Promet (Datum, 
                                        `Naziv(ime) klijenta`, 
                                        Kilometraža, 
                                        `Startno mjesto`, 
                                        `Ciljno mjesto`, 
                                        `Komentar/Napomena`, 
                                        Lokacija, 
                                        `Iznos gotovina (KM)`,
                                        `Iznos žiralno (KM)`, 
                                        Plaćeno,
                                        `Operativni trošak (KM)`,
                                        `Neto zarada (KM)`)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """
                    cursor.execute(query, (row["Datum"], 
                                           row["Naziv(ime) klijenta"], 
                                           row["Kilometraža"], 
                                           row["Startno mjesto"], 
                                           row["Ciljno mjesto"], 
                                           row["Komentar/Napomena"],
                                           'BiH', 
                                           str(row["Iznos"]), 
                                           float(0), 
                                           naplaceno_map[row["Iznos"]],
                                           row["Operativni trošak"],
                                           row["Neto zarada"]))
                if row["Trošak(opis)"] == "Usluga inostranstvo" and row["Način plaćanja"] == "Gotovina":
                    query = """
                    INSERT INTO Promet (Datum,
                                        `Naziv(ime) klijenta`,
                                        Kilometraža, 
                                        `Startno mjesto`, 
                                        `Ciljno mjesto`, 
                                        `Komentar/Napomena`, 
                                        Lokacija, 
                                        `Iznos gotovina (KM)`,
                                        `Iznos žiralno (KM)`, 
                                        Plaćeno,
                                        `Operativni trošak (KM)`,
                                        `Neto zarada (KM)`)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """
                    cursor.execute(query, (row["Datum"],
                                           row["Naziv(ime) klijenta"],
                                           row["Kilometraža"], 
                                           row["Startno mjesto"],
                                           row["Ciljno mjesto"],
                                           row["Komentar/Napomena"],
                                           'Inostranstvo',
                                           row["Iznos"],
                                           float(0),
                                           naplaceno_map[row["Iznos"]],
                                           row["Operativni trošak"],
                                           row["Neto zarada"]))
                if row["Trošak(opis)"] == "Usluga domaća" and row["Način plaćanja"] == "Žiralno":
                    query = """
                    INSERT INTO Promet (Datum,
                                        `Naziv(ime) klijenta`, 
                                        Kilometraža, 
                                        `Startno mjesto`, 
                                        `Ciljno mjesto`, 
                                        `Komentar/Napomena`, 
                                        Lokacija, 
                                        `Iznos gotovina (KM)`,
                                        `Iznos žiralno (KM)`, 
                                        Plaćeno,
                                        `Operativni trošak (KM)`,
                                        `Neto zarada (KM)`)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """
                    cursor.execute(query, (row["Datum"],
                                           row["Naziv(ime) klijenta"], 
                                           row["Kilometraža"], 
                                           row["Startno mjesto"], 
                                           row["Ciljno mjesto"], 
                                           row["Komentar/Napomena"],
                                           'BiH', 
                                           float(0), 
                                           row["Iznos"], 
                                           naplaceno_map[row["Iznos"]],
                                           row["Operativni trošak"],
                                           row["Neto zarada"]))
                if row["Trošak(opis)"] == "Usluga inostranstvo" and row["Način plaćanja"] == "Žiralno":
                    query = """
                    INSERT INTO Promet (Datum, 
                                        `Naziv(ime) klijenta`,
                                        Kilometraža, 
                                        `Startno mjesto`, 
                                        `Ciljno mjesto`, 
                                        `Komentar/Napomena`, 
                                        Lokacija, 
                                        `Iznos gotovina (KM)`,
                                        `Iznos žiralno (KM)`, 
                                        Plaćeno,
                                        `Operativni trošak (KM)`,
                                        `Neto zarada (KM)`)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """
                    cursor.execute(query, (row["Datum"], 
                                           row["Naziv(ime) klijenta"],
                                           row["Kilometraža"], 
                                           row["Startno mjesto"], 
                                           row["Ciljno mjesto"], 
                                           row["Komentar/Napomena"],
                                           'Inostranstvo', 
                                           float(0), 
                                           row["Iznos"], 
                                           naplaceno_map[row["Iznos"]],
                                           row["Operativni trošak"],
                                           row["Neto zarada"]))
                
#connection_1.commit()

        if vrsta_troska == "Usluga probono (donacija)":
            for index, row in df.iterrows():
                query = """
                INSERT INTO Promet (Datum, 
                                    `Naziv(ime) klijenta`, 
                                    Kilometraža, 
                                    `Startno mjesto`, 
                                    `Ciljno mjesto`, 
                                    Lokacija, 
                                    `Iznos gotovina (KM)`, 
                                    `Iznos žiralno (KM)`, 
                                    Plaćeno, 
                                    `Operativni trošak (KM)`, 
                                    `Neto zarada (KM)`, 
                                    `Komentar/Napomena`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        """
                cursor.execute(query, (row["Datum"],
                                       row["Naziv(ime) klijenta"],
                                       row["Kilometraža"],
                                       row["Startno mjesto"],
                                       row["Ciljno mjesto"],
                                       row["Lokacija"],
                                       float(0),
                                       float(0),
                                       "GRATIS",
                                       row["Operativni trošak"],
                                       row["Neto zarada"],
                                       row["Komentar/Napomena"]))
                

        if vrsta_troska == "Gorivo":
            for index, row in df.iterrows():
                query = """
                INSERT INTO Gorivo (Datum, 
                                    Trošak(opis), 
                                    `Nasuta količina`, 
                                    `Cijena goriva (KM)`, 
                                    `Iznos (KM)`, 
                                    `Način plaćanja`, 
                                    `Benzinska pumpa`,  
                                    `Komentar/Napomena`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """
                cursor.execute(query, (row["Datum"],
                                       row["Trošak(opis)"], 
                                       row["Nasuta količina"], 
                                       row["Cijena goriva"], 
                                       row["Iznos"],
                                       row["Način plaćanja"], 
                                       row["Naziv benzinske pumpe"], 
                                       row["Komentar/Napomena"]))

        if vrsta_troska == "Troškovi održavanja (servis, registracija, gume)":
            for index, row in df.iterrows():
                if row["Trošak(opis)"] == "Servis":
                    query = """
                    INSERT INTO Servis (Datum,
                                        Kilometraža,
                                        `Iznos (KM)`,
                                        `Način plaćanja`,
                                        `Komentar/Napomena`)
                    VALUES (%s, %s, %s, %s, %s);
                            """
                    cursor.execute(query, (row["Datum"],
                                           row["Kilometraža"],
                                           row["Iznos"],
                                           row["Način plaćanja"],
                                           row["Komentar/Napomena"]))
                        
                else:
                    query = """
                    INSERT INTO Trošak (Datum,
                                        Opis,
                                        `Iznos (KM)`,
                                        `Način plaćanja`,
                                        `Komentar/Napomena`)
                    VALUES (%s, %s, %s, %s, %s);
                            """
                    cursor.execute(query, (row["Datum"],
                                           row["Trošak(opis)"],
                                           row["Iznos"],
                                           row["Način plaćanja"],
                                           row["Komentar/Napomena"]))
                    
                
        if vrsta_troska == "Terenski troškovi (osiguranje, saobraćajne kazne...)":
            for index, row in df.iterrows():
                query = """
                INSERT INTO Trošak (Datum,
                                    Opis,
                                    `Iznos (KM)`,
                                    `Način plaćanja`,
                                    `Komentar/Napomena`)
                VALUES (%s, %s, %s, %s, %s)
                        """
                cursor.execute(query, (row["Datum"],
                                       row["Trošak(opis)"],
                                       row["Iznos"],
                                       row["Način plaćanja"],
                                       row["Komentar/Napomena"]))
                        
connection_1.commit()



        

    

# if 'Gorivo' not in st.session_state:
#     st.session_state['Gorivo'] = 'Ne'

# if st.session_state['Gorivo'] == 'Da':
    
#     gorivo_litara.update({"disabled": False})
#     gorivo_cijena.update({"disabled": False})
#     gorivo_iznos.update({"disabled": False})
#     gorivo_nacin_placanja.update({"disabled": False})

#     df = call_data_editor(df, "sa gorivom")
# else:
# #if st.session_state['Gorivo'] == 'Ne':
#     gorivo_litara.update({"disabled": True})
#     gorivo_cijena.update({"disabled": True})
#     gorivo_iznos.update({"disabled": True})
#     gorivo_nacin_placanja.update({"disabled": True})

#     df = call_data_editor(df, "bez goriva")

# if df.iloc[-1, 1] == "Gorivo":
#     st.session_state['Gorivo'] = 'Da'
# elif df.iloc[-1, 1] != "Gorivo":
#     st.session_state['Gorivo'] = 'Ne'



# print(st.session_state['Gorivo'])
# edited_df = container.data_editor(
#     df,
#     column_config={
#         "Datum": datum,
#         "Trošak(opis)": trosak, 
#         "Gorivo litara": gorivo_litara,
#         "Gorivo cijena": gorivo_cijena,
#         "Gorivo iznos": gorivo_iznos,
#         "Gorivo način plaćanja": gorivo_nacin_placanja,
#         "Naziv(ime) klijenta": naziv_klijenta,
#         "Startno mjesto": startno_mjesto,
#         "Ciljno mjesto": ciljno_mjesto,
#         "Kilometraža": kilometraza,
#         "Iznos": iznos,
#         "Način plaćanja": nacin_placanja,
#         "Naplaćeno?": naplaceno,
#         "Operativni trošak": operativni_trosak,
#         "Neto zarada": neto_zarada,
#         "Komentar/Napomena": komentar
#     },
#     num_rows="dynamic",
#     use_container_width=True,
#     #key="Bez goriva"
# )

# if edited_df.iloc[-1, 1] == "Gorivo":
#     print(edited_df.iloc[-1, 1])

#     st.session_state['Gorivo'] = 'Da'
#     print(st.session_state['Gorivo'])
    
#     edited_df1 = container.data_editor(
#     edited_df,
#     column_config={
#         "Datum": datum,
#         "Trošak(opis)": trosak, 
#         "Gorivo litara": gorivo_litara,
#         "Gorivo cijena": gorivo_cijena,
#         "Gorivo iznos": gorivo_iznos,
#         "Gorivo način plaćanja": gorivo_nacin_placanja,
#         "Naziv(ime) klijenta": naziv_klijenta,
#         "Startno mjesto": startno_mjesto,
#         "Ciljno mjesto": ciljno_mjesto,
#         "Kilometraža": kilometraza,
#         "Iznos": iznos,
#         "Način plaćanja": nacin_placanja,
#         "Naplaćeno?": naplaceno,
#         "Operativni trošak": operativni_trosak,
#         "Neto zarada": neto_zarada,
#         "Komentar/Napomena": komentar
#     },
#     num_rows="dynamic",
#     use_container_width=True,
#     key="Sa gorivom"
# )
#     edited_df = edited_df1
    # gorivo_litara.update({"disabled": False})
    # gorivo_cijena.update({"disabled": False})
    # gorivo_iznos.update({"disabled": False})
    # gorivo_nacin_placanja.update({"disabled": False})
    
    
#     edited_df = container.data_editor(
#     edited_df.copy(),
#     column_config={
#         "Datum": datum,
#         "Trošak(opis)": trosak, 
#         "Gorivo litara": gorivo_litara,
#         "Gorivo cijena": gorivo_cijena,
#         "Gorivo iznos": gorivo_iznos,
#         "Gorivo način plaćanja": gorivo_nacin_placanja,
#         "Naziv(ime) klijenta": naziv_klijenta,
#         "Startno mjesto": startno_mjesto,
#         "Ciljno mjesto": ciljno_mjesto,
#         "Kilometraža": kilometraza,
#         "Iznos": iznos,
#         "Način plaćanja": nacin_placanja,
#         "Naplaćeno?": naplaceno,
#         "Operativni trošak": operativni_trosak,
#         "Neto zarada": neto_zarada,
#         "Komentar/Napomena": komentar
#     },
#     num_rows="dynamic",
#     use_container_width=True,
#     #key="Sa gorivom"
# )

    #print(gorivo_cijena)
# else:
#     print(edited_df.iloc[-1, 1])

#     st.session_state['Gorivo'] = 'Ne'
#     print(st.session_state['Gorivo'])
    #edited_df = edited_df
    # gorivo_litara.update({"disabled": True})
    # gorivo_cijena.update({"disabled": True})
    # gorivo_iznos.update({"disabled": True})
    # gorivo_nacin_placanja.update({"disabled": True})

#     edited_df2 = container.data_editor(
#     edited_df,
#     column_config={
#         "Datum": datum,
#         "Trošak(opis)": trosak, 
#         "Gorivo litara": gorivo_litara,
#         "Gorivo cijena": gorivo_cijena,
#         "Gorivo iznos": gorivo_iznos,
#         "Gorivo način plaćanja": gorivo_nacin_placanja,
#         "Naziv(ime) klijenta": naziv_klijenta,
#         "Startno mjesto": startno_mjesto,
#         "Ciljno mjesto": ciljno_mjesto,
#         "Kilometraža": kilometraza,
#         "Iznos": iznos,
#         "Način plaćanja": nacin_placanja,
#         "Naplaćeno?": naplaceno,
#         "Operativni trošak": operativni_trosak,
#         "Neto zarada": neto_zarada,
#         "Komentar/Napomena": komentar
#     },
#     num_rows="dynamic",
#     use_container_width=True,
#     key='Bez goriva'
# )   
#     edited_df = edited_df2