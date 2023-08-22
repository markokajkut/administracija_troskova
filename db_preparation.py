import mariadb

# connection parameters
conn_params = {
    "user" : "user",
    "password" : "password",
    "host" : "192.168.90.95",
    "port" : 3306,
    "database" : "mydatabase"
}

# Establish a connection
connection = mariadb.connect(**conn_params)
cursor = connection.cursor()

promet = """
CREATE TABLE IF NOT EXISTS Promet (
    Datum DATE,
    Kilometraža FLOAT,
    Relacija VARCHAR(255),
    Napomena VARCHAR(255),
    Lokacija ENUM('BiH', 'Inostranstvo'),
    `Iznos gotovina` FLOAT,
    `Iznos žiralno` FLOAT,
    Plaćeno ENUM('DA', 'NE')
);
"""

gorivo = """
CREATE TABLE IF NOT EXISTS Gorivo (
    Datum DATE,
    Kilometraža FLOAT,
    `Utrošak goriva (L)` FLOAT,
    Cijena FLOAT,
    Iznos FLOAT
);
"""

servis = """
CREATE TABLE IF NOT EXISTS Servis (
    Datum DATE,
    Kilometraža FLOAT,
    Servis VARCHAR(255),
    Napomena VARCHAR(255),
    Iznos FLOAT
);
"""

kazne = """
CREATE TABLE IF NOT EXISTS Kazne (
    Datum DATE,
    Prekršaj VARCHAR(255),
    Iznos FLOAT
);
"""

trosak = """
CREATE TABLE IF NOT EXISTS Trošak (
    Datum DATE,
    Opis ENUM('Svakodnevni trošak', 'Terminal', 'Autoput', 'Mostarina'),
    Iznos FLOAT
);
"""

cursor.execute("SET character_set_server = 'utf8';")
cursor.execute("SET collation_server = 'utf8mb3_croatian_ci';")
cursor.execute(promet)
cursor.execute(gorivo)
cursor.execute(servis)
cursor.execute(kazne)
cursor.execute(trosak)

cursor.close()
connection.close()