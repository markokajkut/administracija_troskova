GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' IDENTIFIED BY 'admin';
CREATE DATABASE IF NOT EXISTS `Unos`;
SET character_set_server = 'utf8';
SET collation_server = 'utf8mb3_croatian_ci';

CREATE TABLE IF NOT EXISTS Promet (
    `Redni broj` INT,
    Datum DATE,
    `Naziv(ime) klijenta` VARCHAR(255),
    `Kilometraža pređena (km)` FLOAT,
    `Startno mjesto` VARCHAR(255),
    `Ciljno mjesto` VARCHAR(255),
    Lokacija ENUM('BiH', 'Inostranstvo'),
    `Iznos gotovina (KM)` FLOAT,
    `Iznos žiralno (KM)` FLOAT,
    Plaćeno ENUM('DA', 'NE', 'GRATIS'),
    `Operativni trošak (KM)` FLOAT,
    `Cijena po gaženom kilometru (KM/km)` FLOAT,
    `Neto zarada (KM)` FLOAT,
    `Komentar/Napomena` VARCHAR(255),
    PRIMARY KEY (`Redni broj`)
);

CREATE TABLE IF NOT EXISTS Gorivo (
    `Redni broj` INT,
    Datum DATE,
    `Kilometraža na satu (km)` FLOAT,
    `Nasuta količina (l)` FLOAT,
    `Cijena goriva (KM/l)` FLOAT,
    `Iznos (KM)` FLOAT,
    `Način plaćanja` ENUM('Gotovina', 'Žiralno', 'Kartica'),
    `Benzinska pumpa` VARCHAR(255),
    `Komentar/Napomena` VARCHAR(255),
    PRIMARY KEY (`Redni broj`)
);

CREATE TABLE IF NOT EXISTS `Servis-Gume-Registracija` (
    `Redni broj` INT,
    Datum DATE,
    Opis VARCHAR(255),
    `Kilometraža na satu (km)` FLOAT,
    `Iznos (KM)` FLOAT,
    `Način plaćanja` ENUM('Gotovina', 'Žiralno', 'Kartica'),
    `Komentar/Napomena` VARCHAR(255),
    PRIMARY KEY (`Redni broj`)
);

CREATE TABLE IF NOT EXISTS Kazne (
    `Redni broj` INT,
    Datum DATE,
    Prekršaj VARCHAR(255),
    `Iznos (KM)` FLOAT,
    `Komentar/Napomena` VARCHAR(255),
    PRIMARY KEY (`Redni broj`)
);

CREATE TABLE IF NOT EXISTS Trošak (
    `Redni broj` INT,
    Datum DATE,
    Opis ENUM('Operativni trošak', 'Terminal', 'Putarina', 'Mostarina',
              'Osiguranje', 'Telefon', 'Privatno', 'Pranje vozila', 'Ostalo'
              ),
    `Dodatni opis (opciono)` VARCHAR(255),
    `Iznos (KM)` FLOAT,
    `Način plaćanja` ENUM('Gotovina', 'Žiralno', 'Kartica'),
    `Komentar/Napomena` VARCHAR(255)
);

USE Unos;

CREATE TABLE IF NOT EXISTS Usluga (
    Datum DATE, 
    `Trošak(opis)` VARCHAR(255), 
    `Naziv(ime) klijenta` VARCHAR(255),
    Lokacija ENUM('BiH', 'Inostranstvo'), 
    `Startno mjesto` VARCHAR(255),
    `Ciljno mjesto` VARCHAR(255),
    `Kilometraža na satu START` FLOAT,
    `Kilometraža na satu KRAJ` FLOAT, 
    Iznos FLOAT, 
    `Način plaćanja` ENUM('Gotovina', 'Žiralno'),
    `Naplaćeno?` ENUM('DA', 'NE'), 
    `Operativni trošak` FLOAT, 
    `Neto zarada` FLOAT,
    `Komentar/Napomena` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Gorivo (
    Datum DATE,
    `Trošak(opis)` VARCHAR(255),
    `Kilometraža na satu` FLOAT,
    `Nasuta količina` FLOAT, 
    `Cijena goriva` FLOAT, 
    `Iznos` FLOAT, 
    `Način plaćanja` ENUM("Gotovina", "Žiralno", "Kartica"), 
    `Naziv benzinske pumpe` VARCHAR(255),  
    `Komentar/Napomena` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Troskovi_odrzavanja (
    Datum DATE, 
    `Trošak(opis)` VARCHAR(255),
    `Kilometraža na satu` FLOAT,
    `Iznos` FLOAT,
    `Način plaćanja` ENUM("Gotovina", "Žiralno", "Kartica"), 
    `Komentar/Napomena` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Terenski_troskovi (
    Datum DATE, 
    `Trošak(opis)` VARCHAR(255),
    `Dodatni opis (opciono)` VARCHAR(255),                
    `Iznos` FLOAT,
    `Način plaćanja` ENUM("Gotovina", "Žiralno", "Kartica"), 
    `Komentar/Napomena` VARCHAR(255)
);