#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models

from fermentables import all_fermentables
from hops import all_hops

engine = create_engine('sqlite:///./brew.sqlite3', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

models.Base.metadata.create_all(engine)

try:
    session.query(models.Fermentable).delete()
    session.query(models.Hop).delete()
    session.query(models.GrainBill).delete()
    session.query(models.HopSchedule).delete()
    session.query(models.Recipe).delete()

    session.add_all(fermentable.to_model() for fermentable in all_fermentables.values())
    session.add_all(hop.to_model() for hop in all_hops.values())

    session.commit()
except:
    session.rollback()
