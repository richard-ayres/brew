from models import Hop as HopModel
from zymurgy import Hop
from database import db_session

all_hops = {hop.name: Hop.from_model(hop) for hop in db_session.query(HopModel).all()}


HOP_CHALLENGER = all_hops['Challenger']
HOP_BREWERS_GOLD = all_hops['Brewers Gold']
HOP_BRAMLING_CROSS = all_hops['Bramling Cross']
HOP_BULLION = all_hops['Bullion']
HOP_EKG = all_hops['Goldings (East Kent)']
HOP_FUGGLES = all_hops['Fuggles']
HOP_WGOLDING = all_hops['Goldings (Worc.)']
HOP_HALLERTAUER = all_hops['Hallertauer']
HOP_NORTH_BREWER = all_hops['North Brewer']
HOP_NORTHDOWN = all_hops['Northdown']
HOP_PROGRESS = all_hops['Progress']
HOP_SAAZ = all_hops['Saaz']
HOP_STYRIAN_GOLDINGS = all_hops['Styrian Goldings']
HOP_TARGET = all_hops['Target']
HOP_TETTNANG = all_hops['Tettnang']
HOP_WGV = all_hops['WGV']
