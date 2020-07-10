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

#text
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

#answer
lower_frame = tk.Frame(window, bg='#669966', bd=10)
lower_frame.place(relx=0.5, rely=0.30, relheight=0.6, relwidth=0.75, anchor='n')

label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)

#search for a plant
def search_plant():

    #sql
    cursor.execute(
    "select nazwa, ilosc_na_stanie, zywotnosc, id_stanowisko from szkolka_2.dbo.informacje WHERE nazwa = ?",
    entry.get()
    )
    
    #view results
    records = cursor.fetchmany() #przechwytuje wszystkie odpowiedzi
    nazwy = ["Nazwa: ", "Ilość na stanie: ", "Żywotność: ", "Stanowisko: "]
    #answer after search button
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
button = tk.Button(frame, text="Szukaj roślinę po nazwie", font=40, command=search_plant)
button.place(relx=0.6, relwidth=0.4, relheight=1, x=-5)

##################MENU#########################

#ADD PLANT FUNCTION - NEW WINDOW
def add():
    
    root = Tk()
    root.title('Dodaj roslinę')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    
    variables = ["nazwa", "ilosc_na_stanie","zywotnosc", "nazwa_lacinska", "klasa", "rzad",
               "rodzina","rodzaj", "gatunek", "pochodzenie", "wysokosc_rosliny",
               "okres_kwitnienia"]

    teksty = ["Nazwa rośliny", "Ilość na stanie","Żywotność", "Nazwa łacińska","Klasa","Rząd","Rodzina",
              "Rodzaj","Gatunek","Pochodzenie","Wysokość rośliny","Okres kwitnienia"]

    #textboxes
    new_variables = []
    for k in range(0,len(variables)):
        new_variables.append(variables[k]+'_label')
        variables[k] = Entry(root, width=30)
        variables[k].grid(row=k, column=1, padx=20)

    #labels for textboxes
    for i in range(0, len(new_variables)):
        new_variables[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        new_variables[i].grid(row=i, column=0)

    #to add data to the database
    def add_plant():

        #sql
        cursor.execute(
        "INSERT INTO szkolka_2.dbo.roslina(nazwa_lacinska, klasa, rzad, rodzina, rodzaj, gatunek, pochodzenie, wysokosc_rosliny, okres_kwitnienia) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
        variables[3].get(),
        variables[4].get(),
        variables[5].get(),
        variables[6].get(),
        variables[7].get(),
        variables[8].get(),
        variables[9].get(),
        variables[10].get(),
        variables[11].get()
        )

        cursor.execute(
        "INSERT INTO szkolka_2.dbo.informacje(nazwa, ilosc_na_stanie, zywotnosc id_roslina) VALUES(?, ?, ?, (SELECT max(id_roslina) FROM roslina))",
            variables[0].get(),
            variables[1].get(),
            variables[2].get()
        )


        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="Roślina została dodana pomyślnie.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)

        # Clear the text boxes
        for l in range(0, len(variables)):
            variables[l].delete(0, END)


    #create button
    submit_btn = Button(root, text="Dodaj", command=add_plant, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)

###########
#DELETE PLANT - NEW WINDOW
def delete():
    root = Tk()
    root.title('Usuń roslinę')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    nazwa_lacinska = Entry(root, width=30) #do tabeli roslina
    nazwa_lacinska.grid(row=2, column=1)

    nazwa_lacinska_label = Label(root, text="Nazwa łacińska", fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
    nazwa_lacinska_label.grid(row=2, column=0)

    def delete_plant():

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
        
        # Clear the text boxes
        nazwa_lacinska.delete(0, END)


    # Create submit button to add entries
    submit_btn = Button(root, text="Usuń", command=delete_plant, width=10)
    submit_btn.grid(row=6, column=1, columnspan=2, pady=10, padx=10)

#########
 #CHANGE QUANTITY
def quantity():
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

    def change_quantity():

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
    submit_btn = Button(root, text="Zmień", command=change_quantity, width=10)
    submit_btn.grid(row=6, column=1, columnspan=2, pady=10, padx=10)


################
# ADD CROPPING INFORMATION
def cropp():
    root = Tk()
    root.title('Dodaj informacje o uprawie')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    variables = ["nazwa","nawadnianie", "nawozenie", "rodzaj nawozu"]

    teksty = ["Nazwa rośliny","Nawadnianie", "Nawożenie", "Rodzaj użytego nawozu"]

    #textboxes
    new_variables = []
    for k in range(0,len(variables)):
        new_variables.append(variables[k]+'_label')
        variables[k] = Entry(root, width=30)
        variables[k].grid(row=k, column=1, padx=20)

    #labels for textboxes
    for i in range(0, len(new_variables)):
        new_variables[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        new_variables[i].grid(row=i, column=0)

    #database
    def add_crop():

        #sql
        cursor.execute(
        "INSERT INTO szkolka_2.dbo.uprawa(nawadnianie, nawozenie, rodzaj_nawozu, id_informacje) VALUES(?, ?, ?, (SELECT id_informacje FROM informacje where nazwa = ?))",
            variables[1].get(),
            variables[2].get(),
            variables[3].get(),
            variables[0].get()
        )

        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="Informacja o uprawie została dodana.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)
        #potwierdzenie.place(x=20, y=120)

        # Clear the text boxes
        for l in range(0, len(variables)):
            variables[l].delete(0, END)


    #create button
    submit_btn = Button(root, text="Dodaj", command=add_crop, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)


#################### KLIENCI ########################
#ADD CUSTOMER - NEW WINDOW
def add_customer():
    
    root = Tk()
    root.title('Dodaj klienta')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    variables = ["imie", "nazwisko","adres", "numer_telefonu", "e_mail"]

    teksty = ["Imię", "Nazwisko", "Adres", "Numer telefonu", "E_mail"]

    #textboxes
    new_variables = []
    for k in range(0,len(variables)):
        new_variables.append(variables[k]+'_label')
        variables[k] = Entry(root, width=30)
        variables[k].grid(row=k, column=1, padx=20)

    #labels for textboxes
    for i in range(0, len(new_variables)):
        new_variables[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        new_variables[i].grid(row=i, column=0)

    #database
    def add_customer_db():

        #sql
        cursor.execute(
        "INSERT INTO szkolka_2.dbo.klienci(imie, nazwisko, adres, numer_telefonu, e_mail) VALUES(?, ?, ?, ?, ?)",
        variables[0].get(),
        variables[1].get(),
        variables[2].get(),
        variables[3].get(),
        variables[4].get()
        )

        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="Nowy klient został dodany pomyślnie.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)
        #potwierdzenie.place(x=20, y=120)

        # Clear the text boxes
        for l in range(0, len(variables)):
            variables[l].delete(0, END)


    #create button
    submit_btn = Button(root, text="Dodaj", command=add_customer_db, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)

###########
#DELETE CUSTOMER - NEW WINDOW
def delete_customer():
    
    root = Tk()
    root.title('Usuń klienta')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    variables = ["imie", "nazwisko"]

    teksty = ["Imię", "Nazwisko"]

    #textboxes
    new_variables = []
    for k in range(0,len(variables)):
        new_variables.append(variables[k]+'_label')
        variables[k] = Entry(root, width=30)
        variables[k].grid(row=k, column=1, padx=20)

    #labels for textboxes
    for i in range(0, len(new_variables)):
        new_variables[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        new_variables[i].grid(row=i, column=0)

    #database
    def delete_customer_db():

        #sql
        cursor.execute(
        "DELETE FROM szkolka_2.dbo.klienci WHERE imie = ? and nazwisko = ?",
        variables[0].get(),
        variables[1].get()
        )

        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="Klient został usunięty pomyślnie.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)
        #potwierdzenie.place(x=20, y=120)

        # Clear the text boxes
        for l in range(0, len(variables)):
            variables[l].delete(0, END)


    #create button
    submit_btn = Button(root, text="Usuń", command=delete_customer_db, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)


###########
#FUNKCJA CUSTOMER SEARCH - NEW WINDOW
def customer_search():
    
    root = Tk()
    root.title('Wyszukaj klienta')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    variables = ["imie", "nazwisko"]

    teksty = ["Imię", "Nazwisko"]

    #textboxes
    new_variables = []
    for k in range(0,len(variables)):
        new_variables.append(variables[k]+'_label')
        variables[k] = Entry(root, width=30)
        variables[k].grid(row=k, column=1, padx=20)

    #labels for textboxes
    for i in range(0, len(new_variables)):
        new_variables[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        new_variables[i].grid(row=i, column=0)

    #database
    def customer_search_db():

        #sql
        cursor.execute(
        "select imie, nazwisko, adres, numer_telefonu, e_mail from szkolka_2.dbo.klienci WHERE imie = ? and nazwisko = ?",
        variables[0].get(),
        variables[1].get()
        )
        
        #view results
        records = cursor.fetchmany() #przechwytuje wszystkie odpowiedzi
        nazwy = ["Imię: ", "Nazwisko: ", "Adres: ", "Numer telefonu: ", "Adres e-mail: "]
        #answer after search button
        Lbl = Listbox(root)

        tab = []
        for row in records:
            for i in range(0, 5):
                tab.append(nazwy[i] + str(row[i]))
    
        for i in range(1,6):
            Lbl.insert(i, tab[i-1])
        Lbl.place(relx=0.5, rely=0.3, relheight=0.6, relwidth=0.75, anchor='n')

        
        # Clear the text boxes
        for l in range(0, len(variables)):
            variables[l].delete(0, END)

    #create button
    submit_btn = Button(root, text="Szukaj", command=customer_search_db, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)

    
################## ORDERS ##################

#####new order
def new_order():
    
    root = Tk()
    root.title('new zamówienie')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    variables = ["imie", "nazwisko", "nazwa", "ilosc", "data_zamowienia", "data_odbioru", "cena"]

    teksty = ["Imię", "Nazwisko", "Nazwa", "Ilość", "Data zamówienia", "Data odbioru", "Cena"]

    #textboxes
    new_variables = []
    for k in range(0,len(variables)):
        new_variables.append(variables[k]+'_label')
        variables[k] = Entry(root, width=30)
        variables[k].grid(row=k, column=1, padx=20)

    #labels for textboxes
    for i in range(0, len(new_variables)):
        new_variables[i] = Label(root, text=teksty[i], fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
        new_variables[i].grid(row=i, column=0)

    #database
    def add_order():

        #sql    
        cursor.execute(
        "INSERT INTO szkolka_2.dbo.zamowienia(ilosc, data_zamowienia, data_odbioru, cena, id_informacje, id_klient) VALUES(?, ?, ?, ?, (SELECT id_informacje FROM informacje where nazwa = ?),(SELECT id_klient FROM klienci where imie = ? and nazwisko = ?))",
        variables[3].get(),
        variables[4].get(),
        variables[5].get(),
        variables[6].get(),
        variables[2].get(),
        variables[0].get(),
        variables[1].get()
        )

        
        # Commit changes
        conn.commit()

        #response after press button
        potwierdzenie = Label(root, text="new zamówienie zostało dodane pomyślnie.", fg='black', bg = '#E2FFB7')
        potwierdzenie.grid(row=11, column=1)
        #potwierdzenie.place(x=20, y=120)

        # Clear the text boxes
        for l in range(0, len(variables)):
            variables[l].delete(0, END)


    #create button
    submit_btn = Button(root, text="Złóż", command=add_order, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)

##### DELETE ORDER ######
def delete_order():
    
    root = Tk()
    root.title('Usuń zamówienie')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    numer = Entry(root, width=30) #do tabeli roslina
    numer.grid(row=2, column=1)

    numer_label = Label(root, text="Numer zamówienia", fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
    numer_label.grid(row=2, column=0)

    #database
    def delete():

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
    submit_btn = Button(root, text="Usuń", command=delete, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)

    
########SHOW ORDERS###########
def search_order():
    
    root = Tk()
    root.title('Wyszukaj zamówienie')
    root.geometry("400x300")
    root.configure(bg = '#669966') #background color

    data = Entry(root, width=30)
    data.grid(row=2, column=1)

    data_label = Label(root, text="Data zamówienia", fg='white', bg = '#669966',font=('Helvetica', 10, 'bold'))
    data_label.grid(row=2, column=0)

    #database
    def search_db():

        cursor.execute(
        "select i.nazwa, z.id_zamowienia, z.ilosc, z.data_zamowienia, z.data_odbioru, z.cena FROM szkolka_2.dbo.zamowienia z left join szkolka_2.dbo.informacje i on i.id_informacje = z.id_informacje left join szkolka_2.dbo.klienci k on k.id_klient = z.id_klient where z.data_zamowienia = ?",
        data.get()
        )

        #view results
        records = cursor.fetchmany() #przechwytuje wszystkie odpowiedzi
        nazwy = ["Nazwa: ","Numer zamówienia: ", "Ilość: ", "Data zamówienia: ", "Data odbioru: ", "Cena: "]
        #answer after search button
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
    submit_btn = Button(root, text="Szukaj", command=search_db, width=10)
    submit_btn.grid(row=12, column=1, columnspan=2, pady=10, padx=10)
    
######################## MENU ############################

menubar = Menu(window)
podmenu1 = Menu(window)
podmenu2 = Menu(window)
podmenu3 = Menu(window)
submenu = Menu(window)


filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menu", menu=filemenu)

filemenu.add_command(label="Dodaj roślinę", command=add)
filemenu.add_command(label="Usuń roślinę", command=delete)
filemenu.add_command(label="Zmień ilość", command=quantity)

filemenu.add_command(label="Dodaj informację o uprawie", command=cropp)

#MENU 2
zammenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Zamówienia", menu=zammenu)

zammenu.add_command(label="new zamówienie", command=new_order)
zammenu.add_command(label="Usuń zamówienie", command=delete_order)

zammenu.add_cascade(label="Wyszukaj zamówienie", menu=podmenu3)
podmenu3.add_command(label="Szukaj po dacie", command=search_order)

#MENU 3
menu3 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Klienci", menu=menu3)

menu3.add_command(label="Dodaj klienta", command=add_customer)
menu3.add_command(label="Usuń klienta", command=delete_customer)
menu3.add_command(label="Szukaj klienta", command=customer_search)

window.config(menu=menubar)
        
window.mainloop() #wyswietlenie okna

# Close connection
conn.close()

