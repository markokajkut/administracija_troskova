from sqlalchemy import text

def unos_u_bazu_administracija(vrsta_troska, administracija_engine, df, df_troskovi_odrzavanja, df_terenski_troskovi):
    with administracija_engine.connect() as administracija_connection:
        #administracija_connection.execute(text("TRUNCATE TABLE Promet;"))
        # administracija_connection.execute(text("TRUNCATE TABLE Gorivo;"))
        # administracija_connection.execute(text("TRUNCATE TABLE Servis;"))
        # administracija_connection.execute(text("TRUNCATE TABLE Kazne;"))
        # administracija_connection.execute(text("TRUNCATE TABLE Trošak;"))
        # administracija_connection.commit()
        if vrsta_troska == "Usluga":
            #administracija_connection.execute(text("TRUNCATE TABLE Promet;"))
            for index, row in df.iterrows():
                if row["Način plaćanja"] == "Gotovina":
                    query = """
                    INSERT INTO Promet (`Redni broj`,
                                        Datum, 
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
                                VALUES (:redni_broj,
                                        :datum, 
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
                                        :neto_zarada)
                                ON DUPLICATE KEY UPDATE
                                        Datum = VALUES(Datum),
                                        `Naziv(ime) klijenta` = VALUES(`Naziv(ime) klijenta`), 
                                        Kilometraža = VALUES(Kilometraža), 
                                        `Startno mjesto` = VALUES(`Startno mjesto`), 
                                        `Ciljno mjesto` = VALUES(`Ciljno mjesto`),
                                        `Komentar/Napomena` = VALUES(`Komentar/Napomena`),
                                        Lokacija = VALUES(Lokacija),
                                        `Iznos gotovina (KM)` = VALUES(`Iznos gotovina (KM)`),
                                        `Iznos žiralno (KM)` = VALUES(`Iznos žiralno (KM)`), 
                                        Plaćeno = VALUES(Plaćeno),
                                        `Operativni trošak (KM)` = VALUES(`Operativni trošak (KM)`),
                                        `Neto zarada (KM)` = VALUES(`Neto zarada (KM)`);
                            """
                    row_dict = {"redni_broj": index+1,
                                "datum": row["Datum"], 
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
                                "neto_zarada": row["Neto zarada"]}
                    administracija_connection.execute(text(query), parameters=row_dict)
            
                if row["Način plaćanja"] == "Žiralno":
                    query = """
                    INSERT INTO Promet (`Redni broj`,
                                        Datum,
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
                                VALUES (:redni_broj,
                                        :datum, 
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
                                        :neto_zarada)
                                ON DUPLICATE KEY UPDATE
                                        Datum = VALUES(Datum),
                                        `Naziv(ime) klijenta` = VALUES(`Naziv(ime) klijenta`), 
                                        Kilometraža = VALUES(Kilometraža), 
                                        `Startno mjesto` = VALUES(`Startno mjesto`), 
                                        `Ciljno mjesto` = VALUES(`Ciljno mjesto`),
                                        `Komentar/Napomena` = VALUES(`Komentar/Napomena`),
                                        Lokacija = VALUES(Lokacija),
                                        `Iznos gotovina (KM)` = VALUES(`Iznos gotovina (KM)`),
                                        `Iznos žiralno (KM)` = VALUES(`Iznos žiralno (KM)`), 
                                        Plaćeno = VALUES(Plaćeno),
                                        `Operativni trošak (KM)` = VALUES(`Operativni trošak (KM)`),
                                        `Neto zarada (KM)` = VALUES(`Neto zarada (KM)`);
                            """
                    row_dict = {"redni_broj": index+1,
                                "datum": row["Datum"],
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
                                "neto_zarada": row["Neto zarada"]}
                    administracija_connection.execute(text(query), parameters=row_dict)
                            

                if row["Način plaćanja"] == "Gratis":
                    query = """
                    INSERT INTO Promet (`Redni broj`,
                                        Datum, 
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
                                VALUES (:redni_broj,
                                        :datum, 
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
                                        :neto_zarada)
                                ON DUPLICATE KEY UPDATE
                                        Datum = VALUES(Datum),
                                        `Naziv(ime) klijenta` = VALUES(`Naziv(ime) klijenta`), 
                                        Kilometraža = VALUES(Kilometraža), 
                                        `Startno mjesto` = VALUES(`Startno mjesto`), 
                                        `Ciljno mjesto` = VALUES(`Ciljno mjesto`),
                                        `Komentar/Napomena` = VALUES(`Komentar/Napomena`),
                                        Lokacija = VALUES(Lokacija),
                                        `Iznos gotovina (KM)` = VALUES(`Iznos gotovina (KM)`),
                                        `Iznos žiralno (KM)` = VALUES(`Iznos žiralno (KM)`), 
                                        Plaćeno = VALUES(Plaćeno),
                                        `Operativni trošak (KM)` = VALUES(`Operativni trošak (KM)`),
                                        `Neto zarada (KM)` = VALUES(`Neto zarada (KM)`);
                            """
                    row_dict = {"redni_broj": index+1,
                                "datum": row["Datum"],
                                "naziv_klijenta": row["Naziv(ime) klijenta"],
                                "kilometraza": row["Kilometraža"],
                                "startno_mjesto": row["Startno mjesto"],
                                "ciljno_mjesto": row["Ciljno mjesto"],
                                "komentar": row["Komentar/Napomena"],
                                "lokacija": row["Lokacija"],
                                "iznos_gotovina": float(0),
                                "iznos_ziralno": float(0),
                                "placeno": row["Naplaćeno?"],
                                "op_trosak": row["Operativni trošak"],
                                "neto_zarada": row["Neto zarada"]}
                    administracija_connection.execute(text(query), parameters=row_dict)
                        
    

        if vrsta_troska == "Gorivo":
            for index, row in df.iterrows():
                query = """
                INSERT INTO Gorivo (`Redni broj`,
                                    Datum, 
                                    `Nasuta količina (l)`, 
                                    `Cijena goriva (KM)`, 
                                    `Iznos (KM)`, 
                                    `Način plaćanja`, 
                                    `Benzinska pumpa`,  
                                    `Komentar/Napomena`)
                            VALUES (:redni_broj,
                                    :datum,
                                    :nasuta_kolicina,
                                    :cijena_goriva,
                                    :gorivo_iznos,
                                    :nacin_placanja,
                                    :naziv_pumpe,
                                    :komentar)
                            ON DUPLICATE KEY UPDATE
                                    Datum = VALUES(Datum),
                                    `Nasuta količina (l)` = VALUES(`Nasuta količina (l)`), 
                                    `Cijena goriva (KM)` = VALUES(`Cijena goriva (KM)`), 
                                    `Iznos (KM)` = VALUES(`Iznos (KM)`), 
                                    `Način plaćanja` = VALUES(`Način plaćanja`),
                                    `Benzinska pumpa` = VALUES(`Benzinska pumpa`),  
                                    `Komentar/Napomena` = VALUES(`Komentar/Napomena`);
                        """
                row_dict = {"redni_broj": index+1,
                            "datum": row["Datum"],
                            "nasuta_kolicina": row["Nasuta količina"], 
                            "cijena_goriva": row["Cijena goriva"], 
                            "gorivo_iznos": row["Iznos"],
                            "nacin_placanja": row["Način plaćanja"], 
                            "naziv_pumpe": row["Naziv benzinske pumpe"], 
                            "komentar": row["Komentar/Napomena"]}
                administracija_connection.execute(text(query), parameters=row_dict)

            

        if vrsta_troska == "Troškovi održavanja (servis, registracija, gume)":
            administracija_connection.execute(text("TRUNCATE TABLE Trošak;"))


            for index, row in df_terenski_troskovi.iterrows():
                if row["Trošak(opis)"] != "Saobraćajne kazne":
                    query = """
                    INSERT INTO Trošak (`Redni broj`,
                                        Datum,
                                        Opis,
                                        `Dodatni opis (opciono)`,
                                        `Iznos (KM)`,
                                        `Način plaćanja`,
                                        `Komentar/Napomena`)
                                VALUES (:redni_broj,
                                        :datum,
                                        :opis,
                                        :dodatni_opis,
                                        :iznos,
                                        :nacin_placanja,
                                        :komentar);
                            """
                    row_dict = {"redni_broj": index+1,
                                "datum": row["Datum"],
                                "opis": row["Trošak(opis)"],
                                "dodatni_opis": row["Dodatni opis (opciono)"],
                                "iznos": row["Iznos"],
                                "nacin_placanja": row["Način plaćanja"],
                                "komentar": row["Komentar/Napomena"]}
                    if df_terenski_troskovi.loc[0, "Iznos"] != float(0):
                        administracija_connection.execute(text(query), parameters=row_dict)
                    else:
                        pass

            for index, row in df.iterrows():
                if row["Trošak(opis)"] == "Servis":
                    query = """
                    INSERT INTO Servis (`Redni broj`,
                                        Datum,
                                        Opis,
                                        Kilometraža,
                                        `Iznos (KM)`,
                                        `Način plaćanja`,
                                        `Komentar/Napomena`)
                                VALUES (:redni_broj,
                                        :datum,
                                        :dodatni_opis,
                                        :kilometraza,
                                        :iznos,
                                        :nacin_placanja,
                                        :komentar)
                                ON DUPLICATE KEY UPDATE
                                        Datum = VALUES(Datum),
                                        Opis = VALUES(Opis),
                                        Kilometraža = VALUES(Kilometraža),
                                        `Iznos (KM)` = VALUES(`Iznos (KM)`),
                                        `Način plaćanja` = VALUES(`Način plaćanja`),
                                        `Komentar/Napomena` = VALUES(`Komentar/Napomena`);
                            """
                    row_dict = {"redni_broj": index+1,
                                "datum": row["Datum"],
                                "dodatni_opis": row["Dodatni opis (opciono)"],
                                "kilometraza": row["Kilometraža"],
                                "iznos": row["Iznos"],
                                "nacin_placanja": row["Način plaćanja"],
                                "komentar": row["Komentar/Napomena"]}
                    administracija_connection.execute(text(query), parameters=row_dict)
                        
                else:
                    query = """
                    INSERT INTO Trošak (`Redni broj`,
                                        Datum,
                                        Opis,
                                        `Dodatni opis (opciono)`,
                                        `Iznos (KM)`,
                                        `Način plaćanja`,
                                        `Komentar/Napomena`)
                                VALUES (:redni_broj,
                                        :datum,
                                        :opis,
                                        :dodatni_opis,
                                        :iznos,
                                        :nacin_placanja,
                                        :komentar);
                            """
                            #     ON DUPLICATE KEY UPDATE
                            #             Datum = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :datum
                            #                 ELSE Datum END, 
                            #             Opis = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :opis
                            #                 ELSE Opis END,
                            #             `Dodatni opis (opciono)` = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :dodatni_opis
                            #                 ELSE `Dodatni opis (opciono)` END,
                            #             `Iznos (KM)` = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :iznos
                            #                 ELSE `Iznos (KM)` END,
                            #             `Način plaćanja` = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :nacin_placanja
                            #                 ELSE `Način plaćanja` END,
                            #             `Komentar/Napomena` = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :komentar
                            #                 ELSE `Komentar/Napomena` END;
                            # """
                    row_dict = {"redni_broj": index+1,
                                "datum": row["Datum"],
                                "opis": row["Trošak(opis)"],
                                "dodatni_opis": row["Dodatni opis (opciono)"],
                                "iznos": row["Iznos"],
                                "nacin_placanja": row["Način plaćanja"],
                                "komentar": row["Komentar/Napomena"]}
                    administracija_connection.execute(text(query), parameters=row_dict)
                    

            

        if vrsta_troska == "Terenski troškovi (osiguranje, saobraćajne kazne...)":

            administracija_connection.execute(text("TRUNCATE TABLE Trošak;"))

            for index, row in df_troskovi_odrzavanja.iterrows():
                if row["Trošak(opis)"] != "Servis":
                    query = """
                    INSERT INTO Trošak (`Redni broj`,
                                        Datum,
                                        Opis,
                                        `Dodatni opis (opciono)`,
                                        `Iznos (KM)`,
                                        `Način plaćanja`,
                                        `Komentar/Napomena`)
                                VALUES (:redni_broj,
                                        :datum,
                                        :opis,
                                        :dodatni_opis,
                                        :iznos,
                                        :nacin_placanja,
                                        :komentar);
                            """
                    row_dict = {"redni_broj": index+1,
                                "datum": row["Datum"],
                                "opis": row["Trošak(opis)"],
                                "dodatni_opis": row["Dodatni opis (opciono)"],
                                "iznos": row["Iznos"],
                                "nacin_placanja": row["Način plaćanja"],
                                "komentar": row["Komentar/Napomena"]}
                    if df_troskovi_odrzavanja.loc[0, "Iznos"] != float(0):
                        administracija_connection.execute(text(query), parameters=row_dict)
                    else:
                        pass


            for index, row in df.iterrows():
                if row["Trošak(opis)"] == "Saobraćajne kazne":
                    query = """
                    INSERT INTO Kazne (`Redni broj`,
                                       Datum,
                                       Prekršaj,
                                       `Iznos (KM)`,
                                       `Komentar/Napomena`)
                                VALUES (:redni_broj,
                                        :datum,
                                        :dodatni_opis,
                                        :iznos,
                                        :komentar)
                            ON DUPLICATE KEY UPDATE
                                        Datum = VALUES(Datum),
                                        Prekršaj = VALUES(Prekršaj),
                                        `Iznos (KM)` = VALUES(`Iznos (KM)`),
                                       `Komentar/Napomena` = VALUES(`Komentar/Napomena`);
                            """
                    row_dict = {"redni_broj": index+1,
                                "datum": row["Datum"],
                                "dodatni_opis": row["Dodatni opis (opciono)"],
                                "iznos": row["Iznos"],
                                "komentar": row["Komentar/Napomena"]}
                    administracija_connection.execute(text(query), parameters=row_dict)
                else:
                    query = """
                    INSERT INTO Trošak (`Redni broj`,
                                        Datum,
                                        Opis,
                                        `Dodatni opis (opciono)`,
                                        `Iznos (KM)`,
                                        `Način plaćanja`,
                                        `Komentar/Napomena`)
                                VALUES (:redni_broj,
                                        :datum,
                                        :opis,
                                        :dodatni_opis,
                                        :iznos,
                                        :nacin_placanja,
                                        :komentar);
                            """
                            #     ON DUPLICATE KEY UPDATE
                            #             Datum = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :datum
                            #                 ELSE Datum END, 
                            #             Opis = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :opis
                            #                 ELSE Opis END,
                            #             `Dodatni opis (opciono)` = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :dodatni_opis
                            #                 ELSE `Dodatni opis (opciono)` END,
                            #             `Iznos (KM)` = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :iznos
                            #                 ELSE `Iznos (KM)` END,
                            #             `Način plaćanja` = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :nacin_placanja
                            #                 ELSE `Način plaćanja` END,
                            #             `Komentar/Napomena` = CASE
                            #                 WHEN `Redni broj` = :redni_broj
                            #                 AND Opis = :opis 
                            #                 THEN :komentar
                            #                 ELSE `Komentar/Napomena` END;
                            # """
                    row_dict = {"redni_broj": index+1,
                                "datum": row["Datum"],
                                "opis": row["Trošak(opis)"],
                                "dodatni_opis": row["Dodatni opis (opciono)"],
                                "iznos": row["Iznos"],
                                "nacin_placanja": row["Način plaćanja"],
                                "komentar": row["Komentar/Napomena"]}
                    administracija_connection.execute(text(query), parameters=row_dict)
                    
        administracija_connection.commit()
                    
            

def unos_u_bazu_unos(unos_engine, df, vrsta_troska):

    if vrsta_troska == "Usluga":
        df.to_sql(con=unos_engine, name="Usluga", schema="Unos", if_exists="replace", index=False)
    if vrsta_troska == "Gorivo":                    
        df.to_sql(con=unos_engine, name="Gorivo", schema="Unos", if_exists="replace", index=False)
    if vrsta_troska == "Troškovi održavanja (servis, registracija, gume)":
        df.to_sql(con=unos_engine, name="Troskovi_odrzavanja", schema="Unos", if_exists="replace", index=False)
    if vrsta_troska == "Terenski troškovi (osiguranje, saobraćajne kazne...)":
        df.to_sql(con=unos_engine, name="Terenski_troskovi", schema="Unos", if_exists="replace", index=False)