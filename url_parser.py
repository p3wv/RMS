from main import lista_adresow, adresy_url
import re


# adresy parsowane do url (spacje, przecinki, ukosniki)


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
