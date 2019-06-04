"""This module enumerates the standard fermentables (for now)"""
from zymurgy import Fermentable

all_fermentables = dict()

def make_fermentable(*args, **kwargs):
    fermentable = Fermentable(*args, **kwargs)
    all_fermentables[fermentable['name']] = fermentable
    return fermentable

def revise_fermentable(old_fermentable, *args, **kwargs):
    fermentable = old_fermentable.with_(*args, **kwargs)
    all_fermentables[fermentable['name']] = fermentable
    return fermentable

"""Base malts - mashing required"""
MALT_AMBER             = make_fermentable('Amber malt', 269, 0.62, 65)
MALT_BROWN             = make_fermentable('Brown malt', 270, 0.62, 110)
MALT_LAGER             = make_fermentable('Lager malt', 300, 0.62, 2.8)
MALT_MILD              = make_fermentable('Mild ale malt', 295, 0.62, 7)
MALT_MUNICH            = make_fermentable('Munich malt', 295, 0.62, 15)
MALT_PALE              = make_fermentable('Pale malt', 300, 0.62, 5)
MALT_PALE_LOCOLUR      = revise_fermentable(MALT_PALE, name='Pale malt (low colour)', ebc=2.5)
MALT_VIENNA            = make_fermentable('Vienna malt', 295, 0.62, 9)
MALT_WHEAT             = make_fermentable('Wheat malt', 305, 0.62, 9)

"""Caramelized malts - no mashing required"""
MALT_BLACK             = make_fermentable('Black malt', 259, 0.62, 1280)
MALT_CHOCOLATE         = make_fermentable('Chocolate malt', 285, 0.62, 763)
MALT_CARAMALT          = make_fermentable('Caramalt', 275, 0.62, 25)
MALT_CARAPILS          = make_fermentable('Carapils', 268, 0.62, 3)
MALT_CRYSTAL_LIGHT     = make_fermentable('Crystal malt (light)', 283, 0.62, 77)
MALT_CRYSTAL_MED       = make_fermentable('Crystal malt (medium)', 272, 0.62, 104)
MALT_CRYSTAL_DARK      = make_fermentable('Crystal malt (dark)', 271, 0.62, 148)
MALT_CRYSTAL           = MALT_CRYSTAL_MED
MALT_ROAST_BARLEY      = make_fermentable('Roast barley', 276, 0.62, 903)

"""Adjuncts - need mashing with base malts"""
ADJ_FLAKED_BARLEY      = make_fermentable('Flaked barley', 260, 0.62, 2.5)
ADJ_FLAKED_MAIZE       = make_fermentable('Flaked maize', 313, 0.62, 1)
ADJ_FLAKED_RICE        = make_fermentable('Flaked rice', 310, 0.62, 0)
ADJ_FLAKED_BARLEY      = make_fermentable('Flaked barley', 260, 0.62, 3)
ADJ_TORRIFIED_BARLEY   = revise_fermentable(ADJ_FLAKED_BARLEY, name='Torrified barley')
ADJ_FLAKED_OATS        = make_fermentable('Flaked oats', 245, 0.62, 1.5)
ADJ_TORRIFIED_WHEAT    = make_fermentable('Torrified wheat', 288, 0.62, 4)
ADJ_FLAKED_WHEAT       = make_fermentable('Flaked wheat', 173, 0.62, 0)

"""Sugars (incl. malt extract) - no mashing required"""
SUGAR_LACTOSE          = make_fermentable('Lactose', 0, 0, 30, is_extract=True)
SUGAR_BROWN_LIGHT      = make_fermentable('Brown sugar (light)', 370, 1, 16, is_extract=True)
SUGAR_BROWN_MEDIUM     = make_fermentable('Brown sugar (medium)', 370, 1, 45, is_extract=True)
SUGAR_BROWN_DARK       = make_fermentable('Brown sugar (dark)', 370, 1, 90, is_extract=True)
SUGAR_CANE             = make_fermentable('Cane sugar', 375, 1, 0, is_extract=True)
SUGAR_INVERT           = make_fermentable('Invert sugar', 319*0.85, 0.85, 0, is_extract=True)

LME_LIGHT              = make_fermentable('Liquid malt extract (light)', 310, 0.62, 10, is_extract=True)
LME_EXTRA_LIGHT        = revise_fermentable(LME_LIGHT, name='Liquid malt extract (extra light)', ebc=5.5)
LME_MEDIUM             = revise_fermentable(LME_LIGHT, name='Liquid malt extract (amber/medium)', ebc=18)
LME_DARK               = revise_fermentable(LME_LIGHT, name='Liquid malt extract (dark)', ebc=55)
LME_WHEAT              = revise_fermentable(LME_LIGHT, name='Liquid malt extract (wheat)', ebc=9)

DME_LIGHT              = make_fermentable('Dried malt extract (light)', 365, 0.62, 11, is_extract=True)
DME_EXTRA_LIGHT        = revise_fermentable(DME_LIGHT, name='Dried malt extract (extra light)', ebc=7.5)
DME_MEDIUM             = revise_fermentable(DME_LIGHT, name='Dried malt extract (medium)', ebc=34)
DME_DARK               = revise_fermentable(DME_LIGHT, name='Dried malt extract (dark)', ebc=57)
DME_EXTRA_DARK         = revise_fermentable(DME_LIGHT, name='Dried malt extract (extra dark)', ebc=95)
DME_WHEAT              = revise_fermentable(DME_LIGHT, name='Dried malt extract (wheat)', ebc=6)


