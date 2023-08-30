from lib import CONN, CURSOR
from lib.classes.castle import Castle

class Vampire:

    # MAGIC METHODS #

    def __init__(self, name, year_born, castle_id, id=None):
        self.id = id
        self.name = name
        self.year_born = year_born
        self.castle_id = castle_id

    def __repr__(self):
        return f"Vampire(id={self.id}, name={self.name}, year_born={self.year_born}, castle_id={self.castle_id})"

    # THIS METHOD WILL CREATE THE SQL TABLE #

    @classmethod
    def create_table(cls):
        sql="""CREATE TABLE IF NOT EXISTS vampires (
        id INTEGER PRIMARY KEY,
        name TEXT,
        year_born INTEGER,
        castle_id INTEGER
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql="DROP TABLE vampires"
        CURSOR.execute(sql)

    # PROPERTIES #

    @property
    def year_born(self):
        return self._year_born

    @year_born.setter
    def year_born(self, value):
        if value >= 1431 and value <= 2002:
            self._year_born = value
        else:
            raise ValueError('year_born must be a number between 1431 and 2002')

    # SQL METHODS #

    def create(self):
        sql="""INSERT INTO vampires (name, year_born, castle_id)
        VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, [self.name, self.year_born, self.castle_id])
        CONN.commit()

        self.id = CURSOR.lastrowid
        return self

    def update(self):
        sql="""UPDATE vampires
        SET name = ?, year_born = ?, castle_id = ?
        WHERE id = ?
        """
        CURSOR.execute(sql, [self.name, self.year_born, self.castle_id, self.id])

    @classmethod
    def query_all(cls):
        sql="SELECT * FROM vampires"

        rows = CURSOR.execute(sql).fetchall()

        return [ Vampire(row[1], row[2], row[3], row[0]) for row in rows ]

    # ASSOCATION PROPERTIES #

    @property
    def castle(self):
        sql="SELECT * FROM castles WHERE id = ?"

        row = CURSOR.execute(sql, [self.castle_id]).fetchone()

        if row:
            return Customer(row[1], row[0])

    @castle.setter
    def castle(self, value):
        if isinstance(value, Customer):
            self.castle_id = value.id
        else:
            raise ValueError("Customer must be of type Customer class")
