import mariadb
import os
import subprocess
from dotenv import load_dotenv
load_dotenv()

#find_db_ip_command = ["docker", "inspect", "-f", "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}", "db"]
#db_ip_output = subprocess.check_output(find_db_ip_command, universal_newlines=True).strip()

# connection parameters
conn_params = {
    "user" : os.getenv('DB_USER'),
    "password" : os.getenv('DB_PASSWORD'),
    "host" : os.getenv('DB_HOST'),
    #"host": db_ip_output,
    "port" : int(os.getenv('DB_PORT')),
    "database" : os.getenv('DB_DATABASE')
}

db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')

# Establish a connection
connection = mariadb.connect(**conn_params)
cursor = connection.cursor()

promet = """
CREATE TABLE IF NOT EXISTS Promet (
    Datum DATE,
    `Naziv(ime) klijenta` VARCHAR(255),
    Kilometraža FLOAT,
    `Startno mjesto` VARCHAR(255),
    `Ciljno mjesto` VARCHAR(255),
    Lokacija ENUM('BiH', 'Inostranstvo'),
    `Iznos gotovina (KM)` FLOAT,
    `Iznos žiralno (KM)` FLOAT,
    Plaćeno ENUM('DA', 'NE', 'GRATIS'),
    `Operativni trošak (KM)` FLOAT,
    `Neto zarada (KM)` FLOAT,
    `Komentar/Napomena` VARCHAR(255)
);
"""

gorivo = """
CREATE TABLE IF NOT EXISTS Gorivo (
    Datum DATE,
    `Nasuta količina (l)` FLOAT,
    `Cijena goriva (KM)` FLOAT,
    `Iznos (KM)` FLOAT,
    `Način plaćanja` ENUM('Gotovina', 'Žiralno', 'Kartica'),
    `Benzinska pumpa` VARCHAR(255),
    `Komentar/Napomena` VARCHAR(255)
);
"""

servis = """
CREATE TABLE IF NOT EXISTS Servis (
    Datum DATE,
    Opis VARCHAR(255),
    Kilometraža FLOAT,
    `Iznos (KM)` FLOAT,
    `Način plaćanja` ENUM('Gotovina', 'Žiralno', 'Kartica'),
    `Komentar/Napomena` VARCHAR(255)
);
"""

kazne = """
CREATE TABLE IF NOT EXISTS Kazne (
    Datum DATE,
    Prekršaj VARCHAR(255),
    Iznos FLOAT,
    `Komentar/Napomena` VARCHAR(255)
);
"""

trosak = """
CREATE TABLE IF NOT EXISTS Trošak (
    Datum DATE,
    Opis ENUM('Operativni trošak', 'Terminal', 'Putarina', 'Mostarina', 'Gorivo',
              'Osiguranje', 'Telefon', 'Privatno', 'Pranje vozila', 'Ostalo', 'Registracija', 'Saobraćajne kazne',
              'Servis', 'Gume'),
    `Dodatni opis (opciono)` VARCHAR(255),
    `Iznos (KM)` FLOAT,
    `Način plaćanja` ENUM('Gotovina', 'Žiralno', 'Kartica'),
    `Komentar/Napomena` VARCHAR(255)
);
"""

#cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO '{db_user}'@'%' IDENTIFIED BY '{db_pass}' WITH GRANT OPTION;")
#cursor.execute("FLUSH PRIVILEGES;")
cursor.execute("SET character_set_server = 'utf8';")
cursor.execute("SET collation_server = 'utf8mb3_croatian_ci';")
cursor.execute(promet)
cursor.execute(gorivo)
cursor.execute(servis)
cursor.execute(kazne)
cursor.execute(trosak)

cursor.close()
connection.close()
