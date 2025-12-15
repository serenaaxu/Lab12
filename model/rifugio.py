from dataclasses import dataclass


@dataclass
class Rifugio:
    id : int
    nome : str
    localita : str
    altitudine : int
    capienza : int
    aperto : int

    def __str__(self):
        return f"Rifugio: {self.id}, {self.nome}, {self.localita}, {self.altitudine}, {self.capienza}, {self.aperto}"

    def __eq__(self, other):
        return self.id == other

    def __hash__(self):
        return hash(self.id)

