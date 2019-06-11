#!/usr/bin/env python3
import models
import yaml

from database import db_session, Base, engine as db_engine

init_data = yaml.load(open('init.yml'))

Base.metadata.create_all(db_engine)

try:
    def populate(name, model):
        db_session.query(model).delete()
        db_session.add_all(model(**obj) for obj in init_data.get(name, []))

    # Populate stuff
    populate('fermentables', models.Fermentable)
    populate('hops', models.Hop)
    populate('waters', models.Water)
    populate('yeasts', models.Yeast)

    # The rest
    db_session.query(models.GrainBill).delete()
    db_session.query(models.HopSchedule).delete()
    db_session.query(models.Recipe).delete()

    db_session.query(models.User).delete()
    default_user = models.User(
        name='Richard Ayres',
        email='richard@bitspear.co.uk',
        salt='7422dfa8345b2bcd70778586a91130e9bf6429003fca7b32e77ec88e515b3395',
        password='ce13c1706ea37b1fc0ca3c5deb1789179889c1cf9644885561a65dc1c7441345',
        active=True
    )
    db_session.add(default_user)

    db_session.commit()
except:
    db_session.rollback()
    raise
