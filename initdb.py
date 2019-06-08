#!/usr/bin/env python3

import models

from fermentables import all_fermentables
from hops import all_hops
from database import db_session, Base, engine as db_engine

Base.metadata.create_all(db_engine)

try:
    db_session.query(models.Fermentable).delete()
    db_session.query(models.Hop).delete()
    db_session.query(models.GrainBill).delete()
    db_session.query(models.HopSchedule).delete()
    db_session.query(models.Recipe).delete()

    db_session.add_all(fermentable.to_model() for fermentable in all_fermentables.values())
    db_session.add_all(hop.to_model() for hop in all_hops.values())

    db_session.commit()
except:
    db_session.rollback()
