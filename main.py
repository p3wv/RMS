import googlemaps
import usr_input
import url_parser

# klucz API
kluczGM = googlemaps.Client(key='AIzaSyD8i4ysTO8mgS2YyuY-O06EVQCty-ld_Pw')

adresy_url = []

adresy_na_godzine = []

lista_adresow = []

# user podaje adresy (wybiera, jesli sa na godzine)


def main():
    usr_input.user_input()

    url_parser.url_parser()


if __name__ == '__main__':
    main()
