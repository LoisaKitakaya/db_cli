import click
from pytz import timezone
from datetime import datetime
import psycopg2  # type: ignore
from configparser import ConfigParser


class PostgresConnect:
    def __init__(self, path: str) -> None:
        self.path = path
        self.db = {}
        self.section = "postgresql"

        parser = ConfigParser()
        parser.read(self.path)

        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                self.db[param[0]] = param[1]
        else:
            raise Exception(
                f"Section {self.section} not found in the {self.path} file."
            )

    def check_connection(self):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute("SELECT version()")

            db_version = cur.fetchone()

            if db_version:
                click.echo(
                    click.style(
                        f"\nConnection successful.\n",
                        fg="green",
                        bold=True,
                    )
                )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

    def create_tables(self, path: str):
        with open(path, "r") as file:
            sql_commands = file.read()

        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(sql_commands)

            conn.commit()

            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            )

            tables = cur.fetchall()

            click.echo(
                click.style(
                    "\nThe following tables have been created:\n",
                    fg="green",
                    bold=True,
                    underline=True,
                )
            )

            count = 1

            for table in tables:
                click.echo(click.style(f"{count}. {table}\n", fg="green", bold=True))

                count += 1

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def delete_tables(self, table: str):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(f"DROP TABLE {table};")

            conn.commit()

            click.echo(
                click.style(
                    f"\nTable {table} has been deleted successfully.\n",
                    fg="green",
                    bold=True,
                )
            )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def view_tables(self):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            )

            tables = cur.fetchall()

            if tables:
                count = 1

                click.echo(
                    click.style(
                        "\nList of all the tables in the database:\n",
                        fg="cyan",
                        bold=True,
                        underline=True,
                    )
                )

                for table in tables:
                    click.echo(click.style(f"{count}. {table}\n", fg="cyan", bold=True))

                    count += 1

            else:
                click.echo(
                    click.style(
                        "\nNo tables have been created yet (0 tables found).\n",
                        fg="yellow",
                        bold=True,
                    )
                )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def create_record(
        self,
        animal: str,
        morning_production: float,
        afternoon_production: float,
        evening_production: float,
        production_unit: str,
        production_date: datetime,
    ):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(
                f"INSERT INTO milk_production(animal, morning_production, afternoon_production, evening_production, production_unit, production_date) VALUES('{animal}', {morning_production}, { afternoon_production}, {evening_production}, '{production_unit}', '{production_date.date()}')"
            )

            conn.commit()

            click.echo(
                click.style(
                    "\nRecord has been created successfully.\n", fg="green", bold=True
                )
            )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def view_all_records(self, table: str):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(f"SELECT * FROM {table};")

            records = cur.fetchall()

            if records:
                count = 1

                click.echo(
                    click.style(
                        f"\nList of all the records in table '{table}':\n",
                        fg="cyan",
                        bold=True,
                    )
                )

                for record in records:
                    click.echo(
                        click.style(
                            f"{count}. | id: {record[0]} | cow: {record[1]} | morning: {record[2]} | noon: {record[3]} | evening: {record[4]} | unit: {record[5]} | date: {record[6]}\n",
                            fg="cyan",
                            bold=True,
                        )
                    )

                    count += 1

            else:
                click.echo(
                    click.style(
                        f"\n0 records in table '{table}'.\n",
                        fg="yellow",
                        bold=True,
                    )
                )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def view_record(self, table: str, id: int):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(f"SELECT * FROM {table} WHERE id = {id};")

            records = cur.fetchall()

            if records:
                count = 1

                click.echo(
                    click.style(
                        f"\nRecord of id '{id}' in table '{table}':\n",
                        fg="cyan",
                        bold=True,
                        underline=True,
                    )
                )

                for record in records:
                    click.echo(
                        click.style(
                            f"{count}. | id: {record[0]} | cow: {record[1]} | morning: {record[2]} | noon: {record[3]} | evening: {record[4]} | unit: {record[5]} | date: {record[6]}\n",
                            fg="cyan",
                            bold=True,
                        )
                    )

                    count += 1

            else:
                click.echo(
                    click.style(
                        f"\nRecord of id '{id}' in table '{table}' does not exist.\n",
                        fg="yellow",
                        bold=True,
                    )
                )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def delete_record(self, table: str, id: int):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(f"DELETE from {table} WHERE id = {id};")

            conn.commit()

            click.echo(
                click.style(
                    "\nRecord has been deleted successfully.\n", fg="green", bold=True
                )
            )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def update_name(self, table: str, id: int, name: str):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(f"UPDATE {table} SET animal = '{name}' WHERE id = {id};")

            conn.commit()

            click.echo(
                click.style(
                    "\nRecord has been updated successfully.\n", fg="green", bold=True
                )
            )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def update_morning(self, table: str, id: int, amount: float):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(
                f"UPDATE {table} SET morning_production = {amount} WHERE id = {id};"
            )

            conn.commit()

            click.echo(
                click.style(
                    "\nRecord has been updated successfully.\n", fg="green", bold=True
                )
            )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def update_noon(self, table: str, id: int, amount: float):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(
                f"UPDATE {table} SET afternoon_production = {amount} WHERE id = {id};"
            )

            conn.commit()

            click.echo(
                click.style(
                    "\nRecord has been updated successfully.\n", fg="green", bold=True
                )
            )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def update_evening(self, table: str, id: int, amount: float):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(
                f"UPDATE {table} SET evening_production = {amount} WHERE id = {id};"
            )

            conn.commit()

            click.echo(
                click.style(
                    "\nRecord has been updated successfully.\n", fg="green", bold=True
                )
            )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return

    def update_date(self, table: str, id: int, date: datetime):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(
                f"UPDATE {table} SET production_date = '{date}' WHERE id = {id};"
            )

            conn.commit()

            click.echo(
                click.style(
                    "\nRecord has been updated successfully.\n", fg="green", bold=True
                )
            )

            cur.close()

        except Exception as error:
            click.echo(click.style(f"{error}", fg="red", bold=True))

        finally:
            if conn is not None:
                conn.close()

        return


my_db = PostgresConnect("database.ini")


@click.group()
def cli():
    pass


@click.command()
def check_connection():
    my_db.check_connection()


@click.command()
@click.option(
    "--path",
    default="tables.sql",
    help='This refers to a ".sql" file that can be used to create tales in the database.',
)
def create_tables(path: str):
    my_db.create_tables(path)


@click.command()
@click.option(
    "--table",
    default="milk_production",
    help="This refers to database table that is meant to be deleted.",
)
def delete_tables(table: str):
    my_db.delete_tables(table)


@click.command()
def view_tables():
    my_db.view_tables()


@click.command()
@click.option(
    "--animal",
    prompt="name of cow",
    help="This represents the name of the animal (cow).",
)
@click.option(
    "--morning-production",
    prompt="morning production",
    help="This represents the amount (e.g. in Litres) produced by the cow in the morning.",
)
@click.option(
    "--afternoon-production",
    prompt="afternoon production",
    help="This represents the amount (e.g. in Litres) produced by the cow in the afternoon.",
)
@click.option(
    "--evening-production",
    prompt="evening production",
    help="This represents the amount (e.g. in Litres) produced by the cow in the evening.",
)
@click.option(
    "--production-unit",
    default="Litres",
    help="This represents the unit of production, default: Litres.",
)
@click.option(
    "--production-date",
    prompt="date of production",
    help='This represents the date of production (of milk by each cow), e.g. "2023-10-231"',
)
def create_record(
    animal: str,
    morning_production: float,
    afternoon_production: float,
    evening_production: float,
    production_unit: str,
    production_date: str,
):
    my_timezone = timezone("Africa/Nairobi")

    date = my_timezone.localize(datetime.strptime(production_date, "%Y-%m-%d"))

    my_db.create_record(
        animal,
        morning_production,
        afternoon_production,
        evening_production,
        production_unit,
        date,
    )


@click.command()
@click.option(
    "--table",
    default="milk_production",
    help="This represents the name of the database table to query.",
)
def view_all_records(table: str):
    my_db.view_all_records(table)


@click.command()
@click.option(
    "--table",
    default="milk_production",
    help="This represents the name of the database table to query.",
)
@click.option(
    "--id",
    help="This represents the id (a unique identifier) of a record in a table in the database to query.",
)
def view_record(table: str, id: int):
    my_db.view_record(table, id)


@click.command()
@click.option(
    "--table",
    default="milk_production",
    help="This represents the name of the database table to query.",
)
@click.option(
    "--id",
    help="This represents the id (a unique identifier) of a record in a table in the database to query.",
)
def delete_record(table: str, id: int):
    my_db.delete_record(table, id)


@click.command()
@click.option(
    "--table",
    default="milk_production",
    help="This represents the name of the database table to query.",
)
@click.option(
    "--id",
    help="This represents the id (a unique identifier) of a record in a table in the database to query.",
)
@click.option(
    "--name",
    prompt="name of cow",
    help="This represents the name of the animal (cow).",
)
def update_name(table: str, id: int, name: str):
    my_db.update_name(table, id, name)


@click.command()
@click.option(
    "--table",
    default="milk_production",
    help="This represents the name of the database table to query.",
)
@click.option(
    "--id",
    help="This represents the id (a unique identifier) of a record in a table in the database to query.",
)
@click.option(
    "--morning-production",
    prompt="morning production",
    help="This represents the amount (e.g. in Litres) produced by the cow in the morning.",
)
def update_morning(table: str, id: int, morning_production: float):
    my_db.update_morning(table, id, morning_production)


@click.command()
@click.option(
    "--table",
    default="milk_production",
    help="This represents the name of the database table to query.",
)
@click.option(
    "--id",
    help="This represents the id (a unique identifier) of a record in a table in the database to query.",
)
@click.option(
    "--afternoon-production",
    prompt="afternoon production",
    help="This represents the amount (e.g. in Litres) produced by the cow in the afternoon.",
)
def update_noon(table: str, id: int, afternoon_production: float):
    my_db.update_noon(table, id, afternoon_production)


@click.command()
@click.option(
    "--table",
    default="milk_production",
    help="This represents the name of the database table to query.",
)
@click.option(
    "--id",
    help="This represents the id (a unique identifier) of a record in a table in the database to query.",
)
@click.option(
    "--evening-production",
    prompt="evening production",
    help="This represents the amount (e.g. in Litres) produced by the cow in the evening.",
)
def update_evening(table: str, id: int, evening_production: float):
    my_db.update_evening(table, id, evening_production)


@click.command()
@click.option(
    "--table",
    default="milk_production",
    help="This represents the name of the database table to query.",
)
@click.option(
    "--id",
    help="This represents the id (a unique identifier) of a record in a table in the database to query.",
)
@click.option(
    "--production-date",
    prompt="date of production",
    help='This represents the date of production (of milk by each cow), e.g. "2023-10-231"',
)
def update_date(table: str, id: int, production_date: str):
    my_timezone = timezone("Africa/Nairobi")

    date = my_timezone.localize(datetime.strptime(production_date, "%Y-%m-%d"))

    my_db.update_date(table, id, date)


cli.add_command(check_connection)

cli.add_command(create_tables)
cli.add_command(delete_tables)

cli.add_command(view_tables)

cli.add_command(create_record)
cli.add_command(delete_record)

cli.add_command(update_name)
cli.add_command(update_morning)
cli.add_command(update_noon)
cli.add_command(update_evening)
cli.add_command(update_date)

cli.add_command(view_all_records)
cli.add_command(view_record)

if __name__ == "__main__":
    cli()
