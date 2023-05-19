import tables
from datetime import datetime


def user_input():
    liczba_iteracji = 1
    czy_kontynuowac = 't'

    while czy_kontynuowac != 'n':

        na_godzine = int(input("dowoz na teraz czy na wskazana godzine?\n 1. teraz\n 2. na godzine"))

        if na_godzine == 1:
            adres = input("Podaj {}. adres: ".format(liczba_iteracji))
            tables.lista_adresow.append(adres)

        elif na_godzine == 2:
            na_godzine_adres = input('Podaj {}. adres: '. format(liczba_iteracji))

            tablica_na_godzine = [na_godzine_adres]

            godzina = input("podaj godzine w formacie HH:MM:\n")
            format_data = "%H:%M"
            date = datetime.strptime(godzina, format_data)

            for i in tablica_na_godzine:

                tablica_na_godzine[i] = date
                # h, m = map(int, time.split(':'))
                # godzina = time(hour=h, minute=m)

                tables.adresy_na_godzine.append(tablica_na_godzine)

        user_continue_clause = 't'

        while user_continue_clause != 'n':
            user_continue_clause = input("Wprowadzic kolejny adres? (t/n)")
            if user_continue_clause == 't':
                czy_kontynuowac = 't'
                liczba_iteracji += 1
                break

            elif user_continue_clause != 't' and user_continue_clause != 'n':
                print("wybierz prawidlowa wartosc!")

            elif user_continue_clause == 'n':
                czy_kontynuowac = 'n'

    if czy_kontynuowac == 'n':
        print("do widzenia")


