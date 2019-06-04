#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models

from fermentables import all_fermentables
from hops import all_hops

engine = create_engine('sqlite:///./brew.sqlite3', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

fermentables = list(all_fermentables.values())
hops = list(all_hops.values())

fermentables[0].to_model().metadata.create_all(engine)
hops[0].to_model().metadata.create_all(engine)

try:
    session.query(models.Fermentable).delete()
    session.query(models.Hop).delete()

    session.add_all(fermentable.to_model() for fermentable in fermentables)
    session.add_all(hop.to_model() for hop in hops)

    session.commit()
except:
    session.rollback()
