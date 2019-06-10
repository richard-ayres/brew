"""This module enumerates the standard fermentables (for now)"""
import models
import zymurgy

from database import db_session

all_fermentables = dict()


def load_fermentable(name):
    fermentable = db_session.query(models.Fermentable).filter_by(name=name).one()
    fermentable = zymurgy.Fermentable.from_model(fermentable)
    all_fermentables[name] = fermentable
    return fermentable


def revise_fermentable(old_fermentable, name, **kwargs):
    return load_fermentable(name)


"""Base malts - mashing required"""
MALT_AMBER             = load_fermentable('Amber malt')
MALT_BROWN             = load_fermentable('Brown malt')
MALT_LAGER             = load_fermentable('Lager malt')
MALT_MILD              = load_fermentable('Mild ale malt')
MALT_MUNICH            = load_fermentable('Munich malt')
MALT_PALE              = load_fermentable('Pale malt')
MALT_PALE_LOCOLUR      = revise_fermentable(MALT_PALE, name='Pale malt (low colour)', ebc=2.5)
MALT_VIENNA            = load_fermentable('Vienna malt')
MALT_WHEAT             = load_fermentable('Wheat malt')

"""Caramelized malts - no mashing required"""
MALT_BLACK             = load_fermentable('Black malt')
MALT_CHOCOLATE         = load_fermentable('Chocolate malt')
MALT_CARAMALT          = load_fermentable('Caramalt')
MALT_CARAPILS          = load_fermentable('Carapils')
MALT_CRYSTAL_LIGHT     = load_fermentable('Crystal malt (light)')
MALT_CRYSTAL_MED       = load_fermentable('Crystal malt (medium)')
MALT_CRYSTAL_DARK      = load_fermentable('Crystal malt (dark)')
MALT_CRYSTAL           = MALT_CRYSTAL_MED
MALT_ROAST_BARLEY      = load_fermentable('Roast barley')

"""Adjuncts - need mashing with base malts"""
ADJ_FLAKED_BARLEY      = load_fermentable('Flaked barley')
ADJ_FLAKED_MAIZE       = load_fermentable('Flaked maize')
ADJ_FLAKED_RICE        = load_fermentable('Flaked rice')
ADJ_TORRIFIED_BARLEY   = revise_fermentable(ADJ_FLAKED_BARLEY, name='Torrified barley (not sure correct values)')
ADJ_FLAKED_OATS        = load_fermentable('Flaked oats')
ADJ_TORRIFIED_WHEAT    = load_fermentable('Torrified wheat')
ADJ_FLAKED_WHEAT       = load_fermentable('Flaked wheat')

"""Sugars (incl. malt extract) - no mashing required"""
SUGAR_LACTOSE          = load_fermentable('Lactose')
SUGAR_BROWN_LIGHT      = load_fermentable('Brown sugar (light)')
SUGAR_BROWN_MEDIUM     = load_fermentable('Brown sugar (medium)')
SUGAR_BROWN_DARK       = load_fermentable('Brown sugar (dark)')
SUGAR_CANE             = load_fermentable('Cane sugar')
SUGAR_INVERT           = load_fermentable('Invert sugar')

LME_LIGHT              = load_fermentable('Liquid malt extract (light)')
LME_EXTRA_LIGHT        = revise_fermentable(LME_LIGHT, name='Liquid malt extract (extra light)', ebc=5.5)
LME_MEDIUM             = revise_fermentable(LME_LIGHT, name='Liquid malt extract (amber/medium)', ebc=18)
LME_DARK               = revise_fermentable(LME_LIGHT, name='Liquid malt extract (dark)', ebc=55)
LME_WHEAT              = revise_fermentable(LME_LIGHT, name='Liquid malt extract (wheat)', ebc=9)

DME_LIGHT              = load_fermentable('Dried malt extract (light)')
DME_EXTRA_LIGHT        = revise_fermentable(DME_LIGHT, name='Dried malt extract (extra light)', ebc=7.5)
DME_MEDIUM             = revise_fermentable(DME_LIGHT, name='Dried malt extract (medium)', ebc=34)
DME_DARK               = revise_fermentable(DME_LIGHT, name='Dried malt extract (dark)', ebc=57)
DME_EXTRA_DARK         = revise_fermentable(DME_LIGHT, name='Dried malt extract (extra dark)', ebc=95)
DME_WHEAT              = revise_fermentable(DME_LIGHT, name='Dried malt extract (wheat)', ebc=6)


