#!/usr/bin/env python3

import sys
import logging

import fermentables
import hops

from calculators import GrainBill, HopSchedule, HopAddition, BitternessBalance, Attenuation, ABVCalculator

"""all units are metric: volumes in litres, weight/mass in grams"""

if __name__ == "__main__":
    if '-d' in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
    elif '-v' in sys.argv:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    VOLUME = 21
    BREW_EFFICIENCY = 0.78

    list_of_fermentables = [
        fermentables.DME_LIGHT.with_(weight=2301),
        fermentables.MALT_CRYSTAL.with_(weight=228),
        fermentables.MALT_AMBER.with_(weight=85),
        fermentables.MALT_BLACK.with_(weight=19)
    ]
    list_of_hops = [
        hops.HOP_NORTHDOWN.with_(alpha=7.8, weight=36, boil_time=90),
        hops.HOP_FUGGLES.with_(alpha=4.7, weight=18, boil_time=10),
        hops.HOP_FUGGLES.with_(alpha=4.7, weight=23, boil_time=0),
    ]

    gb = GrainBill(efficiency=BREW_EFFICIENCY, volume=VOLUME, fermentables=list_of_fermentables)
    og, ebc = gb.calculate()

    hops = HopSchedule(gravity=og, volume=VOLUME, hop_additions=list_of_hops)
    ibu = hops.calculate()

    attenuation = Attenuation(
        # yeast_efficiency=0.75,
        brew_efficiency=BREW_EFFICIENCY,
        original_gravity=og,
        fermentables=list_of_fermentables,
        volume=VOLUME)
    fg = attenuation.calculate()

    required_ibu = BitternessBalance(
        original_gravity=og,
        final_gravity=fg,
        style='4B. Special or Best Bitter'
        # style='4B'
    ).calculate()

    abv = ABVCalculator(original_gravity=og, final_gravity=fg).calculate()

    print("Grain bill:")
    print(gb)
    print()
    print("Hop Schedule:")
    print(hops)
    print()
    print("""Original gravity = {original-gravity:.3f}
Final gravity={final-gravity:.3f}""".format(**attenuation.get_params('original-gravity', 'final-gravity')))
    print("""ABV = {abv:0.1f}%
EBC = {ebc:.1f}
IBU = {ibu:.1f}""".format(
        og=og,
        fg=fg,
        ebc=ebc,
        ibu=ibu,
        abv=100*abv
    ))
    print("\nBalanced IBU: {required_ibu:.0f}".format(required_ibu=required_ibu))
