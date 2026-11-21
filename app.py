import os

import pymysql
from flask import Flask, make_response, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Nginx kertoo alkuperäisen yhteyden tiedot ja sovelluksen alipolun (/viikko4).
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_prefix=1,
)

def lue_laskuri():
    # Vain luku: käyttäjällä viikko4app on pelkkä SELECT-oikeus,
    # ja B:n tietokanta on lisäksi read_only.
    yhteys = pymysql.connect(
        unix_socket="/run/mysqld/mysqld.sock",
        user="viikko4app",
        password=os.environ["DB_PASSWORD"],
        database="viikko2",
        charset="utf8mb4",
    )
    try:
        with yhteys.cursor() as kursori:
            kursori.execute("SELECT kaynnit FROM laskuri WHERE id = 1")
            return kursori.fetchone()[0]
    finally:
        yhteys.close()

@app.route("/")
def etusivu():
    kaynnit = lue_laskuri()
    vastaus = make_response(render_template("index.html", kaynnit=kaynnit))
    # Selain ei saa näyttää vanhaa laskurin arvoa välimuistista
    vastaus.headers["Cache-Control"] = "no-store"
    return vastaus
