from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country
                from customer c
                where c.Country is not null
                order by c.Country
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.*, count(*) as numBrani, t.GenreId
FROM album a, track t 
WHERE a.AlbumId = t.AlbumId
GROUP BY a.AlbumId
                    """

        cursor.execute(query)

        for row in cursor:
            results.append(Album(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.AlbumId as id1, t2.AlbumId as id2
FROM
(SELECT DISTINCT a.AlbumId, g.GenreId
FROM album a, track t, genre g
WHERE a.AlbumId = t.AlbumId
AND t.GenreId = g.GenreId) t1,
(SELECT DISTINCT a.AlbumId, g.GenreId
FROM album a, track t, genre g
WHERE a.AlbumId = t.AlbumId
AND t.GenreId = g.GenreId) t2
WHERE t1.GenreId = t2.GenreId
AND t1.AlbumId < t2.AlbumId
GROUP BY t1.AlbumId, t2.AlbumId
                        """

        cursor.execute(query)

        for row in cursor:
            results.append((row["id1"], row["id2"]))

        cursor.close()
        conn.close()
        return results



    # esempio per il set
    # Il modo più semplice è aggiungere nella classe Album un attributo generi (insieme di GenreId) e riempirlo con una query.
    @staticmethod
    def getGeneriAlbum():
        conn = DBConnect.get_connection()
        results = {}
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT t.AlbumId, t.GenreId
                   FROM track t
                   WHERE t.GenreId IS NOT NULL"""
        cursor.execute(query)
        for row in cursor:
            results.setdefault(row["AlbumId"], set()).add(row["GenreId"])
        cursor.close()
        conn.close()
        return results

    #Per ogni riga: se AlbumId non è ancora una chiave, crea un set() vuoto; poi aggiunge il GenreId a quel set. Alla fine generi è un dizionario così:
    # {1: {1}, 2: {1}, 3: {1, 3}, ...}
    #  AlbumId: {insieme dei GenreId}

    # il secondo pezzo:
    #
    # python
    # generi = DAO.getGeneriAlbum()          # il dizionario di sopra
    # for node in nodes:                     # per ogni oggetto Album
    #     node.generi = sorted(generi.get(node.AlbumId, []))
    #
    # Qui i generi vengono finalmente attaccati agli oggetti Album:
    #
    # generi.get(node.AlbumId, []) prende il set di generi di quell’album; se l’album non è nel dizionario restituisce [] invece di dare errore (KeyError), quindi niente eccezioni.
    # sorted(...) trasforma il set in una lista ordinata, così quando stampi gli ID escono sempre nello stesso ordine (un set non ha ordine garantito).
    # node.generi = ... crea l’attributo generi sull’oggetto Album.



    # oppure:
    @staticmethod
    def getTracksForAlbum(album):
        # gli passo un album e lo popolo con i suoi tracks
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select t.*
                    from track t
                    where t.AlbumId = %s
                    order by t.Name
                    """

        cursor.execute(query, (album.AlbumId,))

        for row in cursor:
            results.append(Track(**row))
        album.Tracks = results

        cursor.close()
        conn.close()

