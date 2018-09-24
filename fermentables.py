"""This module enumerates the standard fermentables (for now)"""
from calculators import Fermentable, Extract

"""Base malts - mashing required"""
MALT_AMBER             = Fermentable('Amber malt', 269, 0.62, 65)
MALT_BROWN             = Fermentable('Brown malt', 270, 0.62, 110)
MALT_LAGER             = Fermentable('Lager malt', 300, 0.62, 2.8)
MALT_MILD              = Fermentable('Mild ale malt', 295, 0.62, 7)
MALT_MUNICH            = Fermentable('Munich malt', 295, 0.62, 15)
MALT_PALE              = Fermentable('Pale malt', 300, 0.62, 5)
MALT_PALE_LOCOLUR      = MALT_PALE.add(name='Pale malt (low colour)', ebc=2.5)
MALT_VIENNA            = Fermentable('Vienna malt', 295, 0.62, 9)
MALT_WHEAT             = Fermentable('Wheat malt', 305, 0.62, 9)

"""Caramelized malts - no mashing required"""
MALT_BLACK             = Fermentable('Black malt', 259, 0.62, 1280)
MALT_CHOCOLATE         = Fermentable('Chocolate malt', 285, 0.62, 763)
MALT_CARAMALT          = Fermentable('Caramalt', 275, 0.62, 25)
MALT_CARAPILS          = Fermentable('Carapils', 268, 0.62, 3)
MALT_CRYSTAL_LIGHT     = Fermentable('Crystal malt (light)', 283, 0.62, 77)
MALT_CRYSTAL_MED       = Fermentable('Crystal malt (medium)', 272, 0.62, 104)
MALT_CRYSTAL_DARK      = Fermentable('Crystal malt (dark)', 271, 0.62, 148)
MALT_CRYSTAL           = MALT_CRYSTAL_MED
MALT_ROAST_BARLEY      = Fermentable('Roast barley', 276, 0.62, 903)

"""Adjuncts - need mashing with base malts"""
ADJ_FLAKED_BARLEY      = Fermentable('Flaked barley', 260, 0.62, 2.5)
ADJ_FLAKED_MAIZE       = Fermentable('Flaked maize', 313, 0.62, 1)
ADJ_FLAKED_RICE        = Fermentable('Flaked rice', 310, 0.62, 0)
ADJ_FLAKED_BARLEY      = Fermentable('Flaked barley', 260, 0.62, 3)
ADJ_TORRIFIED_BARLEY   = ADJ_FLAKED_BARLEY.add(name='Torrified barley')
ADJ_FLAKED_OATS        = Fermentable('Flaked oats', 245, 0.62, 1.5)
ADJ_TORRIFIED_WHEAT    = Fermentable('Torrified wheat', 288, 0.62, 4)
ADJ_FLAKED_WHEAT       = Fermentable('Flaked wheat', 173, 0.62, 0)

"""Sugars (incl. malt extract) - no mashing required"""
SUGAR_LACTOSE          = Fermentable('Lactose', 0, 0, 30, is_extract=True)
SUGAR_BROWN_LIGHT      = Fermentable('Brown sugar (light)', 370, 1, 16, is_extract=True)
SUGAR_BROWN_MEDIUM     = Fermentable('Brown sugar (medium)', 370, 1, 45, is_extract=True)
SUGAR_BROWN_DARK       = Fermentable('Brown sugar (dark)', 370, 1, 90, is_extract=True)
SUGAR_CANE             = Fermentable('Cane sugar', 375, 1, 0, is_extract=True)
SUGAR_INVERT           = Fermentable('Invert sugar', 319*0.85, 0.85, 0, is_extract=True)

LME_LIGHT              = Fermentable('Liquid malt extract (light)', 310, 0.62, 10, is_extract=True)
LME_EXTRA_LIGHT        = LME_LIGHT.add(name='Liquid malt extract (extra light)', ebc=5.5)
LME_MEDIUM             = LME_LIGHT.add(name='Liquid malt extract (amber/medium)', ebc=18)
LME_DARK               = LME_LIGHT.add(name='Liquid malt extract (dark)', ebc=55)
LME_WHEAT              = LME_LIGHT.add(name='Liquid malt extract (wheat)', ebc=9)

DME_LIGHT              = Fermentable('Dried malt extract (light)', 365, 0.62, 11, is_extract=True)
DME_EXTRA_LIGHT        = DME_LIGHT.add(name='Dried malt extract (extra light)', ebc=7.5)
DME_MEDIUM             = DME_LIGHT.add(name='Dried malt extract (medium)', ebc=34)
DME_DARK               = DME_LIGHT.add(name='Dried malt extract (dark)', ebc=57)
DME_EXTRA_DARK         = DME_LIGHT.add(name='Dried malt extract (extra dark)', ebc=95)
DME_WHEAT              = DME_LIGHT.add(name='Dried malt extract (wheat)', ebc=6)


