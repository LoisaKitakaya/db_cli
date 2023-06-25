from click.testing import CliRunner
from db_cli.psql import check_connection, create_tables, view_tables, delete_tables

runner = CliRunner()


def test_check_connection():
    res = runner.invoke(check_connection)

    assert res.exit_code == 0
    assert res.output == "\nConnection successful.\n\n"


def test_create_tables():
    res = runner.invoke(create_tables)

    assert res.exit_code == 0
    assert res.output.splitlines() == [
        "",
        "The following tables have been created:",
        "",
        "1. ('milk_production',)",
        "",
    ]


def test_view_tables():
    res = runner.invoke(view_tables)

    assert res.exit_code == 0
    assert res.output.splitlines() == [
        "",
        "List of all the tables in the database:",
        "",
        "1. ('milk_production',)",
        "",
    ]


def test_delete_tables():
    res = runner.invoke(delete_tables)

    assert res.exit_code == 0
    assert res.output == "\nTable milk_production has been deleted successfully.\n\n"
