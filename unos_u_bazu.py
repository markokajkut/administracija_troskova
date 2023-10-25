import sqlalchemy
import pymysql
import os
import pandas as pd
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
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        """
                administracija_connection.execute(query, (row["Datum"], 
                                                      row["Naziv(ime) klijenta"], 
                                                      row["Kilometraža"], 
                                                      row["Startno mjesto"], 
                                                      row["Ciljno mjesto"], 
                                                      row["Komentar/Napomena"],
                                                      row["Lokacija"], 
                                                      row["Iznos"], 
                                                      float(0), 
                                                      row["Naplaćeno?"],
                                                      row["Operativni trošak"],
                                                      row["Neto zarada"]))
           
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
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        """
                administracija_connection.execute(query, (row["Datum"],
                                                      row["Naziv(ime) klijenta"], 
                                                      row["Kilometraža"], 
                                                      row["Startno mjesto"], 
                                                      row["Ciljno mjesto"], 
                                                      row["Komentar/Napomena"],
                                                      row["Lokacija"], 
                                                      float(0), 
                                                      row["Iznos"], 
                                                      row["Naplaćeno?"],
                                                      row["Operativni trošak"],
                                                      row["Neto zarada"]))
                          

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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        """
                administracija_connection.execute(query, (row["Datum"],
                                                      row["Naziv(ime) klijenta"],
                                                      row["Kilometraža"],
                                                      row["Startno mjesto"],
                                                      row["Ciljno mjesto"],
                                                      row["Lokacija"],
                                                      float(0),
                                                      float(0),
                                                      row["Naplaćeno?"],
                                                      row["Operativni trošak"],
                                                      row["Neto zarada"],
                                                      row["Komentar/Napomena"]))
                    
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
            administracija_connection.execute(query, (row["Datum"],
                                                  row["Nasuta količina"], 
                                                  row["Cijena goriva"], 
                                                  row["Iznos"],
                                                  row["Način plaćanja"], 
                                                  row["Naziv benzinske pumpe"], 
                                                  row["Komentar/Napomena"]))

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
                administracija_connection.execute(query, (row["Datum"],
                                                      row["Dodatni opis (opciono)"],
                                                      row["Kilometraža"],
                                                      row["Iznos"],
                                                      row["Način plaćanja"],
                                                      row["Komentar/Napomena"]))
                    
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
                administracija_connection.execute(query, (row["Datum"],
                                                      row["Trošak(opis)"],
                                                      row["Dodatni opis (opciono)"],
                                                      row["Iznos"],
                                                      row["Način plaćanja"],
                                                      row["Komentar/Napomena"]))
                

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
                administracija_connection.execute(query, (row["Datum"],
                                                      row["Dodatni opis (opciono)"],
                                                      row["Iznos"],
                                                      row["Komentar/Napomena"]))
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
                administracija_connection.execute(query, (row["Datum"],
                                                      row["Trošak(opis)"],
                                                      row["Dodatni opis (opciono)"],
                                                      row["Iznos"],
                                                      row["Način plaćanja"],
                                                      row["Komentar/Napomena"]))
                
        df.to_sql(con=unos_engine, name="Terenski_troskovi", schema="Unos", if_exists="replace", index=False)
                            
    administracija_connection.commit()