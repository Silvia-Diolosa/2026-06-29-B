import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self.bestScore = 0
        self.bestPath = []


    def buildGraph(self):
        self._graph.clear()
        self._idMap.clear()

        nodes = DAO.getAllNodes()
        for node in nodes:
            self._idMap[node.AlbumId] = node
        self._graph.add_nodes_from(nodes)

        edges = DAO.getAllEdges()
        for edge in edges:
            u = self._idMap[edge[0]]
            v = self._idMap[edge[1]]
            self._graph.add_edge(u, v)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getNumNodi(self):
        return len(self._graph.nodes)
    def getNumEdges(self):
        return len(self._graph.edges)
    def getNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.Title)
        return nodes
    def getEdges(self):
        return list(self._graph.edges(data=True))


    def getInfo(self):
        numCompConn = nx.number_connected_components(self._graph)
        components = list(nx.connected_components(self._graph))
        largest = list(max(components, key=len))
        largest.sort(key=lambda x: x.Title)

        return numCompConn, largest


    def getBestPath(self, partenza, n):
        self.bestScore = 0
        self.bestPath = []

        parziale = [partenza]
        components = []
        for comp in nx.connected_components(self._graph):
            if partenza in comp:
                continue
            components.append(comp)

        self._ricorsione(parziale, n, 0, components)

        self.bestPath.sort(key=lambda x: x.Title)

        return self.bestPath, self.bestScore

    def _ricorsione(self, parziale, n, i, components):
        # caso terminale
        if len(parziale) == n:
            score = self._calcolaScore(parziale)
            if score > self.bestScore:
                self.bestPath = copy.deepcopy(parziale)
                self.bestScore = score
            return

        if n > len(components):
            return

        if (len(components) - i) < (n - len(parziale)):
            return

        # caso ricorsivo
        for nodo in components[i]:
            if nodo not in parziale:
                parziale.append(nodo)
                self._ricorsione(parziale, n, i+1, components)
                parziale.pop()

        self._ricorsione(parziale, n, i+1, components)


    def _calcolaScore(self, parziale):
        score = 0
        for nodo in parziale:
            score = score + nodo.numBrani

        return score


    # possiamo fare versione più veloce di ricorsione
    # inserendo direttamente solo l'album con numero massimo:
    def getBestPath2(self, partenza, n):
        self.bestScore = 0
        self.bestPath = []

        parziale = [partenza]
        components = []
        for comp in nx.connected_components(self._graph):
            if partenza in comp:
                continue
            components.append(max(comp, key=lambda x: x.numBrani)) #QUI scegliamo direttamente il massimo per ogni componente

        self._ricorsione2(parziale, n, 0, components)

        self.bestPath.sort(key=lambda x: x.Title)

        return self.bestPath, self.bestScore

    def _ricorsione2(self, parziale, n, i, components):
        # caso terminale
        if len(parziale) == n:
            score = self._calcolaScore(parziale)
            if score > self.bestScore:
                self.bestPath = copy.deepcopy(parziale)
                self.bestScore = score
            return

        if n > len(components):
            return

        if (len(components) - i) < (n - len(parziale)):
            return

        # caso ricorsivo
        parziale.append(components[i])  # QUI, non cicliamo su ogni elemento per componente perchè abbiamo già selezionato il max
        self._ricorsione2(parziale, n, i+1, components)
        parziale.pop()

        self._ricorsione2(parziale, n, i+1, components)


