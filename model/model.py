import networkx as nx

from database.dao import DAO
from operator import itemgetter


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.DiGraph()
        self._soglia = 0

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.lista_nodi = DAO.getRifugi()
        self.lista_sentieri = DAO.getSentieri(year)

        for sentiero in self.lista_sentieri:
            difficolta = self.convertiDiff(sentiero)
            self.G.add_edge(sentiero.id_rifugio1, sentiero.id_rifugio2, weight=(difficolta * float(sentiero.distanza)))

    def convertiDiff(self, sentiero):
        if sentiero.difficolta == "facile":
            return 1
        elif sentiero.difficolta == "media":
            return 1.5
        elif sentiero.difficolta == "difficile":
            return 2


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO

        minimo = 1000
        massimo = -1000

        for edge in self.G.edges(data=True):
            if edge[2]["weight"] < minimo:
                minimo = edge[2]["weight"]

        for edge in self.G.edges(data=True):
            if edge[2]["weight"] > massimo:
                massimo = edge[2]["weight"]

        return round(minimo, 2), round(massimo, 2)


    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        lista_maggiori = []
        lista_minori = []
        self._soglia = soglia

        for edge in self.G.edges(data=True):
            if edge[2]["weight"] < soglia:
                lista_minori.append(round(edge[2]["weight"], 2))
            elif edge[2]["weight"] > soglia:
                lista_maggiori.append(round(edge[2]["weight"], 2))

        return len(lista_minori), len(lista_maggiori)

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def cammino_minimo(self):
        # algoritmo AP-SP, per cercare il percorso più breve
        # deve restituire sia il peso complessivo del percorso minimo che la sequenza di nodi
        # tutti gli archi all'interno dell'ipotetico percorso con peso minimo devono avere peso superiore
        # alla soglia

        # considero i percorsi che hanno almeno 3 nodi

        percorsi_minimi = {}

        # filtro gli archi così che l'algoritmo possa escludere i percorsi che li contengono
        for edge in self.G.edges(data=True):
            if edge[2]["weight"] < self._soglia:
                edge[2]["weight"] = float("inf")


        # dijkstra

        for nodo_sorgente in self.G.nodes():
            cammini = nx.single_source_dijkstra_path(self.G, nodo_sorgente, weight="weight")

            costo_cammino = nx.single_source_dijkstra_path_length(self.G, nodo_sorgente, weight="weight")

            validi = {}
            for destinazione, path in cammini.items():

                if len(path) < 3:
                    continue

                costo = costo_cammino[destinazione]
                if costo == float("inf"):
                    continue

                validi[destinazione] = (path, costo)

            if len(validi.keys()) != 0:
                percorsi_minimi[nodo_sorgente] = validi

        for nodo_sorgente, validi in percorsi_minimi.items():
            validi_ordinati = dict(sorted(validi.items(), key=lambda item: item[1][1]))
            percorsi_minimi[nodo_sorgente] = validi_ordinati

        for key in percorsi_minimi:
            print(f"{key} ha {percorsi_minimi[key]}")

        min_costo = float("inf")

        for sorgente, validi in percorsi_minimi.items():
            for dest, (path, costo) in validi.items():
                if costo < min_costo:
                    min_costo = costo

        percorsi_minimi_assoluti = []

        for sorgente, validi in percorsi_minimi.items():
                for dest, (path, costo) in validi.items():
                    if costo == min_costo:
                        percorsi_minimi_assoluti.append([sorgente, dest, path, costo])

        print(f"Costo minimo assoluto: {min_costo}")
        for sorgente, dest, path, costo in percorsi_minimi_assoluti:
            print(f"Sorgente: {sorgente}, Destinazione: {dest}, Percorso: {path}, costo: {costo}")

            # rimuovo i percorsi duplicati
        percorsi_minimi_non_duplicati = []
        for sorgente, dest, path, costo in percorsi_minimi_assoluti:
            for sorgente2, dest2, path2, costo2 in percorsi_minimi_assoluti:
                if sorgente == dest2:
                    break
                else:
                    percorsi_minimi_non_duplicati.append([sorgente, dest, path, costo])

        for i in range(len(percorsi_minimi_non_duplicati)):
            for rifugio in self.lista_nodi:
                    if rifugio.id == percorsi_minimi_assoluti[i][0]:
                        percorsi_minimi_assoluti[i][0] = rifugio
                    if rifugio.id == percorsi_minimi_assoluti[i][1]:
                        percorsi_minimi_assoluti[i][1] = rifugio

        return percorsi_minimi_non_duplicati

    def cammino_minimo_recursive(self):

            self.best_cost = float("inf")
            self.best_result = None

            for nodo in self.G.nodes():
                self.dfs_rec(nodo_corrente = nodo,
                             sorgente = nodo,
                             visitati = {nodo},
                             path = [nodo],
                             costo = 0)
            if self.best_result is None:
                return []

            sorgente_id, dest_id, path_ids, costo = self.best_result

            path_rifugi = []
            for nodo_id in path_ids:
                for rifugio in self.lista_nodi:
                    if rifugio.id == nodo_id:
                        path_rifugi.append(rifugio)
                        break

            return [
                sorgente_id,
                dest_id,
                path_rifugi,
                costo
            ]
    def dfs_rec(self, nodo_corrente, sorgente, visitati,path, costo):
        if len(path) >= 3:
            if costo < self.best_cost:
                self.best_cost = costo
                self.best_result = ( sorgente, nodo_corrente, path.copy, costo)

        for vicino in self.G.neighbors(nodo_corrente):
            if vicino in visitati:
                continue
            peso = self.G[nodo_corrente][vicino]["weight"]

            if peso <= self._soglia:
                continue

            if costo + peso >= self.best_cost:
                continue

            visitati.add(vicino)
            path.append(vicino)

            self.dfs_rec(vicino, sorgente, visitati, path, costo + peso)

            path.pop()
            visitati.remove(vicino)


