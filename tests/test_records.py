from click.testing import CliRunner
from db_cli.psql import (
    check_connection,
    create_tables,
    delete_tables,
    create_record,
    update_name,
    update_morning,
    update_noon,
    update_evening,
    update_date,
    delete_record,
    view_all_records,
    view_record,
)

runner = CliRunner()


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


def test_check_connection():
    res = runner.invoke(check_connection)

    assert res.exit_code == 0
    assert res.output == "\nConnection successful.\n\n"


def test_create_record():
    input_params = [
        "--animal",
        "Cow 1",
        "--morning-production",
        10.5,
        "--afternoon-production",
        12.3,
        "--evening-production",
        9.2,
        "--production-unit",
        "Litres",
        "--production-date",
        "2023-06-25",
    ]

    res = runner.invoke(create_record, input_params)

    assert res.exit_code == 0
    assert res.output == "\nRecord has been created successfully.\n\n"


def test_view_all_records():
    res = runner.invoke(view_all_records)

    assert res.exit_code == 0
    assert res.output.splitlines() == [
        "",
        "List of all the records in table 'milk_production':",
        "",
        "1. | id: 1 | cow: Cow 1 | morning: 10.5 | noon: 12.3 | evening: 9.2 | unit: Litres | date: 2023-06-25",
        "",
    ]


def test_view_record():
    input_params = ["--id", 1]

    res = runner.invoke(view_record, input_params)

    assert res.exit_code == 0
    assert res.output.splitlines() == [
        "",
        "Record of id '1' in table 'milk_production':",
        "",
        "1. | id: 1 | cow: Cow 1 | morning: 10.5 | noon: 12.3 | evening: 9.2 | unit: Litres | date: 2023-06-25",
        "",
    ]


def test_update_name():
    input_params = ["--id", 1, "--name", "Cow 2"]

    res = runner.invoke(update_name, input_params)

    assert res.exit_code == 0
    assert res.output == "\nRecord has been updated successfully.\n\n"


def test_update_morning():
    input_params = ["--id", 1, "--morning-production", 5.8]

    res = runner.invoke(update_morning, input_params)

    assert res.exit_code == 0
    assert res.output == "\nRecord has been updated successfully.\n\n"


def test_update_noon():
    input_params = ["--id", 1, "--afternoon-production", 7.8]

    res = runner.invoke(update_noon, input_params)

    assert res.exit_code == 0
    assert res.output == "\nRecord has been updated successfully.\n\n"


def test_update_evening():
    input_params = ["--id", 1, "--evening-production", 6.6]

    res = runner.invoke(update_evening, input_params)

    assert res.exit_code == 0
    assert res.output == "\nRecord has been updated successfully.\n\n"


def test_update_date():
    input_params = ["--id", 1, "--production-date", "2023-8-12"]

    res = runner.invoke(update_date, input_params)

    assert res.exit_code == 0
    assert res.output == "\nRecord has been updated successfully.\n\n"


def test_delete_record():
    input_params = ["--id", 1]

    res = runner.invoke(delete_record, input_params)

    assert res.exit_code == 0
    assert res.output == "\nRecord has been deleted successfully.\n\n"


def test_delete_tables():
    res = runner.invoke(delete_tables)

    assert res.exit_code == 0
    assert res.output == "\nTable milk_production has been deleted successfully.\n\n"
