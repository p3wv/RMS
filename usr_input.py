from main import adresy_na_godzine, lista_adresow
from datetime import datetime


def user_input():
    liczba_iteracji = 1
    czy_kontynuowac = 't'

    while czy_kontynuowac != 'n':

        na_godzine = int(input("dowoz na teraz czy na wskazana godzine?\n 1. teraz\n 2. na godzine"))

        if na_godzine == 1:
            adres = input("Podaj {}. adres: ".format(liczba_iteracji))
            lista_adresow.append(adres)

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

                adresy_na_godzine.append(tablica_na_godzine)

        czy_kontynuowac = input("Wprowadzic kolejny adres? (t/n)")
        if czy_kontynuowac == 't':
            liczba_iteracji += 1
