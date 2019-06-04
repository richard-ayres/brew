import logging

from .calculator import Calculator


class BitternessBalance(Calculator):
    """Calculate the recommended bitterness (IBU) for the style and strength"""
    required = {'original-gravity', 'final-gravity', 'style'}

    styles = {
        '1A. Light/Standard/Premium':	1.02,
        '1B. Dark': 0.7,
        '1C. Classic American Pilsner': 1.33,
        '2A. Bohemian Pilsner': 1.5,
        '2B. Northern German Pilsner': 1.64,
        '2C. Dortmunder Export': 1.06,
        '2D. Münchner Helles': 0.83,
        '3A. Blond Ale': 1.02,
        '3B. American Wheat': 0.91,
        '3C. Cream Ale': 0.81,
        '4A. Ordinary Bitter': 1.63,
        '4B. Special or Best Bitter': 1.53,
        '4C. Strong Bitter/English Pale Ale': 1.67,
        '5A. Light 60/-': 0.63,
        '5B. Heavy 70/-': 0.81,
        '5C. Export 80/-': 1,
        '6A. American Pale Ale': 1.24,
        '6B. American Amber Ale': 1.24,
        '6C. California Common Beer': 1.67,
        '7. India Pale Ale': 1.76,
        '8A. Kölsch-Style Ale': 1.11,
        '8B. Düsseldorf Altbier': 1.88,
        '8C. Northern German Altbier': 1.22,
        '9A. Oktoberfest/Märzen': 0.92,
        '9B. Vienna Lager': 1.03,
        '10A. Mild': 0.81,
        '10B. Northern English Brown Ale': 1.03,
        '10C. Southern English Brown': 0.85,
        '10D. American Brown Ale': 1.69,
        '11A. Old Ale': 1.26,
        '11B. Strong Scotch Ale (Wee Heavy)': 0.74,
        '12A. English-style Barleywine': 1.56,
        '12B. American-Style Barleywine': 1.56,
        '12C. Russian Imperial Stout': 1.6,
        '13A. Munich Dunkel': 0.9,
        '13B. Schwarzbier (Black Beer)': 1.23,
        '14A. Traditional Bock': 0.85,
        '14B. Helles Bock/Maibock': 0.88,
        '14C. Doppelbock': 0.65,
        '15A. Robust Porter': 1.28,
        '15B. Brown Porter': 1.17,
        '16A. Dry Stout': 2.13,
        '16B. Sweet Stout': 1.08,
        '16C. Oatmeal Stout': 1.4,
        '16D. Foreign Extra Stout': 1.88,
        '17A. Bavarian Weizen': 0.65,
        '17B. Bavarian Dunkelweizen': 0.65,
        '17D. Weizenbock': 0.64,
        '18A. Dubbel': 0.95,
        '18B. Tripel': 0.79,
        '18C. Belgian Strong Golden Ale': 0.89,
        '18D. Belgian Strong Dark Ale': 0.86,
        '19A. Belgian Pale Ale': 1.28,
        '19B. Witbier': 0.87,
        '19C. Biere de Garde': 0.8,
        '19D. Saison': 1.16,
        '19E. Belgian Specialty Ale': 1.22,
        '23A. Classic Rauchbier': 0.92
    }
    styles_truncated = None

    def calculate(self):
        rte = 0.82 * (1000*(self['final-gravity'] - 1.0)) + 0.18*(1000*(self['original-gravity']-1.0))
        balance_value = self.get_balance_value()

        required_ibu = 1.25 * balance_value * rte

        logging.debug("""IBU Required for balance:
    OG = {og:.3f}
    FG = {fg:.3f}
    RTE = {rte:.1f}
    Style = {style}
    Balance Value = {bv}
    Required IBU = {ibu:.1f}""".format(
            og=self['original-gravity'],
            fg=self['final-gravity'],
            rte=rte,
            style=self['style'],
            bv=balance_value,
            ibu=required_ibu
        ))

        return required_ibu

    def get_balance_value(self):
        try:
            return self.styles[self['style']]
        except KeyError:
            if BitternessBalance.styles_truncated is None:
                BitternessBalance.styles_truncated = {name.split('.')[0]: self.styles[name] for name in self.styles.keys()}
            return self.styles_truncated[self['style']]
