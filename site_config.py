"""
site_config.py
===============
Costanti condivise tra generate_pages.py e generate_blog_pages.py, così il
dominio base e il nome del sito restano allineati ovunque invece di essere
duplicati (e potenzialmente disallineati, come accadeva prima con BASE_URL
duplicato in generate_blog_pages.py).

SWITCH-DOMAIN: se in futuro il dominio cambia di nuovo, aggiornare solo qui.
"""

BASE_URL = "https://www.parafarmaciaemy.it"
SITE_NAME = "Parafarmacia Erboristeria Viale Umberto 1°"
