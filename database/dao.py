from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.sentiero import Sentiero


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO

    @staticmethod
    def getRifugi():
        cnx = DBConnect.get_connection()
        result = []
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM rifugiO"
        cursor.execute(query)
        for row in cursor:
            rif = Rifugio(row["id"],row["nome"], row["localita"], row["altitudine"], row["capienza"], row["aperto"])
            result.append(rif)
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getSentieri(anno):
        cnx = DBConnect.get_connection()
        result = []
        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT *
                    FROM connessione c
                    WHERE c.anno <= %s
                    GROUP BY c.id_rifugio1, c.id_rifugio2"""
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(Sentiero(row["id"], row["id_rifugio1"], row["id_rifugio2"], row["distanza"], row["difficolta"], row["durata"], row["anno"]))
        cursor.close()
        cnx.close()
        return result
