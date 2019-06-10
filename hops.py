import models
import zymurgy

from database import db_session

all_hops = dict()


def load_hop(name):
    hop = db_session.query(models.Hop).filter_by(name=name).one()
    hop = zymurgy.Hop.from_model(hop)
    all_hops[name] = hop
    return hop


HOP_CHALLENGER = load_hop('Challenger')
HOP_BREWERS_GOLD = load_hop('Brewers Gold')
HOP_BRAMLING_CROSS = load_hop('Bramling Cross')
HOP_BULLION = load_hop('Bullion')
HOP_EKG = load_hop('Goldings (East Kent)')
HOP_FUGGLES = load_hop('Fuggles')
HOP_WGOLDING = load_hop('Goldings (Worc.)')
HOP_HALLERTAUER = load_hop('Hallertauer')
HOP_NORTH_BREWER = load_hop('North Brewer')
HOP_NORTHDOWN = load_hop('Northdown')
HOP_PROGRESS = load_hop('Progress')
HOP_SAAZ = load_hop('Saaz')
HOP_STYRIAN_GOLDINGS = load_hop('Styrian Goldings')
HOP_TARGET = load_hop('Target')
HOP_TETTNANG = load_hop('Tettnang')
HOP_WGV = load_hop('WGV')
