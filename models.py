from pony.orm import *

db = Database()


class Izlet(db.Entity):

    id = PrimaryKey(int, auto=True)

    naziv_planine = Required(str)

    datum = Required(str)

    kilometraza = Required(float)

    broj_sudionika = Required(int)

    nadmorska_visina = Required(int)


db.bind(
    provider='sqlite',
    filename='database.sqlite',
    create_db=True
)

db.generate_mapping(create_tables=True)