from lib import CONN, CURSOR

class Castle:

    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    def __repr__(self):
        return f"Castle(id={self.id}, name={self.name})"

    @classmethod
    def create_table(cls):
        sql="""CREATE TABLE IF NOT EXISTS castles (
        id INTEGER PRIMARY KEY,
        name TEXT
        )
        """

        CURSOR.execute(sql)

    @classmethod
    def query_all(cls):
        rows = CURSOR.execute("SELECT * FROM castles").fetchall()
        return [ Castle(r[1], r[0]) for r in rows ]
