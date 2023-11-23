import streamlit as st
import datetime

datum = st.column_config.DateColumn(
            format="DD.MM.YYYY",
            default=datetime.date.today(),
            help="Izaberite datum",
            required=True
        )

gorivo_kilometraza = st.column_config.NumberColumn(
            help="Kilometraža na satu",
            default=float(0),
            min_value=float(0),
            format="%.2f km"
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

def call_data_editor(vrsta_troska, df_usluga, df_gorivo, df_troskovi_odrzavanja, df_terenski_troskovi):
    
    ############### USLUGA DOMACA ILI USLUGA INOSTRANSTVO ###############
    if vrsta_troska == "Usluga":
        st.session_state.edited_df_usluga = st.data_editor(
        df_usluga,
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

    ############### GORIVO ###############    
    elif vrsta_troska == "Gorivo":
        st.session_state.edited_df_gorivo = st.data_editor(
        df_gorivo,
        column_config={
            "Datum": datum,
            "Trošak(opis)": st.column_config.TextColumn(help="Vrsta troška", default=vrsta_troska, disabled=True),
            "Kilometraža": gorivo_kilometraza, 
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
        st.session_state.edited_df_troskovi_odrzavanja = st.data_editor(
        df_troskovi_odrzavanja,
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
        return st.session_state.edited_df_troskovi_odrzavanja

    ############### TERENSKI TROSKOVI ###############    
    elif vrsta_troska == "Terenski troškovi (osiguranje, saobraćajne kazne...)":
        st.session_state.edited_df_terenski_troskovi = st.data_editor(
        df_terenski_troskovi,
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