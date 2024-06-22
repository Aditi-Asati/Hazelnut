from dataclasses import dataclass, asdict
from mysql.connector import connect


@dataclass(frozen=True)
class DBConnector:
    """
    Establishes a connection with the given database
    """

    host: str
    user: str
    password: str
    port: int
    database: str

    def connect_to_db(self):
        connection = connect(**self.asdict())
        return connection

    def asdict(self):
        return asdict(self)


class DBConnectionError(Exception):
    pass


if __name__ == "__main__":
    obj = DBConnector(
        host="localhost", user="root", password="oursql", port=3306, database="pokedex"
    )
    print(obj.asdict())
    obj.connect_to_db()
