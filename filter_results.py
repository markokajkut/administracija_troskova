import streamlit as st
import pandas as pd
from helpers import clear_cache

def filter_results(odabir_tabele, administracija_connection):

    rest_of_query = ""
    
    ######## PROMET ##############
    if odabir_tabele == "Promet":
        
        with st.sidebar:
                    
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
            _datum = st.form("_datum", clear_on_submit=False)
            with _datum:
                st.write("Unesite raspon datuma")
                donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
                gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
                if st.form_submit_button("Potvrda"):
                    donja_datum = donja_datum
                    gornja_datum = gornja_datum
                    st.session_state.donja_datum_promet = donja_datum
                    st.session_state.gornja_datum_promet = gornja_datum
            if st.session_state.donja_datum_promet != None and st.session_state.gornja_datum_promet != None:
                with _datum:
                    st.info("Primjenjen filter.")
                query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum_promet}" AND "{st.session_state.gornja_datum_promet}"'
            rest_of_query = rest_of_query + " " + query_part_datum
        
            # NAZIV KLIJENTA
            konacan_naziv = ""
            if 'naziv_klijenta' not in st.session_state:
                st.session_state.naziv_klijenta = konacan_naziv
            query_part_naziv = ""
            _naziv_klijenta = st.form("_naziv_klijenta", clear_on_submit=False)
            with _naziv_klijenta:
                unos_naziv_klijenta = st.text_input("Naziv (ime) klijenta", "")
                if st.form_submit_button("Potvrda"):
                    konacan_naziv = unos_naziv_klijenta
                    st.session_state.naziv_klijenta = konacan_naziv
            if st.session_state.naziv_klijenta != "":
                with _naziv_klijenta:
                    st.info("Primjenjen filter.")
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
            _raspon_kilometraze = st.form("_raspon_kilometraze", clear_on_submit=False)
            with _raspon_kilometraze:
                st.write("Unesite raspon kilometraže")
                donja_kilometraza = st.number_input("Donja granica", min_value=float(0))
                gornja_kilometraza = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_kilometraza = donja_kilometraza
                    gornja_kilometraza = gornja_kilometraza
                    st.session_state.donja_kilometraza = donja_kilometraza
                    st.session_state.gornja_kilometraza = gornja_kilometraza
            if st.session_state.donja_kilometraza != None and st.session_state.gornja_kilometraza != None:
                with _raspon_kilometraze:
                    st.info("Primjenjen filter.")
                query_part_kilometraza = f'AND `Kilometraža pređena (km)` BETWEEN {st.session_state.donja_kilometraza} AND {st.session_state.gornja_kilometraza}'
            rest_of_query = rest_of_query + " " + query_part_kilometraza
            
            # STARTNO MJESTO
            startno_mjesto_konacno = ""
            if 'startno_mjesto' not in st.session_state:
                st.session_state.startno_mjesto = startno_mjesto_konacno
            query_part_start = ""
            _startno_mjesto = st.form("_startno_mjesto", clear_on_submit=False)
            with _startno_mjesto:
                startno_mjesto = st.text_input("Startno mjesto", "")
                if st.form_submit_button("Potvrda"):
                    startno_mjesto_konacno = startno_mjesto
                    st.session_state.startno_mjesto = startno_mjesto_konacno
            if st.session_state.startno_mjesto != "":
                with _startno_mjesto:
                    st.info("Primjenjen filter.")
                query_part_start = f'AND `Startno mjesto` = "{st.session_state.startno_mjesto}"'
            rest_of_query = rest_of_query + " " + query_part_start

            # CILJNO MJESTO
            ciljno_mjesto_konacno = ""
            if 'ciljno_mjesto' not in st.session_state:
                st.session_state.ciljno_mjesto = ciljno_mjesto_konacno
            query_part_cilj = ""
            _ciljno_mjesto = st.form("_ciljno_mjesto", clear_on_submit=False)
            with _ciljno_mjesto:
                ciljno_mjesto = st.text_input("Ciljno mjesto", "")
                if st.form_submit_button("Potvrda"):
                    ciljno_mjesto_konacno = ciljno_mjesto
                    st.session_state.ciljno_mjesto = ciljno_mjesto_konacno
            if st.session_state.ciljno_mjesto != "":
                with _ciljno_mjesto:
                    st.info("Primjenjen filter.")
                query_part_cilj = f'AND `Ciljno mjesto` = "{st.session_state.ciljno_mjesto}"'
            rest_of_query = rest_of_query + " " + query_part_cilj

            # LOKACIJA
            lokacija_konacno = ""
            if 'lokacija' not in st.session_state:
                st.session_state.lokacija = lokacija_konacno
            query_part_lokacija = ""
            _lokacija = st.form("_lokacija", clear_on_submit=False)
            with _lokacija:
                lokacija = st.selectbox(label="Lokacija", options=("BiH", "Inostranstvo"))
                if st.form_submit_button("Potvrda"):
                    lokacija_konacno = lokacija
                    st.session_state.lokacija = lokacija_konacno
            if st.session_state.lokacija != "":
                with _lokacija:
                    st.info("Primjenjen filter.")
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
            _iznos_gotovina = st.form("_iznos_gotovina", clear_on_submit=False)
            with _iznos_gotovina:
                st.write("Unesite raspon iznosa u gotovini")
                donja_iznos_gotovina = st.number_input("Donja granica", min_value=float(0))
                gornja_iznos_gotovina = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_iznos_gotovina = donja_iznos_gotovina
                    gornja_iznos_gotovina = gornja_iznos_gotovina
                    st.session_state.donja_iznos_gotovina = donja_iznos_gotovina
                    st.session_state.gornja_iznos_gotovina = gornja_iznos_gotovina
            if st.session_state.donja_iznos_gotovina != None and st.session_state.gornja_iznos_gotovina != None:
                with _iznos_gotovina:
                    st.info("Primjenjen filter.")
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
            _iznos_ziralno = st.form("_iznos_ziralno", clear_on_submit=False)
            with _iznos_ziralno:
                st.write("Unesite raspon žiralnog iznosa")
                donja_iznos_ziralno = st.number_input("Donja granica", min_value=float(0))
                gornja_iznos_ziralno = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_iznos_ziralno = donja_iznos_ziralno
                    gornja_iznos_ziralno = gornja_iznos_ziralno
                    st.session_state.donja_iznos_ziralno = donja_iznos_ziralno
                    st.session_state.gornja_iznos_ziralno = gornja_iznos_ziralno
            if st.session_state.donja_iznos_ziralno != None and st.session_state.gornja_iznos_ziralno != None:
                with _iznos_ziralno:
                    st.info("Primjenjen filter.")
                query_part_iznos_ziralno = f'AND `Iznos žiralno (KM)` BETWEEN {st.session_state.donja_iznos_ziralno} AND {st.session_state.gornja_iznos_ziralno}'
            rest_of_query = rest_of_query + " " + query_part_iznos_ziralno

            # PLACENO
            placeno_konacno = ""
            if 'placeno' not in st.session_state:
                st.session_state.placeno = placeno_konacno
            query_part_placeno = ""
            _placeno = st.form("_placeno", clear_on_submit=False)
            with _placeno:
                placeno = st.selectbox(label="Plaćeno", options=("DA", "NE", "GRATIS"))
                if st.form_submit_button("Potvrda"):
                    placeno_konacno = placeno
                    st.session_state.placeno = placeno_konacno
            if st.session_state.placeno != "":
                with _placeno:
                    st.info("Primjenjen filter.")
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
            _op_trosak = st.form("_op_trosak", clear_on_submit=False)
            with _op_trosak:
                st.write("Unesite raspon operativnog troška")
                donja_op_trosak = st.number_input("Donja granica", min_value=float(0))
                gornja_op_trosak = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_op_trosak = donja_op_trosak
                    gornja_op_trosak = gornja_op_trosak
                    st.session_state.donja_op_trosak = donja_op_trosak
                    st.session_state.gornja_op_trosak = gornja_op_trosak
            if st.session_state.donja_op_trosak != None and st.session_state.gornja_op_trosak != None:
                with _op_trosak:
                    st.info("Primjenjen filter.")
                query_part_op_trosak = f'AND `Operativni trošak (KM)` BETWEEN {st.session_state.donja_op_trosak} AND {st.session_state.gornja_op_trosak}'
            rest_of_query = rest_of_query + " " + query_part_op_trosak
            
            # CIJENA PO GAZENOM KILOMETRU
            donja_cijena_po_km = None
            gornja_cijena_po_km = None
            if 'donja_cijena_po_km' not in st.session_state:
                st.session_state.donja_cijena_po_km = donja_cijena_po_km
            if 'gornja_cijena_po_km' not in st.session_state:
                st.session_state.gornja_cijena_po_km = gornja_cijena_po_km
            query_part_cijena_po_km = ""
            _cijena_po_km = st.form("_cijena_po_km", clear_on_submit=False)
            with _cijena_po_km:
                st.write("Unesite raspon cijene po gaženom kilometru")
                donja_cijena_po_km = st.number_input("Donja granica cijena po km", min_value=float(0))
                gornja_cijena_po_km = st.number_input("Gornja granica cijena po km", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_cijena_po_km = donja_cijena_po_km
                    gornja_cijena_po_km = gornja_cijena_po_km
                    st.session_state.donja_cijena_po_km = donja_cijena_po_km
                    st.session_state.gornja_cijena_po_km = gornja_cijena_po_km
            if st.session_state.donja_cijena_po_km != None and st.session_state.gornja_cijena_po_km != None:
                with _cijena_po_km:
                    st.info("Primjenjen filter.")
                query_part_cijena_po_km = f'AND `Cijena po gaženom kilometru (KM/km)` BETWEEN {st.session_state.donja_cijena_po_km} AND {st.session_state.gornja_cijena_po_km}'
            rest_of_query = rest_of_query + " " + query_part_cijena_po_km

            # NETO ZARADA
            donja_neto_zarada = None
            gornja_neto_zarada = None
            if 'donja_neto_zarada' not in st.session_state:
                st.session_state.donja_neto_zarada = donja_neto_zarada
            if 'gornja_neto_zarada' not in st.session_state:
                st.session_state.gornja_neto_zarada = gornja_neto_zarada
            query_part_neto_zarada = "" 
            _neto_zarada = st.form("_neto_zarada", clear_on_submit=False)
            with _neto_zarada:
                st.write("Unesite raspon neto zarade")
                donja_neto_zarada = st.number_input("Donja granica", min_value=float(0))
                gornja_neto_zarada = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_neto_zarada = donja_neto_zarada
                    gornja_neto_zarada = gornja_neto_zarada
                    st.session_state.donja_neto_zarada = donja_neto_zarada
                    st.session_state.gornja_neto_zarada = gornja_neto_zarada
            if st.session_state.donja_neto_zarada != None and st.session_state.donja_neto_zarada != None:
                with _neto_zarada:
                    st.info("Primjenjen filter.")
                query_part_neto_zarada = f'AND `Neto zarada (KM)` BETWEEN {st.session_state.donja_neto_zarada} AND {st.session_state.gornja_neto_zarada}'
            rest_of_query = rest_of_query + " " + query_part_neto_zarada

            # KOMENTAR
            komentar_konacno = ""
            if 'komentar_promet' not in st.session_state:
                st.session_state.komentar_promet = komentar_konacno
            query_part_komentar = ""
            _komentar_promet = st.form("_komentar_promet", clear_on_submit=False)
            with _komentar_promet:
                komentar = st.text_input("Komentar/Napomena", "")
                if st.form_submit_button("Potvrda"):
                    komentar_konacno = komentar
                    st.session_state.komentar_promet = komentar_konacno
            if st.session_state.komentar_promet != "":
                with _komentar_promet:
                    st.info("Primjenjen filter.")
                query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar_promet}"'
            rest_of_query = rest_of_query + " " + query_part_komentar

        # QUERY
        if rest_of_query.strip() != "":
            rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
            query = f'SELECT * FROM {odabir_tabele} WHERE {rest_of_query};'
            
            df = pd.read_sql(query, administracija_connection)
        else:
            df = pd.read_sql(f'SELECT * from `{odabir_tabele}`;', administracija_connection)
        
        df['Datum'] = pd.to_datetime(df['Datum'])
        df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y.')
        
        tabela = st.dataframe(data=df.drop(columns=["Redni broj"]), use_container_width=True, hide_index=False)
        
                
    ######## GORIVO ##############
    if odabir_tabele == "Gorivo":
        
        with st.sidebar:
                    
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
            _datum_gorivo = st.form("_datum_gorivo", clear_on_submit=False)
            with _datum_gorivo:
                st.write("Unesite raspon datuma")
                donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
                gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
                if st.form_submit_button("Potvrda"):
                    donja_datum = donja_datum
                    gornja_datum = gornja_datum
                    st.session_state.donja_datum_gorivo = donja_datum
                    st.session_state.gornja_datum_gorivo = gornja_datum
            if st.session_state.donja_datum_gorivo != None and st.session_state.gornja_datum_gorivo != None:
                with _datum_gorivo:
                    st.info("Primjenjen filter.")
                query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum_gorivo}" AND "{st.session_state.gornja_datum_gorivo}"'
            rest_of_query = rest_of_query + " " + query_part_datum

            # KILOMETRAZA
            donja_kilometraza = None
            gornja_kilometraza = None
            if 'donja_kilometraza_gorivo' not in st.session_state:
                st.session_state.donja_kilometraza_gorivo = donja_kilometraza
            if 'gornja_kilometraza_gorivo' not in st.session_state:
                st.session_state.gornja_kilometraza_gorivo = gornja_kilometraza
            query_part_kilometraza = ""
            _raspon_kilometraze_gorivo = st.form("_raspon_kilometraze_gorivo", clear_on_submit=False)
            with _raspon_kilometraze_gorivo:
                st.write("Unesite raspon kilometraže")
                donja_kilometraza = st.number_input("Donja granica", min_value=float(0))
                gornja_kilometraza = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_kilometraza = donja_kilometraza
                    gornja_kilometraza = gornja_kilometraza
                    st.session_state.donja_kilometraza_gorivo = donja_kilometraza
                    st.session_state.gornja_kilometraza_gorivo = gornja_kilometraza
            if st.session_state.donja_kilometraza_gorivo != None and st.session_state.gornja_kilometraza_gorivo != None:
                with _raspon_kilometraze_gorivo:
                    st.info("Primjenjen filter.")
                query_part_kilometraza = f'AND `Kilometraža na satu (km)` BETWEEN {st.session_state.donja_kilometraza_gorivo} AND {st.session_state.gornja_kilometraza_gorivo}'
            rest_of_query = rest_of_query + " " + query_part_kilometraza 

            # NASUTA KOLICINA
            donja_nasuta_kolicina = None
            gornja_nasuta_kolicina = None
            if 'donja_nasuta_kolicina' not in st.session_state:
                st.session_state.donja_nasuta_kolicina = donja_nasuta_kolicina
            if 'gornja_nasuta_kolicina' not in st.session_state:
                st.session_state.gornja_nasuta_kolicina = gornja_nasuta_kolicina
            query_part_nasuta_kolicina = ""
            _raspon_nasute_kolicine = st.form("_raspon_nasute_kolicine", clear_on_submit=False)
            with _raspon_nasute_kolicine:
                st.write("Unesite raspon nasute količine goriva")
                donja_nasuta_kolicina = st.number_input("Donja granica", min_value=float(0))
                gornja_nasuta_kolicina = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_nasuta_kolicina = donja_nasuta_kolicina
                    gornja_nasuta_kolicina = gornja_nasuta_kolicina
                    st.session_state.donja_nasuta_kolicina = donja_nasuta_kolicina
                    st.session_state.gornja_nasuta_kolicina = gornja_nasuta_kolicina
            if st.session_state.donja_nasuta_kolicina != None and st.session_state.gornja_nasuta_kolicina != None:
                with _raspon_nasute_kolicine:
                    st.info("Primjenjen filter.")
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
            _raspon_cijene_goriva = st.form("_raspon_cijene_goriva", clear_on_submit=False)
            with _raspon_cijene_goriva:
                st.write("Unesite raspon cijene goriva")
                donja_cijena_goriva = st.number_input("Donja granica", min_value=float(0))
                gornja_cijena_goriva = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_cijena_goriva = donja_cijena_goriva
                    gornja_cijena_goriva = gornja_cijena_goriva
                    st.session_state.donja_cijena_goriva = donja_cijena_goriva
                    st.session_state.gornja_cijena_goriva = gornja_cijena_goriva
            if st.session_state.donja_cijena_goriva != None and st.session_state.gornja_cijena_goriva != None:
                with _raspon_cijene_goriva:
                    st.info("Primjenjen filter.")
                query_part_cijena_goriva = f'AND `Cijena goriva (KM/l)` BETWEEN {st.session_state.donja_cijena_goriva} AND {st.session_state.gornja_cijena_goriva}'
            rest_of_query = rest_of_query + " " + query_part_cijena_goriva

            # IZNOS GORIVO
            donja_iznos_gorivo = None
            gornja_iznos_gorivo = None
            if 'donja_iznos_gorivo' not in st.session_state:
                st.session_state.donja_iznos_gorivo = donja_iznos_gorivo
            if 'gornja_iznos_gorivo' not in st.session_state:
                st.session_state.gornja_iznos_gorivo = gornja_iznos_gorivo
            query_part_iznos_gorivo = ""
            _iznos_gorivo = st.form("_iznos_gorivo", clear_on_submit=False)
            with _iznos_gorivo:
                st.write("Unesite raspon iznosa goriva")
                donja_iznos_gorivo = st.number_input("Donja granica", min_value=float(0))
                gornja_iznos_gorivo = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_iznos_gorivo = donja_iznos_gorivo
                    gornja_iznos_gorivo = gornja_iznos_gorivo
                    st.session_state.donja_iznos_gorivo = donja_iznos_gorivo
                    st.session_state.gornja_iznos_gorivo = gornja_iznos_gorivo
            if st.session_state.donja_iznos_gorivo != None and st.session_state.gornja_iznos_gorivo != None:
                with _iznos_gorivo:
                    st.info("Primjenjen filter.")
                query_part_iznos_gorivo = f'AND `Iznos (KM)` BETWEEN {st.session_state.donja_iznos_gorivo} AND {st.session_state.gornja_iznos_gorivo}'
            rest_of_query = rest_of_query + " " + query_part_iznos_gorivo

            # NACIN PLACANJA
            nacin_placanja_konacno = ""
            if 'nacin_placanja_gorivo' not in st.session_state:
                st.session_state.nacin_placanja_gorivo = nacin_placanja_konacno
            query_part_nacin_placanja = ""
            _nacin_placanja_gorivo = st.form("_nacin_placanja_gorivo", clear_on_submit=False)
            with _nacin_placanja_gorivo:
                nacin_placanja = st.selectbox(label="Način plaćanja", options=('Gotovina', 'Žiralno', 'Kartica'))
                if st.form_submit_button("Potvrda"):
                    nacin_placanja_konacno = nacin_placanja
                    st.session_state.nacin_placanja_gorivo = nacin_placanja_konacno
            if st.session_state.nacin_placanja_gorivo != "":
                with _nacin_placanja_gorivo:
                    st.info("Primjenjen filter.")
                query_part_nacin_placanja = f'AND `Način plaćanja` = "{st.session_state.nacin_placanja_gorivo}"'
            rest_of_query = rest_of_query + " " + query_part_nacin_placanja

            # BENZINSKA PUMPA
            benz_pumpa_konacno = ""
            if 'benz_pumpa' not in st.session_state:
                st.session_state.benz_pumpa = benz_pumpa_konacno
            query_part_benz_pumpa = ""
            _benz_pumpa = st.form("_benz_pumpa", clear_on_submit=False)
            with _benz_pumpa:
                benz_pumpa = st.text_input("Naziv benzinske pumpe", "")
                if st.form_submit_button("Potvrda"):
                    benz_pumpa_konacno = benz_pumpa
                    st.session_state.benz_pumpa = benz_pumpa_konacno
            if st.session_state.benz_pumpa != "":
                with _benz_pumpa:
                    st.info("Primjenjen filter.")
                query_part_benz_pumpa = f'AND `Benzinska pumpa` = "{st.session_state.benz_pumpa}"'
            rest_of_query = rest_of_query + " " + query_part_benz_pumpa

            # KOMENTAR
            komentar_konacno = ""
            if 'komentar_gorivo' not in st.session_state:
                st.session_state.komentar_gorivo = komentar_konacno
            query_part_komentar = ""
            _komentar_gorivo = st.form("_komentar_gorivo", clear_on_submit=False)
            with _komentar_gorivo:
                komentar = st.text_input("Komentar/Napomena", "")
                if st.form_submit_button("Potvrda"):
                    komentar_konacno = komentar
                    st.session_state.komentar_gorivo = komentar_konacno
            if st.session_state.komentar_gorivo != "":
                with _komentar_gorivo:
                    st.info("Primjenjen filter.")
                query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar_gorivo}"'
            rest_of_query = rest_of_query + " " + query_part_komentar

        # QUERY
        if rest_of_query.strip() != "":
            rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
            query = f'SELECT * from {odabir_tabele} WHERE {rest_of_query};'
            
            df = pd.read_sql(query, administracija_connection)
        else:
            df = pd.read_sql(f'SELECT * from `{odabir_tabele}`;', administracija_connection)
        
        df['Datum'] = pd.to_datetime(df['Datum'])
        df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y.')
        
        tabela = st.dataframe(data=df.drop(columns=["Redni broj"]), use_container_width=True, hide_index=False)
        
            
    ######## SERVIS ##############
    if odabir_tabele == "Servis-Gume-Registracija":
            
        with st.sidebar:

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
            _datum_servis = st.form("_datum_servis", clear_on_submit=False)
            with _datum_servis:
                st.write("Unesite raspon datuma")
                donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
                gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
                if st.form_submit_button("Potvrda"):
                    donja_datum = donja_datum
                    gornja_datum = gornja_datum
                    st.session_state.donja_datum_servis = donja_datum
                    st.session_state.gornja_datum_servis = gornja_datum
            if st.session_state.donja_datum_servis != None and st.session_state.gornja_datum_servis != None:
                with _datum_servis:
                    st.info("Primjenjen filter.")
                query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum_servis}" AND "{st.session_state.gornja_datum_servis}"'
            rest_of_query = rest_of_query + " " + query_part_datum

            # OPIS
            konacan_opis = ""
            if 'opis_servis' not in st.session_state:
                st.session_state.opis_servis = konacan_opis
            query_part_opis = ""
            _opis_servis = st.form("_opis_servis", clear_on_submit=False)
            with _opis_servis:
                opis = st.text_input("Opis", "")
                if st.form_submit_button("Potvrda"):
                    konacan_opis = opis
                    st.session_state.opis_servis = konacan_opis
            if st.session_state.opis_servis != "":
                with _opis_servis:
                    st.info("Primjenjen filter.")
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
            _raspon_kilometraze_servis = st.form("_raspon_kilometraze_servis", clear_on_submit=False)
            with _raspon_kilometraze_servis:
                st.write("Unesite raspon kilometraže")
                donja_kilometraza = st.number_input("Donja granica", min_value=float(0))
                gornja_kilometraza = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_kilometraza = donja_kilometraza
                    gornja_kilometraza = gornja_kilometraza
                    st.session_state.donja_kilometraza_servis = donja_kilometraza
                    st.session_state.gornja_kilometraza_servis = gornja_kilometraza
            if st.session_state.donja_kilometraza_servis != None and st.session_state.gornja_kilometraza_servis != None:
                with _raspon_kilometraze_servis:
                    st.info("Primjenjen filter.")
                query_part_kilometraza = f'AND `Kilometraža na satu (km)` BETWEEN {st.session_state.donja_kilometraza_servis} AND {st.session_state.gornja_kilometraza_servis}'
            rest_of_query = rest_of_query + " " + query_part_kilometraza  

            # IZNOS
            donja_iznos = None
            gornja_iznos = None
            if 'donja_iznos_servis' not in st.session_state:
                st.session_state.donja_iznos_servis = donja_iznos
            if 'gornja_iznos_servis' not in st.session_state:
                st.session_state.gornja_iznos_servis = gornja_iznos
            query_part_iznos = ""
            _iznos_servis = st.form("_iznos_servis", clear_on_submit=False)
            with _iznos_servis:
                st.write("Unesite raspon iznosa")
                donja_iznos = st.number_input("Donja granica", min_value=float(0))
                gornja_iznos = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_iznos = donja_iznos
                    gornja_iznos = gornja_iznos
                    st.session_state.donja_iznos_servis = donja_iznos
                    st.session_state.gornja_iznos_servis = gornja_iznos
            if st.session_state.donja_iznos_servis != None and st.session_state.gornja_iznos_servis != None:
                with _iznos_servis:
                    st.info("Primjenjen filter.")
                query_part_iznos = f'AND `Iznos (KM)` BETWEEN {st.session_state.donja_iznos_servis} AND {st.session_state.gornja_iznos_servis}'
            rest_of_query = rest_of_query + " " + query_part_iznos

            # NACIN PLACANJA
            nacin_placanja_konacno = ""
            if 'nacin_placanja_servis' not in st.session_state:
                st.session_state.nacin_placanja_servis = nacin_placanja_konacno
            query_part_nacin_placanja = ""
            _nacin_placanja_servis = st.form("_nacin_placanja_servis", clear_on_submit=False)
            with _nacin_placanja_servis:
                nacin_placanja = st.selectbox(label="Način plaćanja", options=('Gotovina', 'Žiralno', 'Kartica'))
                if st.form_submit_button("Potvrda"):
                    nacin_placanja_konacno = nacin_placanja
                    st.session_state.nacin_placanja_servis = nacin_placanja_konacno
            if st.session_state.nacin_placanja_servis != "":
                with _nacin_placanja_servis:
                    st.info("Primjenjen filter.")
                query_part_nacin_placanja = f'AND `Način plaćanja` = "{st.session_state.nacin_placanja_servis}"'
            rest_of_query = rest_of_query + " " + query_part_nacin_placanja

            # KOMENTAR
            komentar_konacno = ""
            if 'komentar_servis' not in st.session_state:
                st.session_state.komentar_servis = komentar_konacno
            query_part_komentar = ""
            _komentar_servis = st.form("_komentar_servis", clear_on_submit=False)
            with _komentar_servis:
                komentar = st.text_input("Komentar/Napomena", "")
                if st.form_submit_button("Potvrda"):
                    komentar_konacno = komentar
                    st.session_state.komentar_servis = komentar_konacno
            if st.session_state.komentar_servis != "":
                with _komentar_servis:
                    st.info("Primjenjen filter.")
                query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar_servis}"'
            rest_of_query = rest_of_query + " " + query_part_komentar

        # QUERY
        if rest_of_query.strip() != "":
            rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
            query = f'SELECT * from `{odabir_tabele}` WHERE {rest_of_query};'
            
            df = pd.read_sql(query, administracija_connection)
        else:
            df = pd.read_sql(f'SELECT * from `{odabir_tabele}`;', administracija_connection)
            
        df['Datum'] = pd.to_datetime(df['Datum'])
        df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y.')
        
        tabela = st.dataframe(data=df.drop(columns=["Redni broj"]), use_container_width=True, hide_index=False)

            
    ######## KAZNE ##############
    if odabir_tabele == "Kazne":
        
        with st.sidebar:
                    
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
            _datum_kazne = st.form("_datum_kazne", clear_on_submit=False)
            with _datum_kazne:
                st.write("Unesite raspon datuma")
                donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
                gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
                if st.form_submit_button("Potvrda"):
                    donja_datum = donja_datum
                    gornja_datum = gornja_datum
                    st.session_state.donja_datum_kazne = donja_datum
                    st.session_state.gornja_datum_kazne = gornja_datum
            if st.session_state.donja_datum_kazne != None and st.session_state.gornja_datum_kazne != None:
                with _datum_kazne:
                    st.info("Primjenjen filter.")
                query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum_kazne}" AND "{st.session_state.gornja_datum_kazne}"'
            rest_of_query = rest_of_query + " " + query_part_datum

            # PREKRSAJ
            prekrsaj_konacno = ""
            if 'prekrsaj' not in st.session_state:
                st.session_state.prekrsaj = prekrsaj_konacno
            query_part_prekrsaj = ""
            _prekrsaj = st.form("_prekrsaj", clear_on_submit=False)
            with _prekrsaj:
                prekrsaj = st.text_input("Prekršaj", "")
                if st.form_submit_button("Potvrda"):
                    prekrsaj_konacno = prekrsaj
                    st.session_state.prekrsaj = prekrsaj_konacno
            if st.session_state.prekrsaj != "":
                with _prekrsaj:
                    st.info("Primjenjen filter.")
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
            _iznos_kazne = st.form("_iznos_kazne", clear_on_submit=False)
            with _iznos_kazne:
                st.write("Unesite raspon iznosa")
                donja_iznos = st.number_input("Donja granica", min_value=float(0))
                gornja_iznos = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_iznos = donja_iznos
                    gornja_iznos = gornja_iznos
                    st.session_state.donja_iznos_kazne = donja_iznos
                    st.session_state.gornja_iznos_kazne = gornja_iznos
            if st.session_state.donja_iznos_kazne != None and st.session_state.gornja_iznos_kazne != None:
                with _iznos_kazne:
                    st.info("Primjenjen filter.")
                query_part_iznos = f'AND `Iznos (KM)` BETWEEN {st.session_state.donja_iznos_kazne} AND {st.session_state.gornja_iznos_kazne}'
            rest_of_query = rest_of_query + " " + query_part_iznos

            # KOMENTAR
            komentar_konacno = ""
            if 'komentar_kazne' not in st.session_state:
                st.session_state.komentar_kazne = komentar_konacno
            query_part_komentar = ""
            _komentar_kazne = st.form("_komentar_kazne", clear_on_submit=False)
            with _komentar_kazne:
                komentar = st.text_input("Komentar/Napomena", "")
                if st.form_submit_button("Potvrda"):
                    komentar_konacno = komentar
                    st.session_state.komentar_kazne = komentar_konacno
            if st.session_state.komentar_kazne != "":
                with _komentar_kazne:
                    st.info("Primjenjen filter.")
                query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar_kazne}"'
            rest_of_query = rest_of_query + " " + query_part_komentar

        # QUERY
        if rest_of_query.strip() != "":
            rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
            query = f'SELECT * from {odabir_tabele} WHERE {rest_of_query};'
            
            df = pd.read_sql(query, administracija_connection)
        else:
            df = pd.read_sql(f'SELECT * from `{odabir_tabele}`;', administracija_connection)
        
        df['Datum'] = pd.to_datetime(df['Datum'])
        df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y.')
        
        tabela = st.dataframe(data=df.drop(columns=["Redni broj"]), use_container_width=True, hide_index=False)

    
    ######## TROSAK ##############
    if odabir_tabele == "Trošak":
        
        with st.sidebar:
                    
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
            _datum_trosak = st.form("_datum_trosak", clear_on_submit=False)
            with _datum_trosak:
                st.write("Unesite raspon datuma")
                donja_datum = st.date_input("Donja granica", format="DD.MM.YYYY")
                gornja_datum = st.date_input("Gornja granica", format="DD.MM.YYYY")
                if st.form_submit_button("Potvrda"):
                    donja_datum = donja_datum
                    gornja_datum = gornja_datum
                    st.session_state.donja_datum_trosak = donja_datum
                    st.session_state.gornja_datum_trosak = gornja_datum
            if st.session_state.donja_datum_trosak != None and st.session_state.gornja_datum_trosak != None:
                with _datum_trosak:
                    st.info("Primjenjen filter.")
                query_part_datum = f'AND Datum BETWEEN "{st.session_state.donja_datum_trosak}" AND "{st.session_state.gornja_datum_trosak}"'
            rest_of_query = rest_of_query + " " + query_part_datum

            # OPIS
            opis_konacno = ""
            if 'opis_trosak' not in st.session_state:
                st.session_state.opis_trosak = opis_konacno
            query_part_opis_trosak = ""
            _opis_trosak = st.form("_opis_trosak", clear_on_submit=False)
            with _opis_trosak:
                opis = st.selectbox(label="Opis trošak", options=("Putarina",
                                                                "Terminal",
                                                                "Mostarina",
                                                                "Osiguranje",
                                                                "Saobraćajne kazne",
                                                                "Telefon",
                                                                "Privatno",
                                                                "Pranje vozila",
                                                                "Ostalo"))
                if st.form_submit_button("Potvrda"):
                    opis_konacno = opis
                    st.session_state.opis_trosak = opis_konacno
            if st.session_state.opis_trosak != "":
                with _opis_trosak:
                    st.info("Primjenjen filter.")
                query_part_opis_trosak = f'AND Opis = "{st.session_state.opis_trosak}"'
            rest_of_query = rest_of_query + " " + query_part_opis_trosak

            # DODATNI OPIS
            konacan_dodatni_opis = ""
            if 'dodatni_opis_trosak' not in st.session_state:
                st.session_state.dodatni_opis_trosak = konacan_dodatni_opis
            query_part_dodatni_opis = ""
            _dodatni_opis_trosak = st.form("_dodatni_opis_trosak", clear_on_submit=False)
            with _dodatni_opis_trosak:
                dodatni_opis = st.text_input("Dodatni opis", "")
                if st.form_submit_button("Potvrda"):
                    konacan_dodatni_opis = dodatni_opis
                    st.session_state.dodatni_opis_trosak = konacan_dodatni_opis
            if st.session_state.dodatni_opis_trosak != "":
                with _dodatni_opis_trosak:
                    st.info("Primjenjen filter.")
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
            _iznos_trosak = st.form("_iznos_trosak", clear_on_submit=False)
            with _iznos_trosak:
                st.write("Unesite raspon iznosa")
                donja_iznos = st.number_input("Donja granica", min_value=float(0))
                gornja_iznos = st.number_input("Gornja granica", min_value=float(0))
                if st.form_submit_button("Potvrda"):
                    donja_iznos = donja_iznos
                    gornja_iznos = gornja_iznos
                    st.session_state.donja_iznos_trosak = donja_iznos
                    st.session_state.gornja_iznos_trosak = gornja_iznos
            if st.session_state.donja_iznos_trosak != None and st.session_state.gornja_iznos_trosak != None:
                with _iznos_trosak:
                    st.info("Primjenjen filter.")
                query_part_iznos = f'AND `Iznos (KM)` BETWEEN {st.session_state.donja_iznos_trosak} AND {st.session_state.gornja_iznos_trosak}'
            rest_of_query = rest_of_query + " " + query_part_iznos

            # NACIN PLACANJA
            nacin_placanja_konacno = ""
            if 'nacin_placanja_trosak' not in st.session_state:
                st.session_state.nacin_placanja_trosak = nacin_placanja_konacno
            query_part_nacin_placanja = ""
            _nacin_placanja_trosak = st.form("_nacin_placanja_trosak", clear_on_submit=False)
            with _nacin_placanja_trosak:
                nacin_placanja = st.selectbox(label="Način plaćanja", options=('Gotovina', 'Žiralno', 'Kartica'))
                if st.form_submit_button("Potvrda"):
                    nacin_placanja_konacno = nacin_placanja
                    st.session_state.nacin_placanja_trosak = nacin_placanja_konacno
            if st.session_state.nacin_placanja_trosak != "":
                with _nacin_placanja_trosak:
                    st.info("Primjenjen filter.")
                query_part_nacin_placanja = f'AND `Način plaćanja` = "{st.session_state.nacin_placanja_trosak}"'
            rest_of_query = rest_of_query + " " + query_part_nacin_placanja

            # KOMENTAR
            komentar_konacno = ""
            if 'komentar_trosak' not in st.session_state:
                st.session_state.komentar_trosak = komentar_konacno
            query_part_komentar = ""
            _komentar_trosak = st.form("_komentar_trosak", clear_on_submit=False)
            with _komentar_trosak:
                komentar = st.text_input("Komentar/Napomena", "")
                if st.form_submit_button("Potvrda"):
                    komentar_konacno = komentar
                    st.session_state.komentar_trosak = komentar_konacno
            if st.session_state.komentar_trosak != "":
                with _komentar_trosak:
                    st.info("Primjenjen filter.")
                query_part_komentar = f'AND `Komentar/Napomena` = "{st.session_state.komentar_trosak}"'
            rest_of_query = rest_of_query + " " + query_part_komentar

        # QUERY
        if rest_of_query.strip() != "":
            rest_of_query = rest_of_query.split("AND", maxsplit=1)[1].strip()
            query = f'SELECT * from {odabir_tabele} WHERE {rest_of_query};'
            
            df = pd.read_sql(query, administracija_connection)
        else:
            df = pd.read_sql(f'SELECT * from `{odabir_tabele}`;', administracija_connection)
            
        df['Datum'] = pd.to_datetime(df['Datum'])
        df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y.')
        
        tabela = st.dataframe(data=df.drop(columns=["Redni broj"]), use_container_width=True, hide_index=False)
