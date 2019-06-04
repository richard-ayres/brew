from zymurgy import Hop

all_hops = dict()

def make_hop(*args, **kwargs):
    hop = Hop(*args, **kwargs)
    all_hops[hop['name']] = hop
    return hop

HOP_CHALLENGER = make_hop('Challenger', alpha=7.1)
HOP_BREWERS_GOLD = make_hop('Brewers Gold', alpha=5.5)
HOP_BRAMLING_CROSS = make_hop('Bramling Cross', alpha=6.0)
HOP_BULLION = make_hop('Bullion', alpha=8)
HOP_CHALLENGER = make_hop('Challenger', alpha=7.1)
HOP_EKG = make_hop('Goldings (East Kent)', alpha=5)
HOP_FUGGLES = make_hop('Fuggles', alpha=4.5)
HOP_WGOLDING = make_hop('Goldings (Worc.)', alpha=5.3)
HOP_HALLERTAUER = make_hop('Hallertauer', alpha=4.5)
HOP_NORTH_BREWER = make_hop('North Brewer', alpha=7.5)
HOP_NORTHDOWN = make_hop('Northdown', alpha=9.25)
HOP_PROGRESS = make_hop('Progress', alpha=6.2)
HOP_SAAZ = make_hop('Saaz', alpha=2.2)
HOP_STYRIAN_GOLDINGS = make_hop('Styrian Goldings', alpha=4.5)
HOP_TARGET = make_hop('Target', alpha=11.2)
HOP_TETTNANG = make_hop('Tettnang', alpha=5)
HOP_WGV = make_hop('WGV', alpha=6.3)
