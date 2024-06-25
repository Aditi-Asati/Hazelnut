from dataclasses import dataclass
from typing import Any
from src.query_builder.db_connector import DBConnector, DBConnectionError


@dataclass(frozen=True)
class TableFieldDescriptor:
    field: str
    field_type: str
    null: bool
    key: str
    default: Any
    extra: str

    keys = {"PRI": "PRIMARY KEY", "UNI": "UNIQUE"}

    def generate_create_field_stmt(self):
        create_stmt = f"{self.field} {self.field_type} {'NOT NULL' if not self.null else ''} {self.keys[self.key] if self.key else ''} {f'DEFAULT {self.default}' if self.default else ''} {self.extra}".strip()
        return create_stmt

    @classmethod
    def from_tuple(cls, t):
        l = list(t)
        l[2] = True if l[2] == "Yes" else False
        return cls(*l)


def generate_create_table_command(
    table_name: str, field_descs: list[TableFieldDescriptor]
):
    command = f"CREATE TABLE {table_name[0]} (\n"
    command += ",\n".join([field.generate_create_field_stmt() for field in field_descs])
    command += "\n);"
    return command


class DDLCommandGenerator:

    def __init__(self, dbconnection: DBConnector) -> None:
        try:
            self.connection = dbconnection.connect_to_db()

        except Exception:
            raise DBConnectionError(
                "Couldn't connect to the database. Check credentials."
            )

    def generate_ddl_command(self):
        show_table_query = "SHOW tables;"
        cursor = self.connection.cursor()
        cursor.execute(show_table_query)
        tables = cursor.fetchall()
        ddl_command = []
        for table in tables:
            desc_table_command = f"DESC {table[0]};"
            cursor.execute(desc_table_command)
            field_descs = [
                TableFieldDescriptor.from_tuple(f) for f in cursor.fetchall()
            ]
            ddl_command.append(generate_create_table_command(table, field_descs))

        self.connection.close()

        return ddl_command
