import pyodbc
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

window = tkinter.Tk()
window.title("Green plant") #window name

canvas = tk.Canvas(window, height=500, width = 600)
canvas.pack()
image = Image.open("liscie.png")
background_image = ImageTk.PhotoImage(image)
background_label = tk.Label(window, image=background_image)
background_label.place(relwidth=1, relheight=1)

#tekst
w1 = Label(window, text="SZKÓŁKA ROŚLIN", fg='#669966', bg = 'white' ,font=("Arial", 20, "bold"))#,"bold"))
w1.place(x=180,y=10)


#### CONNECTION TO DATABASE ####
conn = pyodbc.connect('Driver={SQL Server};'
                   'Server=LAPTOP-SCO4KAMB\SQLEXPRESS01;'
                   'Database=szkolka_2;'
                   'Trusted_Connection=yes;')

cursor = conn.cursor()

################## WYSZUKIWARKA ##################
frame = tk.Frame(window, bg='#669966', bd=4)
frame.place(relx=0.5, rely=0.15, relwidth=0.8,relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.55, relheight=1,x=5)

#ramka do odpowiedzi
lower_frame = tk.Frame(window, bg='#669966', bd=10)
lower_frame.place(relx=0.5, rely=0.30, relheight=0.6, relwidth=0.75, anchor='n')

label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)

#WYSZUKAJ ROŚLINĘ
def szukaj_rosline():

    #komenda sql
    cursor.execute(
    "select nazwa, ilosc_na_stanie, zywotnosc, id_stanowisko from szkolka_2.dbo.informacje WHERE nazwa = ?",
    entry.get()
    )
    
    #view results
    records = cursor.fetchmany() #przechwytuje wszystkie odpowiedzi
    nazwy = ["Nazwa: ", "Ilość na stanie: ", "Żywotność: ", "Stanowisko: "]
    #odpowiedz po przycisku szukaj
    Lbl = Listbox(lower_frame)
    tab = []
    for row in records:
        for i in range(0, 4):
            tab.append(nazwy[i] + str(row[i]))

    for i in range(1,5):
        Lbl.insert(i, tab[i-1])
    Lbl.place(relx=0.5, rely=0, relheight=1, relwidth=1, anchor='n')
 
    # Clear the text boxes
    entry.delete(0, END)

#create button
button = tk.Button(frame, text="Szukaj roślinę po nazwie", font=40, command=szukaj_rosline)
button.place(relx=0.6, relwidth=0.4, relheight=1, x=-5)

##################MENU#########################

#FUNKCJA DODAJ ROŚLINĘ - NOWE OKNO
def dodaj():
    
    root = Tk()
    root.title('Dodaj roslinę')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    
    zmienne = ["nazwa", "ilosc_na_stanie","zywotnosc", "nazwa_lacinska", "klasa", "rzad",
               "rodzina","rodzaj", "gatunek", "pochodzenie", "wysokosc_rosliny",
               "okres_kwitnienia"]

    teksty = ["Nazwa rośliny", "Ilość na stanie","Żywotność", "Nazwa łacińska","Klasa","Rząd","Rodzina",
              "Rodzaj","Gatunek","Pochodzenie","Wysokość rośliny","Okres kwitnienia"]

    #Stworzenie textboxow
    nowe_zmienne = []
    for k in range(0,len(zmienne)):
        nowe_zmienne.append(zmienne[k]+'_label')
        zmienne[k] = Entry(root, width=30)
        zmienne[k].grid(row=k, column=1, padx=20)

    #stworzenie labels do textboxow
    for i in range(0, len(nowe_zmienne)):
        nowe_zmienne[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        nowe_zmienne[i].grid(row=i, column=0)

    #do dodania danych do bazy danych
    def dodaj_rosline():

        #komenda sql
        cursor.execute(
        "INSERT INTO szkolka_2.dbo.roslina(nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
        zmienne[3].get(),
        zmienne[4].get(),
        zmienne[5].get(),
        zmienne[6].get(),
        zmienne[7].get(),
        zmienne[8].get(),
        zmienne[9].get(),
        zmienne[10].get(),
        zmienne[11].get()
        )

        cursor.execute(
        "INSERT INTO szkolka_2.dbo.informacje(nazwa, ilosc_na_stanie, zywotnosc id_roslina) VALUES(?, ?, ?, (SELECT max(id_roslina) FROM roslina))",
            zmienne[0].get(),
            zmienne[1].get(),
            zmienne[2].get()
        )


        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="Roślina została dodana pomyślnie.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)
        #potwierdzenie.place(x=20, y=120)

        # Clear the text boxes
        for l in range(0, len(zmienne)):
            zmienne[l].delete(0, END)


    #create button
    submit_btn = Button(root, text="Dodaj", command=dodaj_rosline, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)

###########
#FUNKCJA USUN ROŚLINĘ - NOWE OKNO
def usun():
    root = Tk()
    root.title('Usuń roslinę')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    nazwa_lacinska = Entry(root, width=30) #do tabeli roslina
    nazwa_lacinska.grid(row=2, column=1)

    nazwa_lacinska_label = Label(root, text="Nazwa łacińska", fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
    nazwa_lacinska_label.grid(row=2, column=0)

    def usun_rosline():

        cursor.execute(
        "DELETE FROM szkolka_2.dbo.informacje where id_roslina = (SELECT id_roslina from szkolka_2.dbo.roslina where szkolka_2.dbo.roslina.nazwa_lacinska = ?); DELETE FROM szkolka_2.dbo.roslina WHERE nazwa_lacinska = ?",
            nazwa_lacinska.get(),
            nazwa_lacinska.get()        
        )

        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie_usun = Label(root, text="Roślina została usunięta pomyślnie.", fg='black', bg = '#E2FFB7')
        potwierdzenie_usun.grid(row=4, column=1)
        #potwierdzenie.place(x=20, y=120)
        
        # Clear the text boxes
        nazwa_lacinska.delete(0, END)


    # Create submit button to add entries
    submit_btn = Button(root, text="Usuń", command=usun_rosline, width=10)
    submit_btn.grid(row=6, column=1, columnspan=2, pady=10, padx=10)

#########
#FUNKCJA ZMIEN ILOSC NA STANE- NOWE OKNO
def ilosc():
    root = Tk()
    root.title('Zmień ilość')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    # Create text boxes
    nazwa = Entry(root, width=30) #do tab informacje
    nazwa.grid(row=0, column=1, padx=20)

    ilosc_na_stanie = Entry(root, width=30) #do tabeli roslina
    ilosc_na_stanie.grid(row=2, column=1)

    nazwa_label = Label(root, text="Nazwa rośliny", fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
    nazwa_label.grid(row=0, column=0)
    
    ilosc_na_stanie_label = Label(root, text="Zmień ilość", fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
    ilosc_na_stanie_label.grid(row=2, column=0) 

    def zmien_ilosc():

        # Insert into table
        cursor.execute(
        "UPDATE szkolka_2.dbo.informacje SET ilosc_na_stanie = ? where nazwa = ?",
            ilosc_na_stanie.get(),
            nazwa.get()
        )

        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie_ilosc = Label(root, text="Ilość na stanie została zmieniona.", fg='black', bg = '#E2FFB7')
        potwierdzenie_ilosc.grid(row=4, column=1)
        #potwierdzenie.place(x=20, y=120)
        
        # Clear the text boxes
        nazwa.delete(0, END)
        ilosc_na_stanie.delete(0, END)


    # Create submit button to add entries
    submit_btn = Button(root, text="Zmień", command=zmien_ilosc, width=10)
    submit_btn.grid(row=6, column=1, columnspan=2, pady=10, padx=10)


################
#FUNKCJA DODAJ INFORMACJE O UPRAWIE
def uprawa():
    root = Tk()
    root.title('Dodaj informacje o uprawie')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    zmienne = ["nazwa","nawadnianie", "nawozenie", "rodzaj nawozu"]

    teksty = ["Nazwa rośliny","Nawadnianie", "Nawożenie", "Rodzaj użytego nawozu"]

    #Stworzenie textboxow
    nowe_zmienne = []
    for k in range(0,len(zmienne)):
        nowe_zmienne.append(zmienne[k]+'_label')
        zmienne[k] = Entry(root, width=30)
        zmienne[k].grid(row=k, column=1, padx=20)

    #stworzenie labels do textboxow
    for i in range(0, len(nowe_zmienne)):
        nowe_zmienne[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        nowe_zmienne[i].grid(row=i, column=0)

    #do dodania danych do bazy danych
    def dodaj_uprawe():

        #komenda sql
        cursor.execute(
        "INSERT INTO szkolka_2.dbo.uprawa(nawadnianie, nawozenie, rodzaj_nawozu, id_informacje) VALUES(?, ?, ?, (SELECT id_informacje FROM informacje where nazwa = ?))",
            zmienne[1].get(),
            zmienne[2].get(),
            zmienne[3].get(),
            zmienne[0].get()
        )

        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="Informacja o uprawie została dodana.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)
        #potwierdzenie.place(x=20, y=120)

        # Clear the text boxes
        for l in range(0, len(zmienne)):
            zmienne[l].delete(0, END)


    #create button
    submit_btn = Button(root, text="Dodaj", command=dodaj_uprawe, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)


#################### KLIENCI ########################
#FUNKCJA DODAJ KLIENTA - NOWE OKNO
def dodaj_klienta():
    
    root = Tk()
    root.title('Dodaj klienta')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    zmienne = ["imie", "nazwisko","adres", "numer_telefonu", "e_mail"]

    teksty = ["Imię", "Nazwisko", "Adres", "Numer telefonu", "E_mail"]

    #Stworzenie textboxow
    nowe_zmienne = []
    for k in range(0,len(zmienne)):
        nowe_zmienne.append(zmienne[k]+'_label')
        zmienne[k] = Entry(root, width=30)
        zmienne[k].grid(row=k, column=1, padx=20)

    #stworzenie labels do textboxow
    for i in range(0, len(nowe_zmienne)):
        nowe_zmienne[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        nowe_zmienne[i].grid(row=i, column=0)

    #do dodania danych do bazy danych
    def dodaj_klienta_baza():

        #komenda sql
        cursor.execute(
        "INSERT INTO szkolka_2.dbo.klienci(imie, nazwisko, adres, numer_telefonu, e_mail) VALUES(?, ?, ?, ?, ?)",
        zmienne[0].get(),
        zmienne[1].get(),
        zmienne[2].get(),
        zmienne[3].get(),
        zmienne[4].get()
        )

        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="Nowy klient został dodany pomyślnie.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)
        #potwierdzenie.place(x=20, y=120)

        # Clear the text boxes
        for l in range(0, len(zmienne)):
            zmienne[l].delete(0, END)


    #create button
    submit_btn = Button(root, text="Dodaj", command=dodaj_klienta_baza, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)

###########
#FUNKCJA USUN KLIENTA - NOWE OKNO
def usun_klienta():
    
    root = Tk()
    root.title('Usuń klienta')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    zmienne = ["imie", "nazwisko"]

    teksty = ["Imię", "Nazwisko"]

    #Stworzenie textboxow
    nowe_zmienne = []
    for k in range(0,len(zmienne)):
        nowe_zmienne.append(zmienne[k]+'_label')
        zmienne[k] = Entry(root, width=30)
        zmienne[k].grid(row=k, column=1, padx=20)

    #stworzenie labels do textboxow
    for i in range(0, len(nowe_zmienne)):
        nowe_zmienne[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        nowe_zmienne[i].grid(row=i, column=0)

    #do dodania danych do bazy danych
    def usun_klienta_baza():

        #komenda sql
        cursor.execute(
        "DELETE FROM szkolka_2.dbo.klienci WHERE imie = ? and nazwisko = ?",
        zmienne[0].get(),
        zmienne[1].get()
        )

        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="Klient został usunięty pomyślnie.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)
        #potwierdzenie.place(x=20, y=120)

        # Clear the text boxes
        for l in range(0, len(zmienne)):
            zmienne[l].delete(0, END)


    #create button
    submit_btn = Button(root, text="Usuń", command=usun_klienta_baza, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)


###########
#FUNKCJA SZUKAJ KLIENTA - NOWE OKNO
def szukaj_klienta():
    
    root = Tk()
    root.title('Wyszukaj klienta')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    zmienne = ["imie", "nazwisko"]

    teksty = ["Imię", "Nazwisko"]

    #Stworzenie textboxow
    nowe_zmienne = []
    for k in range(0,len(zmienne)):
        nowe_zmienne.append(zmienne[k]+'_label')
        zmienne[k] = Entry(root, width=30)
        zmienne[k].grid(row=k, column=1, padx=20)

    #stworzenie labels do textboxow
    for i in range(0, len(nowe_zmienne)):
        nowe_zmienne[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        nowe_zmienne[i].grid(row=i, column=0)

    #do dodania danych do bazy danych
    def szukaj_klienta_baza():

        #komenda sql
        cursor.execute(
        "select imie, nazwisko, adres, numer_telefonu, e_mail from szkolka_2.dbo.klienci WHERE imie = ? and nazwisko = ?",
        zmienne[0].get(),
        zmienne[1].get()
        )
        
        #view results
        records = cursor.fetchmany() #przechwytuje wszystkie odpowiedzi
        nazwy = ["Imię: ", "Nazwisko: ", "Adres: ", "Numer telefonu: ", "Adres e-mail: "]
        #odpowiedz po przycisku szukaj
        Lbl = Listbox(root)

        tab = []
        for row in records:
            for i in range(0, 5):
                tab.append(nazwy[i] + str(row[i]))
    
        for i in range(1,6):
            Lbl.insert(i, tab[i-1])
        Lbl.place(relx=0.5, rely=0.3, relheight=0.6, relwidth=0.75, anchor='n')

        
        # Clear the text boxes
        for l in range(0, len(zmienne)):
            zmienne[l].delete(0, END)

    #create button
    submit_btn = Button(root, text="Szukaj", command=szukaj_klienta_baza, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)

    
################## ZAMOWIENIA ##################

#####NOWE ZAMOWIENIE
def nowe_zamowienie():
    
    root = Tk()
    root.title('Nowe zamówienie')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    zmienne = ["imie", "nazwisko", "nazwa", "ilosc", "data_zamowienia", "data_odbioru", "cena"]

    teksty = ["Imię", "Nazwisko", "Nazwa", "Ilość", "Data zamówienia", "Data odbioru", "Cena"]

    #Stworzenie textboxow
    nowe_zmienne = []
    for k in range(0,len(zmienne)):
        nowe_zmienne.append(zmienne[k]+'_label')
        zmienne[k] = Entry(root, width=30)
        zmienne[k].grid(row=k, column=1, padx=20)

    #stworzenie labels do textboxow
    for i in range(0, len(nowe_zmienne)):
        nowe_zmienne[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        nowe_zmienne[i].grid(row=i, column=0)

    #do dodania danych do bazy danych
    def dodaj_zamowienie():

        #komenda sql    
        cursor.execute(
        "INSERT INTO szkolka_2.dbo.zamowienia(ilosc, data_zamowienia, data_odbioru, cena, id_informacje, id_klient) VALUES(?, ?, ?, ?, (SELECT id_informacje FROM informacje where nazwa = ?),(SELECT id_klient FROM klienci where imie = ? and nazwisko = ?))",
        zmienne[3].get(),
        zmienne[4].get(),
        zmienne[5].get(),
        zmienne[6].get(),
        zmienne[2].get(),
        zmienne[0].get(),
        zmienne[1].get()
        )

        
        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="Nowe zamówienie zostało dodane pomyślnie.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)
        #potwierdzenie.place(x=20, y=120)

        # Clear the text boxes
        for l in range(0, len(zmienne)):
            zmienne[l].delete(0, END)


    #create button
    submit_btn = Button(root, text="Złóż", command=dodaj_zamowienie, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)

##### NOWE ZAMOWIENIE ######
def usun_zamowienie():
    
    root = Tk()
    root.title('Usuń zamówienie')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    numer = Entry(root, width=30) #do tabeli roslina
    numer.grid(row=2, column=1)

    numer_label = Label(root, text="Numer zamówienia", fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
    numer_label.grid(row=2, column=0)

    #do dodania danych do bazy danych
    def usun():

        cursor.execute(
        "DELETE FROM szkolka_2.dbo.zamowienia WHERE id_zamowienia = ?",
        numer.get()
        )

        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="Zamówienie zostało usunięte pomyślnie.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)

        # Clear the text boxes
        numer.delete(0, END)


    #create button
    submit_btn = Button(root, text="Usuń", command=usun, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)

    
########POKAZ ZAMOWIENIA###########
def szukaj_zamowienie():
    
    root = Tk()
    root.title('Wyszukaj zamówienie')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    data = Entry(root, width=30)
    data.grid(row=2, column=1)

    data_label = Label(root, text="Data zamówienia", fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
    data_label.grid(row=2, column=0)

    #do dodania danych do bazy danych
    def szukaj_data():

        cursor.execute(
        "select i.nazwa, z.id_zamowienia, z.ilosc, z.data_zamowienia, z.data_odbioru, z.cena FROM szkolka_2.dbo.zamowienia z left join szkolka_2.dbo.informacje i on i.id_informacje = z.id_informacje left join szkolka_2.dbo.klienci k on k.id_klient = z.id_klient where z.data_zamowienia = ?",
        data.get()
        )

        #view results
        records = cursor.fetchmany() #przechwytuje wszystkie odpowiedzi
        nazwy = ["Nazwa: ","Numer zamówienia: ", "Ilość: ", "Data zamówienia: ", "Data odbioru: ", "Cena: "]
        #odpowiedz po przycisku szukaj
        Lbl = Listbox(root)
        tab = []
        for row in records:
            print(row)
        for row in records:
            for i in range(0, 6):
                tab.append(str(nazwy[i]) + str(row[i]))
    
        for i in range(1,7):
            Lbl.insert(i, tab[i-1])
        Lbl.grid(row=11, column=1)
        Lbl.place(relx=0.5, rely=0.3, relheight=0.6, relwidth=0.75, anchor='n')

        
        # Clear the text boxes
        data.delete(0, END)


    #create button
    submit_btn = Button(root, text="Szukaj", command=szukaj_data, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)
    
######################## MENU ###############################

menubar = Menu(window)
podmenu1 = Menu(window)
podmenu2 = Menu(window)
podmenu3 = Menu(window)
submenu = Menu(window)


filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menu", menu=filemenu)

#zrobione
filemenu.add_command(label="Dodaj roślinę", command=dodaj)
filemenu.add_command(label="Usuń roślinę", command=usun)
filemenu.add_command(label="Zmień ilość", command=ilosc)

filemenu.add_command(label="Dodaj informację o uprawie", command=uprawa)

#DRUGIE MENU ZAMOWIENIA
zammenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Zamówienia", menu=zammenu)

zammenu.add_command(label="Nowe zamówienie", command=nowe_zamowienie)
zammenu.add_command(label="Usuń zamówienie", command=usun_zamowienie)

zammenu.add_cascade(label="Wyszukaj zamówienie", menu=podmenu3)
podmenu3.add_command(label="Szukaj po dacie", command=szukaj_zamowienie)

#MENU 3 klienci
menu3 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Klienci", menu=menu3)

menu3.add_command(label="Dodaj klienta", command=dodaj_klienta)
menu3.add_command(label="Usuń klienta", command=usun_klienta)
menu3.add_command(label="Szukaj klienta", command=szukaj_klienta)

window.config(menu=menubar)
        
window.mainloop() #wyswietlenie okna

# Close connection
conn.close()

