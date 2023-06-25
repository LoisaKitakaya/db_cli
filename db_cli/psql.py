import click
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
                        f"Connection successful.\n",
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
                    "The following tables have been created:\n",
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

    def view_tables(self):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            )

            tables = cur.fetchall()

            click.echo(
                click.style(
                    "List of all the tables in the database:\n",
                    fg="cyan",
                    bold=True,
                    underline=True,
                )
            )

            count = 1

            for table in tables:
                click.echo(click.style(f"{count}. {table}\n", fg="cyan", bold=True))

                count += 1

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
        morning_production: int,
        afternoon_production: int,
        evening_production: int,
        production_unit: str,
        production_date: datetime,
    ):
        conn = None

        try:
            conn = psycopg2.connect(**self.db)

            cur = conn.cursor()

            cur.execute(
                f"INSERT INTO milk_production(animal, morning_production, afternoon_production, evening_production, production_unit, production_date), ({animal}, {morning_production}, { afternoon_production}, {evening_production}, {production_unit}, {production_date})"
            )

            conn.commit()

            click.echo(
                click.style(
                    "Record has been created successfully.", fg="green", bold=True
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
def view_tables():
    my_db.view_tables()


@click.command()
def create_record():
    pass


cli.add_command(check_connection)

cli.add_command(create_tables)
cli.add_command(view_tables)

cli.add_command(create_record)


if __name__ == "__main__":
    cli()