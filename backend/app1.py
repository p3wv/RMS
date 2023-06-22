import re
import requests
from datetime import datetime
from tables import *
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

def url_parser():
    adresy_spaced = []

    for adresy in lista_adresow:
        adres_z_ampersandem = re.sub(' ', '%20', adresy)
        adresy_spaced.append(adres_z_ampersandem)

    adresy_z_przecinkami = []

    for _ in adresy_spaced:
        adres_przecinek = re.sub(',', '%2C', _)
        adresy_z_przecinkami.append(adres_przecinek)

    for _ in adresy_z_przecinkami:
        adres_url = re.sub('/', '%2F', _)
        adresy_url.append(adres_url)   


@app.route('/api/user_input', methods=['POST'])
def handle_user_input():
    data = request.get_json()
    command = data.get('command')
    if command == 'user_input':
        # Place your user_input logic here
        liczba_iteracji = 1
        czy_kontynuowac = 't'

        while czy_kontynuowac != 'n':
            na_godzine = int(input("dowoz na teraz czy na wskazana godzine?\n 1. teraz\n 2. na godzine"))

            if na_godzine == 1:
                adres = input("Podaj {}. adres: ".format(liczba_iteracji))
                tables.lista_adresow.append(adres)
            elif na_godzine == 2:
                na_godzine_adres = input('Podaj {}. adres: '.format(liczba_iteracji))
                tablica_na_godzine = [na_godzine_adres]
                godzina = input("podaj godzine w formacie HH:MM:\n")
                format_data = "%H:%M"
                date = datetime.strptime(godzina, format_data)
                for i in tablica_na_godzine:
                    tablica_na_godzine[i] = date
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
    #     return jsonify({'message': 'User input handled'})
    # else:
    #     return jsonify({'message': 'Invalid command'})
        url_parser()

        return render_template('map.html', addresses=lista_adresow)
    else:
        return jsonify({'message': 'Invalid command'})
    
    
        
# Define other routes and functions as needed

if __name__ == '__main__':
    app.run()
