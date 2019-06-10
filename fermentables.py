"""This module enumerates the standard fermentables (for now)"""
from models import Fermentable as FermentableModel
from zymurgy import Fermentable
from database import db_session


all_fermentables = {malt.name: Fermentable.from_model(malt) for malt in db_session.query(FermentableModel).all()}


"""Base malts - mashing required"""
MALT_AMBER             = all_fermentables['Amber malt']
MALT_BROWN             = all_fermentables['Brown malt']
MALT_LAGER             = all_fermentables['Lager malt']
MALT_MILD              = all_fermentables['Mild ale malt']
MALT_MUNICH            = all_fermentables['Munich malt']
MALT_PALE              = all_fermentables['Pale malt']
MALT_PALE_LOCOLUR      = all_fermentables['Pale malt (low colour)']
MALT_VIENNA            = all_fermentables['Vienna malt']
MALT_WHEAT             = all_fermentables['Wheat malt']

"""Caramelized malts - no mashing required"""
MALT_BLACK             = all_fermentables['Black malt']
MALT_CHOCOLATE         = all_fermentables['Chocolate malt']
MALT_CARAMALT          = all_fermentables['Caramalt']
MALT_CARAPILS          = all_fermentables['Carapils']
MALT_CRYSTAL_LIGHT     = all_fermentables['Crystal malt (light)']
MALT_CRYSTAL_MED       = all_fermentables['Crystal malt (medium)']
MALT_CRYSTAL_DARK      = all_fermentables['Crystal malt (dark)']
MALT_CRYSTAL           = all_fermentables['Crystal malt']
MALT_ROAST_BARLEY      = all_fermentables['Roast barley']

"""Adjuncts - need mashing with base malts"""
ADJ_FLAKED_BARLEY      = all_fermentables['Flaked barley']
ADJ_FLAKED_MAIZE       = all_fermentables['Flaked maize']
ADJ_FLAKED_RICE        = all_fermentables['Flaked rice']
ADJ_TORRIFIED_BARLEY   = all_fermentables['Torrified barley (not sure correct values)']
ADJ_FLAKED_OATS        = all_fermentables['Flaked oats']
ADJ_TORRIFIED_WHEAT    = all_fermentables['Torrified wheat']
ADJ_FLAKED_WHEAT       = all_fermentables['Flaked wheat']

"""Sugars (incl. malt extract) - no mashing required"""
SUGAR_LACTOSE          = all_fermentables['Lactose']
SUGAR_BROWN_LIGHT      = all_fermentables['Brown sugar (light)']
SUGAR_BROWN_MEDIUM     = all_fermentables['Brown sugar (medium)']
SUGAR_BROWN_DARK       = all_fermentables['Brown sugar (dark)']
SUGAR_CANE             = all_fermentables['Cane sugar']
SUGAR_INVERT           = all_fermentables['Invert sugar']

LME_LIGHT              = all_fermentables['Liquid malt extract (light)']
LME_EXTRA_LIGHT        = all_fermentables['Liquid malt extract (extra light)']
LME_MEDIUM             = all_fermentables['Liquid malt extract (amber/medium)']
LME_DARK               = all_fermentables['Liquid malt extract (dark)']
LME_WHEAT              = all_fermentables['Liquid malt extract (wheat)']

DME_LIGHT              = all_fermentables['Dried malt extract (light)']
DME_EXTRA_LIGHT        = all_fermentables['Dried malt extract (extra light)']
DME_MEDIUM             = all_fermentables['Dried malt extract (medium)']
DME_DARK               = all_fermentables['Dried malt extract (dark)']
DME_EXTRA_DARK         = all_fermentables['Dried malt extract (extra dark)']
DME_WHEAT              = all_fermentables['Dried malt extract (wheat)']


