class Game:
    def __init__(self, name, producer, release_year, language, players, price_rent, price_sell, storage):
        if len(language) > 5:
            raise ValueError('Sigla da linguagem deve ter até 5 caracteres ' +
                             '(https://www.loc.gov/standards/iso639-2/php/code_list.php)')
        self.name = name
        self.producer = producer
        self.release_year = release_year
        self.language = language
        self.players = players
        self.price_rent = price_rent
        self.price_sell = price_sell
        self.storage = storage
