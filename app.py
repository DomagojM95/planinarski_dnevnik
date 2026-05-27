from flask import Flask, render_template, request, redirect
from pony.orm import db_session, select

from models import Izlet


app = Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")



@app.route("/izleti")
@db_session
def index():
    izleti = select(i for i in Izlet)[:]

    return render_template("index.html", izleti=izleti)



@app.route("/dodaj")
def dodaj_forma():
    return render_template("dodaj-izlet.html")



@app.route("/dodaj", methods=["POST"])
@db_session
def dodaj_izlet():
    naziv_planine = request.form.get("naziv_planine")

    datum = request.form.get("datum")

    kilometraza = float(request.form.get("kilometraza"))

    broj_sudionika = int(request.form.get("broj_sudionika"))

    nadmorska_visina = int(request.form.get("nadmorska_visina"))

    Izlet(
        naziv_planine=naziv_planine,
        datum=datum,
        kilometraza=kilometraza,
        broj_sudionika=broj_sudionika,
        nadmorska_visina=nadmorska_visina,
    )

    return redirect("/izleti")



@app.route("/uredi/<int:id>")
@db_session
def uredi_forma(id):
    izlet = Izlet.get(id=id)

    return render_template("uredi-izlet.html", izlet=izlet)



@app.route("/uredi/<int:id>", methods=["POST"])
@db_session
def uredi_izlet(id):
    izlet = Izlet.get(id=id)

    if izlet:
        izlet.naziv_planine = request.form.get("naziv_planine")

        izlet.datum = request.form.get("datum")

        izlet.kilometraza = float(request.form.get("kilometraza"))

        izlet.broj_sudionika = int(request.form.get("broj_sudionika"))

        izlet.nadmorska_visina = int(request.form.get("nadmorska_visina"))

    return redirect("/izleti")



@app.route("/delete/<int:id>", methods=["POST"])
@db_session
def delete_izlet(id):
    izlet = Izlet.get(id=id)

    if izlet:
        izlet.delete()

    return redirect("/izleti")



@app.route("/statistika")
@db_session
def statistika():
    izleti = select(i for i in Izlet)[:]

    ukupan_broj = len(izleti)

    ukupna_kilometraza = sum(i.kilometraza for i in izleti)

    prosjecna_kilometraza = 0

    if ukupan_broj > 0:
        prosjecna_kilometraza = round(ukupna_kilometraza / ukupan_broj, 2)

    najvisa_planina = 0

    if izleti:
        najvisa_planina = max(i.nadmorska_visina for i in izleti)

    nazivi_planina = [i.naziv_planine for i in izleti]

    kilometraze = [i.kilometraza for i in izleti]

    return render_template(
        "statistika.html",
        ukupan_broj=ukupan_broj,
        ukupna_kilometraza=ukupna_kilometraza,
        prosjecna_kilometraza=prosjecna_kilometraza,
        najvisa_planina=najvisa_planina,
        nazivi_planina=nazivi_planina,
        kilometraze=kilometraze,
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
