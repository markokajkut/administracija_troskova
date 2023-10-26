import pymysql
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def unos_u_bazu(vrsta_troska, unos_engine, administracija_connection, df):

    if vrsta_troska == "Usluga":
        for index, row in df.iterrows():
            if row["Trošak(opis)"] == "Usluga naplativa" and row["Način plaćanja"] == "Gotovina":
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
                            VALUES (:datum, 
                                    :naziv_klijenta, 
                                    :kilometraza, 
                                    :startno_mjesto, 
                                    :ciljno_mjesto, 
                                    :komentar, 
                                    :lokacija, 
                                    :iznos_gotovina, 
                                    :iznos_ziralno, 
                                    :placeno, 
                                    :op_trosak, 
                                    :neto_zarada);
                        """
                row_tuple = ({"datum": row["Datum"], 
                              "naziv_klijenta": row["Naziv(ime) klijenta"], 
                              "kilometraza": row["Kilometraža"], 
                              "startno_mjesto": row["Startno mjesto"], 
                              "ciljno_mjesto": row["Ciljno mjesto"], 
                              "komentar": row["Komentar/Napomena"],
                              "lokacija": row["Lokacija"], 
                              "iznos_gotovina": row["Iznos"], 
                              "iznos_ziralno": float(0), 
                              "placeno": row["Naplaćeno?"],
                              "op_trosak": row["Operativni trošak"],
                              "neto_zarada": row["Neto zarada"]})
                administracija_connection.execute(text(query), **row_tuple)
           
            if row["Trošak(opis)"] == "Usluga naplativa" and row["Način plaćanja"] == "Žiralno":
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
                            VALUES (:datum, 
                                    :naziv_klijenta, 
                                    :kilometraza, 
                                    :startno_mjesto, 
                                    :ciljno_mjesto, 
                                    :komentar,
                                    :lokacija, 
                                    :iznos_gotovina, 
                                    :iznos_ziralno, 
                                    :placeno, 
                                    :op_trosak, 
                                    :neto_zarada);
                        """
                row_tuple = ({"datum": row["Datum"],
                              "naziv_klijenta": row["Naziv(ime) klijenta"], 
                              "kilometraza": row["Kilometraža"], 
                              "startno_mjesto": row["Startno mjesto"], 
                              "ciljno_mjesto": row["Ciljno mjesto"], 
                              "komentar": row["Komentar/Napomena"],
                              "lokacija": row["Lokacija"], 
                              "iznos_gotovina": float(0), 
                              "iznos_ziralno": row["Iznos"], 
                              "placeno": row["Naplaćeno?"],
                              "op_trosak": row["Operativni trošak"],
                              "neto_zarada": row["Neto zarada"]})
                administracija_connection.execute(text(query), **row_tuple)
                          

            if row["Trošak(opis)"] == "Usluga pro-bono":
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
                            VALUES (:datum, 
                                    :naziv_klijenta, 
                                    :kilometraza, 
                                    :startno_mjesto, 
                                    :ciljno_mjesto, 
                                    :lokacija, 
                                    :iznos_gotovina, 
                                    :iznos_ziralno, 
                                    :placeno, 
                                    :op_trosak, 
                                    :neto_zarada,
                                    :komentar);
                        """
                row_tuple = ({"datum": row["Datum"],
                              "naziv_klijenta": row["Naziv(ime) klijenta"],
                              "kilometraza": row["Kilometraža"],
                              "startno_mjesto": row["Startno mjesto"],
                              "ciljno_mjesto": row["Ciljno mjesto"],
                              "lokacija": row["Lokacija"],
                              "iznos_gotovina": float(0),
                              "iznos_ziralno": float(0),
                              "placeno": row["Naplaćeno?"],
                              "op_trosak": row["Operativni trošak"],
                              "neto_zarada": row["Neto zarada"],
                              "komentar": row["Komentar/Napomena"]})
                administracija_connection.execute(text(query), **row_tuple)
                    
        df.to_sql(con=unos_engine, name="Usluga", schema="Unos", if_exists="replace", index=False)

    if vrsta_troska == "Gorivo":
        for index, row in df.iterrows():
            query = """
            INSERT INTO Gorivo (Datum, 
                                `Nasuta količina (l)`, 
                                `Cijena goriva (KM)`, 
                                `Iznos (KM)`, 
                                `Način plaćanja`, 
                                `Benzinska pumpa`,  
                                `Komentar/Napomena`)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """
            row_tuple = (row["Datum"],
                         row["Nasuta količina"], 
                         row["Cijena goriva"], 
                         row["Iznos"],
                         row["Način plaćanja"], 
                         row["Naziv benzinske pumpe"], 
                         row["Komentar/Napomena"])
            administracija_connection.execute(text(query), (row_tuple,))

        df.to_sql(con=unos_engine, name="Gorivo", schema="Unos", if_exists="replace", index=False)

    if vrsta_troska == "Troškovi održavanja (servis, registracija, gume)":
        for index, row in df.iterrows():
            if row["Trošak(opis)"] == "Servis":
                query = """
                INSERT INTO Servis (Datum,
                                    Opis,
                                    Kilometraža,
                                    `Iznos (KM)`,
                                    `Način plaćanja`,
                                    `Komentar/Napomena`)
                VALUES (%s, %s, %s, %s, %s, %s);
                        """
                row_tuple = (row["Datum"],
                             row["Dodatni opis (opciono)"],
                             row["Kilometraža"],
                             row["Iznos"],
                             row["Način plaćanja"],
                             row["Komentar/Napomena"])
                administracija_connection.execute(text(query), (row_tuple,))
                    
            else:
                query = """
                INSERT INTO Trošak (Datum,
                                    Opis,
                                    `Dodatni opis (opciono)`,
                                    `Iznos (KM)`,
                                    `Način plaćanja`,
                                    `Komentar/Napomena`)
                VALUES (%s, %s, %s, %s, %s, %s);
                        """
                row_tuple = (row["Datum"],
                             row["Trošak(opis)"],
                             row["Dodatni opis (opciono)"],
                             row["Iznos"],
                             row["Način plaćanja"],
                             row["Komentar/Napomena"])
                administracija_connection.execute(text(query), (row_tuple,))
                

        df.to_sql(con=unos_engine, name="Troskovi_odrzavanja", schema="Unos", if_exists="replace", index=False)

    if vrsta_troska == "Terenski troškovi (osiguranje, saobraćajne kazne...)":
        for index, row in df.iterrows():
            if row["Trošak(opis)"] == "Saobraćajne kazne":
                query = """
                INSERT INTO Kazne (Datum,
                                   Prekršaj,
                                   Iznos,
                                   `Komentar/Napomena`)
                VALUES (%s, %s, %s, %s);
                        """
                row_tuple = (row["Datum"],
                             row["Dodatni opis (opciono)"],
                             row["Iznos"],
                             row["Komentar/Napomena"])
                administracija_connection.execute(text(query), (row_tuple,))
            else:
                query = """
                INSERT INTO Trošak (Datum,
                                    Opis,
                                    `Dodatni opis (opciono)`,
                                    `Iznos (KM)`,
                                    `Način plaćanja`,
                                    `Komentar/Napomena`)
                VALUES (%s, %s, %s, %s, %s, %s);
                        """
                row_tuple = (row["Datum"],
                             row["Trošak(opis)"],
                             row["Dodatni opis (opciono)"],
                             row["Iznos"],
                             row["Način plaćanja"],
                             row["Komentar/Napomena"])
                administracija_connection.execute(text(query), (row_tuple,))
                
        df.to_sql(con=unos_engine, name="Terenski_troskovi", schema="Unos", if_exists="replace", index=False)
                            
    #administracija_connection.commit()