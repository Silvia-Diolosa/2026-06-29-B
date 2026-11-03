import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDD = None


    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        try:

            self._model.buildGraph()
            nNodi, nArchi = self._model.getGraphDetails()

            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Grafo correttamente creato.", color="green"))
            self._view._txt_result.controls.append(
                ft.Text(f"Nodi: {nNodi}, Archi: {nArchi}"))

            self.fillDD()

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione del grafo: {ex}")

    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        try:
            nComp, maxComp = self._model.getInfo()

            self._view._txt_result.controls.append(ft.Text(f"Numero di componenti connesse: {nComp}"))
            self._view._txt_result.controls.append(ft.Text(f""))

            self._view._txt_result.controls.append(ft.Text(f"Dimensione componente connessa più grande: {len(maxComp)}"))
            self._view._txt_result.controls.append(ft.Text(f""))

            self._view._txt_result.controls.append(ft.Text(f"Dettagli degli album appartenenti alla componente connessa più grande:"))
            self._view._txt_result.controls.append(ft.Text(f""))
            for album in maxComp:
                self._view._txt_result.controls.append(ft.Text(f"- {album.Title}: brani: {album.numBrani}"))

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella stampa delle info: {ex}")


    def fillDD(self):
        album = self._model.getNodes()
        for a in album:
            self._view._ddAlbum.options.append(ft.dropdown.Option(
                    data=a,
                    key=a.Title,
                    on_click=self._handleDD))
        self._view.update_page()

    def _handleDD(self, e):
        self._choiceDD = e.control.data


    def handleSelezione(self,e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        if self._choiceDD is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare un valore dal menu."))
            self._view.update_page()
            return

        txt = self._view._txtInN.value

        if txt == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserire un valore."))
            self._view.update_page()
            return

        try:
            val = int(txt)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserire un valore intero."))
            self._view.update_page()
            return

        if val < 1:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserire un valore positivo."))
            self._view.update_page()
            return

        try:
            path, score = self._model.getBestPath2(self._choiceDD, val)

            self._view._txt_result.controls.clear()
            if not path:
                self._view._txt_result.controls.append(
                    ft.Text("Nessun cammino trovato.", color="orange"))
            else:
                self._view._txt_result.controls.append(
                    ft.Text(f"Cammino trovato di lunghezza {len(path)} e numero di brani complessivo {score}."))
                for n in path:
                    self._view._txt_result.controls.append(ft.Text(f"- {n}, {n.numBrani} brani, genere id: {n.GenreId}"))
            self._view.update_page()
        except Exception as ex:
            self._view.create_alert(f"Errore nella ricerca della sequenza: {ex}")



