USE [master]
GO

/****** Object:  Database [szkolka]    Script Date: 06.06.2020 10:42:01 ******/
CREATE DATABASE [szkolka]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'szkolka', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL14.SQLEXPRESS01\MSSQL\DATA\szkolka.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'szkolka_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL14.SQLEXPRESS01\MSSQL\DATA\szkolka_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
GO

IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [szkolka].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO

ALTER DATABASE [szkolka] SET ANSI_NULL_DEFAULT OFF 
GO

ALTER DATABASE [szkolka] SET ANSI_NULLS OFF 
GO

ALTER DATABASE [szkolka] SET ANSI_PADDING OFF 
GO

ALTER DATABASE [szkolka] SET ANSI_WARNINGS OFF 
GO

ALTER DATABASE [szkolka] SET ARITHABORT OFF 
GO

ALTER DATABASE [szkolka] SET AUTO_CLOSE OFF 
GO

ALTER DATABASE [szkolka] SET AUTO_SHRINK OFF 
GO

ALTER DATABASE [szkolka] SET AUTO_UPDATE_STATISTICS ON 
GO

ALTER DATABASE [szkolka] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO

ALTER DATABASE [szkolka] SET CURSOR_DEFAULT  GLOBAL 
GO

ALTER DATABASE [szkolka] SET CONCAT_NULL_YIELDS_NULL OFF 
GO

ALTER DATABASE [szkolka] SET NUMERIC_ROUNDABORT OFF 
GO

ALTER DATABASE [szkolka] SET QUOTED_IDENTIFIER OFF 
GO

ALTER DATABASE [szkolka] SET RECURSIVE_TRIGGERS OFF 
GO

ALTER DATABASE [szkolka] SET  DISABLE_BROKER 
GO

ALTER DATABASE [szkolka] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO

ALTER DATABASE [szkolka] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO

ALTER DATABASE [szkolka] SET TRUSTWORTHY OFF 
GO

ALTER DATABASE [szkolka] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO

ALTER DATABASE [szkolka] SET PARAMETERIZATION SIMPLE 
GO

ALTER DATABASE [szkolka] SET READ_COMMITTED_SNAPSHOT OFF 
GO

ALTER DATABASE [szkolka] SET HONOR_BROKER_PRIORITY OFF 
GO

ALTER DATABASE [szkolka] SET RECOVERY SIMPLE 
GO

ALTER DATABASE [szkolka] SET  MULTI_USER 
GO

ALTER DATABASE [szkolka] SET PAGE_VERIFY CHECKSUM  
GO

ALTER DATABASE [szkolka] SET DB_CHAINING OFF 
GO

ALTER DATABASE [szkolka] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO

ALTER DATABASE [szkolka] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO

ALTER DATABASE [szkolka] SET DELAYED_DURABILITY = DISABLED 
GO

ALTER DATABASE [szkolka] SET QUERY_STORE = OFF
GO

ALTER DATABASE [szkolka] SET  READ_WRITE 
GO


use szkolka;

CREATE TABLE roslina(
id_roslina int NOT NULL PRIMARY KEY,
nazwa_lacinska varchar(255) NOT NULL,
klasa varchar(255),
rzad varchar(255),
rodzina varchar(255),
rodzaj varchar(255),
gatunek varchar(255),
pochodzenie varchar(255),
wysokosc_rosliny varchar(255),
okres_kwitnienia varchar(255)
);


CREATE TABLE stanowisko(
id_stanowisko int NOT NULL PRIMARY KEY,
strefa varchar(255),
rzad varchar(255),
miejsce varchar(255)
);

CREATE TABLE zastosowanie(
id_zastosowanie int NOT NULL PRIMARY KEY,
nazwa varchar(255)
);

CREATE TABLE informacje(
id_informacje int NOT NULL PRIMARY KEY,
nazwa varchar(255) NOT NULL,
ilosc_na_stanie varchar(255),
zywotnosc varchar(255),
id_roslina int FOREIGN KEY REFERENCES roslina(id_roslina),
id_zastosowanie int FOREIGN KEY REFERENCES zastosowanie(id_zastosowanie),
id_stanowisko int FOREIGN KEY REFERENCES stanowisko(id_stanowisko)
);


CREATE TABLE owoce(
id_owoce int NOT NULL PRIMARY KEY,
obecnosc varchar(255),
barwa varchar(255),
rodzaj varchar(255),
id_informacje int FOREIGN KEY REFERENCES informacje(id_informacje)
);

CREATE TABLE kwiaty(
id_kwiaty int,
pora_roku varchar(255),
cechy varchar(255),
kolor varchar(255),
id_informacje int,
PRIMARY KEY (id_kwiaty),
FOREIGN KEY (id_informacje) REFERENCES informacje(id_informacje)
);

CREATE TABLE uprawa(
id_uprawa int,
nawadnianie varchar(255),
nawozenie varchar(255),
rodzaj_nawozu varchar(255),
id_informacje int,
PRIMARY KEY (id_uprawa),
FOREIGN KEY (id_informacje) REFERENCES informacje(id_informacje)
);

CREATE TABLE stan(
id_stan int,
zyski varchar(255),
straty varchar(255),
choroby varchar(255),
id_uprawa int,
PRIMARY KEY (id_stan),
FOREIGN KEY (id_uprawa) REFERENCES uprawa(id_uprawa)
);


CREATE TABLE warunki(
id_warunki int,
miejsce varchar(255),
tolerancja varchar(255),
strefy_mrozoodpornosci varchar(255),
id_informacje int,
PRIMARY KEY (id_warunki),
FOREIGN KEY (id_informacje) REFERENCES informacje(id_informacje)
);

CREATE TABLE gleba(
id_gleba int,
ph varchar(255),
rodzaj varchar(255),
wilgotnosc varchar(255),
id_warunki int,
PRIMARY KEY (id_gleba),
FOREIGN KEY (id_warunki) REFERENCES warunki(id_warunki)
);

CREATE TABLE liscie(
id_liscie int,
wielkosc varchar(255),
kolor varchar(255),
ksztalt varchar(255),
id_warunki int,
PRIMARY KEY (id_liscie),
FOREIGN KEY (id_warunki) REFERENCES warunki(id_warunki)
);

CREATE TABLE klienci(
id_klient int,
imie varchar(255) NOT NULL,
nazwisko varchar(255) NOT NULL,
adres varchar(255) NOT NULL,
numer_telefonu varchar(255),
e_mail varchar(255),
PRIMARY KEY (id_klient),
);

CREATE TABLE zamowienia(
id_zamowienia int,
ilosc int NOT NULL,
data_zamowienia varchar(255),
data_odbioru varchar(255),
cena varchar(255),
id_informacje int,
id_klient int,
PRIMARY KEY (id_zamowienia),
FOREIGN KEY (id_informacje) REFERENCES informacje(id_informacje),
FOREIGN KEY (id_klient) REFERENCES klienci(id_klient)
);



-------------------
--zastosowanie

INSERT INTO zastosowanie(id_zastosowanie, nazwa) 
VALUES (1, 'zielen miejska')

INSERT INTO zastosowanie(id_zastosowanie, nazwa) 
VALUES (2, 'ogród')

INSERT INTO zastosowanie(id_zastosowanie, nazwa) 
VALUES (3, 'donica')

INSERT INTO zastosowanie(id_zastosowanie, nazwa) 
VALUES (4, 'owoc dekoracyjny')

INSERT INTO zastosowanie(id_zastosowanie, nazwa) 
VALUES (5, 'rosliny ozdobne')

INSERT INTO zastosowanie(id_zastosowanie, nazwa) 
VALUES (6, 'ogrod skalny')

INSERT INTO zastosowanie(id_zastosowanie, nazwa) 
VALUES (7, 'pod drzewa i krzewy')

INSERT INTO zastosowanie(id_zastosowanie, nazwa) 
VALUES (8, 'obrzeża')

INSERT INTO zastosowanie(id_zastosowanie, nazwa) 
VALUES (9, 'tarasowe')

select * from zastosowanie;

-------------------------------------------------------
--abelia mosańska

INSERT INTO roslina (id_roslina, nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) 
VALUES (1, 'Abelia mosanensis' , 'okrytonasienne', 'szczeciowe', 'przewiertniowate', 'abelia', 'abelia mosańska', 'Korea', '1-2m', 'maj, czerwiec')

INSERT INTO stanowisko (id_stanowisko, strefa, rzad, miejsce) VALUES (1, '2', 'I', '10')

INSERT INTO informacje (id_informacje, nazwa, ilosc_na_stanie, zywotnosc, id_roslina, id_zastosowanie, id_stanowisko) 
VALUES (1,'Abelia mosańska', 15, '25 lat',1, 3, 1)

INSERT INTO owoce (id_owoce, id_informacje, obecnosc, barwa, rodzaj)  VALUES (1, 1,  'brak', 'brak owocu', 'brak')

INSERT INTO kwiaty (id_kwiaty, id_informacje, pora_roku, cechy, kolor)  
VALUES (1, 1, 'lato', 'pojedyńcze', 'białe, różowe')

INSERT INTO warunki (id_warunki, id_informacje, miejsce, strefy_mrozoodpornosci) VALUES (1, 1, '6a', 'mrozoodporny' )

INSERT INTO gleba (id_gleba, id_warunki, pH, rodzaj, wilgotnosc) 
VALUES (1, 1, 'odczyn lekko kwaśny', 'przeciętna ogrodowa, próchnicza', 'podłoże umiarkowane wilgotne')

INSERT INTO liscie (id_liscie, id_warunki, wielkosc, kolor, ksztalt) VALUES (1, 1, '6cm', 'ciemnozielone', 'jajowaty')

-------------------------------------------------------
--Babtysja błękitna
use szkolka

INSERT INTO roslina (id_roslina, nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) 
VALUES (2, 'Baptisia austalis', 'okrytonasienne', 'brak informacji', 'brak informacji', 'Baptysja', 'Babtysja błękitna', 'USA', '0.5-1m', 'czerwiec, lipiec')
INSERT INTO stanowisko (id_stanowisko, strefa, rzad, miejsce) VALUES (2, '3', 'II', '10')
INSERT INTO informacje (id_informacje, id_roslina, nazwa, id_zastosowanie, id_stanowisko, ilosc_na_stanie, zywotnosc) 
VALUES (2, 2, 'Babtysja błękitna', 2, 2, 15, '2 lata' )
INSERT INTO owoce (id_owoce, id_informacje, obecnosc, barwa, rodzaj)  VALUES (2, 2,  'obecne', 'czarne', 'strąki')
INSERT INTO kwiaty (id_kwiaty, id_informacje, pora_roku, cechy, kolor)  VALUES (2, 2,'lato', 'pojedyńcze, kwiatostan', 'niebieskie')
INSERT INTO warunki (id_warunki, id_informacje, miejsce, tolerancja, strefy_mrozoodpornosci) 
VALUES (2, 2, 'stanowisko półcieniste, stanowisko słoneczne', 'roślina tolerancyjna', 'mrozoodporna' )
INSERT INTO gleba (id_gleba, id_warunki, pH, rodzaj, wilgotnosc) VALUES (2, 2, 'roślina tolerancyjna', 'roślina tolerancyjna', 'podłoże umiarkowanie wilgotne')
INSERT INTO liscie (id_liscie, id_warunki, wielkosc, kolor, ksztalt) VALUES (2, 2, '5 cm', 'jasnozielone', 'odwrotnie jajowate')

-------------------------------------------------------
--trzcinnik ostrokwiatowy 'Karl Foerster'

INSERT INTO roslina (id_roslina, nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) 
VALUES (3, 'Calamagrostis ×acutiflora', 'okrytonasienne', 'wiechlinowce', 'wiechlinowate', 'Trzcinnik', 'Trzcinnik ostrokwiatowy', 'USA', '1-2m', 'czerwiec, lipiec, sierpień')
INSERT INTO stanowisko (id_stanowisko, strefa, rzad, miejsce) VALUES (3, '4', 'II', '12')
INSERT INTO informacje (id_informacje, id_roslina, nazwa, id_zastosowanie, id_stanowisko) VALUES (3, 3, 'Trzcinnik ostrokwiatowy', 6, 3)
INSERT INTO owoce (id_owoce, id_informacje, obecnosc, barwa, rodzaj)  VALUES (3, 3,  'brak', 'brak', 'brak')
INSERT INTO kwiaty (id_kwiaty, id_informacje, pora_roku, cechy, kolor)  VALUES (3, 3,'czerwiec, lipiec, sierpień', 'kwiatostan', 'beżowe')
INSERT INTO warunki (id_warunki, id_informacje, miejsce, strefy_mrozoodpornosci) VALUES (3, 3, 'stanowisko słoneczne', 'mrozoodporna' )
INSERT INTO gleba (id_gleba, id_warunki, pH, rodzaj, wilgotnosc) VALUES (3, 3, 'roślina tolerancyjna', 'próchnicza, gliniasta', 'podłoże umiarkowanie wilgotne')
INSERT INTO liscie (id_liscie, id_warunki, wielkosc, kolor, ksztalt) VALUES (3, 3, '40-90 cm', 'ciemnozielone', 'łukowate')

-------------------------------------------------------
--dabecja kantabryjska forma biała

INSERT INTO roslina (id_roslina, nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) VALUES (4, 'Daboecia cantabrica f.alba', 'okrytonasienne', 'wrzosowce', 'wrzosowate', 'Dabecja', 'Dabecja kantabryjska', 'Szkocja', '0,2 - 0,5m', 'lipiec, sierpień, wrzesień, październik')
INSERT INTO stanowisko (id_stanowisko, strefa, rzad, miejsce) VALUES (4, '5', 'II', '10')
INSERT INTO informacje (id_informacje, id_roslina, nazwa, id_zastosowanie, id_stanowisko, ilosc_na_stanie) VALUES (4, 4, 'Dabecja kantabryjska', 4, 4, '15' )
INSERT INTO owoce (id_owoce, id_informacje, obecnosc, barwa, rodzaj)  VALUES (4, 4,  'brak', 'brak', 'brak')
INSERT INTO kwiaty (id_kwiaty, id_informacje, pora_roku, cechy, kolor)  VALUES (4, 4,'lipiec, sierpień, wrzesień, październik', 'pojedyńcze, kwiatostan', 'białe')
INSERT INTO warunki (id_warunki, id_informacje, miejsce, tolerancja) VALUES (4, 4, 'stanowisko słoneczne, stanowisko półcieniste', 'wymaga dobrego okrycia na zimę' )
INSERT INTO gleba (id_gleba, id_warunki, pH, rodzaj, wilgotnosc) VALUES (4, 4, 'odczyn kwaśny', 'próchnicza', 'podłoże umiarkowanie wilgotne')
INSERT INTO liscie (id_liscie, id_warunki, wielkosc, kolor) VALUES (4, 4, 'drobne', 'ciemnozielone')

---------------------------------------------------------
--jeżówka 'Cheyenne Spirit'
INSERT INTO roslina (id_roslina, nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) VALUES (5, 'Echinacea Cheyenne Spirit', 'okrytonasienne', 'astrowce', 'astrowate', 'Jeżówka', 'Jeżówka Cheyenne Spirit', 'Ameryka północna', '0,5 - 1m', 'lipiec, sierpień, wrzesień')
INSERT INTO stanowisko (id_stanowisko, strefa, rzad, miejsce) VALUES (5, '5', 'II', '15')
INSERT INTO informacje (id_informacje, id_roslina, nazwa, id_zastosowanie, id_stanowisko) VALUES (5, 5, 'Jeżówka Cheyenne Spirit', 5, 5 )
INSERT INTO owoce (id_owoce, id_informacje, obecnosc, barwa, rodzaj)  VALUES (5, 5,  'brak', 'brak', 'brak')
INSERT INTO kwiaty (id_kwiaty, id_informacje, pora_roku, cechy, kolor)  VALUES (5, 5,
'lipiec, sierpień, wrzesień', 'kwiatostan', ' kremowe, białe, bordowe, czerwone, pomarańczowe, purpurowe, łososiowe, żółte')
INSERT INTO warunki (id_warunki, id_informacje, miejsce, tolerancja) VALUES (5, 5, 'stanowisko słoneczne', 'wrażliwe na mrozy' )
INSERT INTO gleba (id_gleba, id_warunki, pH, rodzaj, wilgotnosc) VALUES (5, 5, 'tolerancyjna', 'tolerancyjna ', 'podłoże umiarkowanie wilgotne')
INSERT INTO liscie (id_liscie, id_warunki, wielkosc, kolor, ksztalt) VALUES (5, 5, '3cm', 'ciemnozielone', 'lancetowate')

------------------------------------------------------------
--miłorząb dwuklapowy 'Beijing Gold'
INSERT INTO roslina (id_roslina, nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) VALUES (6, 'Ginkgobiloba Beijing Gold', 'miłorzębowe', 'miłorzębowce', 'miłorzębowate', 'miłorząb', 'miłorząb dwuklapowy', 'Ameryka północna', '5 - 10m', 'późna wiosna')
INSERT INTO stanowisko (id_stanowisko, strefa, rzad, miejsce) VALUES (6, '5', 'III', '5')
INSERT INTO informacje (id_informacje, id_roslina, nazwa, id_zastosowanie, id_stanowisko, ilosc_na_stanie) VALUES (6, 6, 'miłorząb dwuklapowy Beijing Gold', 9, 6, '15')
INSERT INTO owoce (id_owoce, id_informacje, obecnosc)  VALUES (6, 6,  'brak')
INSERT INTO kwiaty (id_kwiaty, id_informacje, pora_roku, cechy, kolor)  VALUES (6, 6, 'maj', 'brak', 'brak')
INSERT INTO warunki (id_warunki, id_informacje, miejsce, tolerancja) VALUES (6, 6, 'stanowisko słoneczne, półcieniste', 'mrozoodporne')
INSERT INTO gleba (id_gleba, id_warunki, pH, rodzaj, wilgotnosc) VALUES (6, 6, 'odczyn kwaśny, odczyn lekko kwaśny', 'próchnicza, przeciętna ogrodowa ', 'podłoże umiarkowanie wilgotne')
INSERT INTO liscie (id_liscie, id_warunki, wielkosc, kolor, ksztalt) VALUES (6, 6, '3cm-5cm', 'ciemnozielone, żółte, złociste', 'szerokowachlarzowaty')

-------------------------------------------------------------
--heptakodium chińskie TIANSHAN 'Minhep'
INSERT INTO roslina (id_roslina, nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) VALUES (7, 'Heptacodium miconioides TIANSHAN Minhep', 'okrytonasienne', 'szczeciowce', 'przewiertniowate', 'heptacodium', 'Heptacodium miconioides', 'Francja', '2-3m', 'jesień')
INSERT INTO stanowisko (id_stanowisko, strefa, rzad, miejsce) VALUES (7, '5', 'III', '10')
INSERT INTO informacje (id_informacje, id_roslina, nazwa, id_zastosowanie, id_stanowisko, ilosc_na_stanie) VALUES (7, 7, 'Heptakodium chińskie', 1, 7, 15)
INSERT INTO owoce (id_owoce, id_informacje, obecnosc, rodzaj)  VALUES (7, 7,  'obecne', 'walcowate niełupki')
INSERT INTO kwiaty (id_kwiaty, id_informacje, pora_roku, cechy, kolor)  VALUES (7, 7,'wrzesień, październik', 'pojedyncze, kwiatostan', 'czerwone')
INSERT INTO warunki (id_warunki, id_informacje, miejsce, tolerancja) VALUES (7, 7, 'stanowisko słoneczne, półcieniste', 'mrozoodporne' )
INSERT INTO gleba (id_gleba, id_warunki, pH, rodzaj, wilgotnosc) VALUES (7, 7, 'tolerancyjna', 'przeciętna ogrodowa ', 'tolerancyjna')
INSERT INTO liscie (id_liscie, id_warunki, wielkosc, kolor, ksztalt) VALUES (7, 7, '8cm-15cm', 'ciemnozielone', 'szerokojajowata')

---------------------------------------------------------------
--kolcowój szkarłatny 'New Big'
INSERT INTO roslina (id_roslina, nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) VALUES (8, 'Lycium barbarum New Big', 'okrytonasienne', 'psiankowce', 'psiankowate', 'kolcowój', 'Kolcowój pospolity', 'Chiny', '2-3m', 'lato')
INSERT INTO stanowisko (id_stanowisko, strefa, rzad, miejsce) VALUES (8, '5', 'III', '15')
INSERT INTO informacje (id_informacje, id_roslina, nazwa, id_zastosowanie, id_stanowisko, ilosc_na_stanie) VALUES (8, 8, 'kolcowój szkarłatny New Big', 2, 8, '15')
INSERT INTO owoce (id_owoce, id_informacje, obecnosc, barwa, rodzaj)  VALUES (8, 8,  'obecne', 'czerwone', 'jagody Goji')
INSERT INTO kwiaty (id_kwiaty, id_informacje, pora_roku, cechy, kolor)  VALUES (8, 8,'czerwiec, lipiec, sierpień', 'pojedyncze', 'fioletowe, purpurowe')
INSERT INTO warunki (id_warunki, id_informacje, miejsce, tolerancja) VALUES (8, 8, 'stanowisko słoneczne, półcieniste', 'mrozoodporne')
INSERT INTO gleba (id_gleba, id_warunki, pH, rodzaj, wilgotnosc) VALUES (8, 8, 'odczyn lekko kwaśny', 'przeciętna ogrodowa', 'podłoże umiarkowanie wilgotne, roślina tolerancyjna')
INSERT INTO liscie (id_liscie, id_warunki, wielkosc, kolor, ksztalt) VALUES (8, 8, '6cm', 'jasnozielone', 'lancetowate')

-----------------------------------------------------------------
--magnolia 'Ann'
INSERT INTO roslina (id_roslina, nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) VALUES (9, 'Magnolia Ann', 'okrytonasienne', 'magnoliowce', 'magnoliowate', 'magnolia', 'Magnolia Ann', 'USA', '3-5m', 'późna wiosna')
INSERT INTO stanowisko (id_stanowisko, strefa, rzad, miejsce) VALUES (9, '5', 'III', '20')
INSERT INTO informacje (id_informacje, id_roslina, nazwa, id_zastosowanie, id_stanowisko, ilosc_na_stanie) VALUES (9, 9, 'Magnolia Ann', 3, 9, '15')
INSERT INTO owoce (id_owoce, id_informacje, obecnosc, rodzaj)  VALUES (9, 9,  'obecne', 'liczne mieszki')
INSERT INTO kwiaty (id_kwiaty, id_informacje, pora_roku, cechy, kolor)  VALUES (9, 9,'kwiecień, maj', 'pojedyncze', 'purpurowe, różowe')
INSERT INTO warunki (id_warunki, id_informacje, miejsce, tolerancja) VALUES (9, 9, 'stanowisko słoneczne, półcieniste', 'mrozoodporne')
INSERT INTO gleba (id_gleba, id_warunki, pH, rodzaj, wilgotnosc) VALUES (9, 9, 'odczyn lekko kwaśny', 'próchnicza', 'podłoże umiarkowanie wilgotne')
INSERT INTO liscie (id_liscie, id_warunki, wielkosc, kolor, ksztalt) VALUES (9, 9, '10cm-15cm', 'jasnozielone', 'owalne')

--------------------------------------------------------------------
--lebiodka gładka 'Herrenhausen'
INSERT INTO roslina (id_roslina, nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) VALUES (10, 'riganum laevigatum Herrenhausen', 'okrytonasienne', 'jasnotowce', 'jasnotowate', 'Lebiodka', 'Lebiodka gładka', '-', '0,2-0,5m', 'lato')
INSERT INTO stanowisko (id_stanowisko, strefa, rzad, miejsce) VALUES (10, '5', 'III', '25')
INSERT INTO informacje (id_informacje, id_roslina, nazwa, id_zastosowanie, id_stanowisko, ilosc_na_stanie) VALUES (10, 10, 'Lebiodka gładka', 5, 10, '15' )
INSERT INTO owoce (id_owoce, id_informacje, obecnosc, rodzaj)  VALUES (10, 10,  'obecne', 'czterodzielne rozłupnie')
INSERT INTO kwiaty (id_kwiaty, id_informacje, pora_roku, cechy, kolor)  VALUES (10, 10,'lipiec, sierpień', 'pojedyncze, kwiatostan','rożowe')
INSERT INTO warunki (id_warunki, id_informacje, miejsce, tolerancja) VALUES (10, 10, 'stanowisko słoneczne', 'brak mrozoodporności')
INSERT INTO gleba (id_gleba, id_warunki, pH, rodzaj, wilgotnosc) VALUES (9, 9, 'zasadowe', 'czarnoziem' ,'podłoże suche, umiarkowanie wilgotne')
INSERT INTO liscie (id_liscie, id_warunki, wielkosc, kolor, ksztalt) VALUES (10, 10, '1cm-2cm', 'czerwone, purpurowe, jasnozielone', 'lancetowate')


-----------------------------------------------------
--query
select * from owoce;
select * from informacje where id_roslina = 4;
select wilgotnosc from gleba where id_warunki in (select id_warunki from warunki where id_informacje in(select id_informacje from informacje where nazwa = 'Dabecja kantabryjska'))

