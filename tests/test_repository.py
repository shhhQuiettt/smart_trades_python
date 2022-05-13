from testfixtures import LogCapture
import pytest
from scripts.repository.Repository import Repository
import time
from datetime import datetime
from os import environ


@pytest.fixture()
def repository():
    """
    Fixture that creates valid repository, and cleans transaction
    table in test database
    after test.
    Environmental variables are loaded by brownie from .env file
    specified in brownie-config.yaml
    """

    db_address = environ["DB_ADDRESS"]
    db_user = environ["DB_USER"]
    db_password = environ["DB_PASSWORD"]
    db_name = environ["TEST_DB_NAME"]
    db_port = int(environ["DB_PORT"])
    repository = Repository(db_address=db_address, db_user=db_user,
                            db_password=db_password, db_port=db_port,
                            db_name=db_name)
    yield repository
    repository.cur.execute("delete from transactions where txId < 1000")
    # repository.cur.execute("delete from transaction")


def test_with_invalid_db_programm_exits():
    with pytest.raises(SystemExit) as e:
        invalid_repository = Repository("invalid", "args", "what",
                                        9, "isgoingon")
    assert e.type == SystemExit
    assert e.value.code == 1


def test_insert_transaction(repository):
    tx_data = {
        "tx_time": int(time.time()),
        "tx_type": "buy",
        "base_token_exchanged": 100 * 10 ** 18,
        "token_exchanged": 0.1 * 10 ** 18,
        "amount_out_min": 0.1 * 10 ** 18,
        "oracle_price": 0.75 * 10 ** 18,
        "gas_price": 0.0000035 * 10 ** 18,
        "gas_used": 0.00004 * 10 ** 18,
        "gas_estimated": 0.00004 * 10 ** 18,
        "new_base_token_balance": 100 * 10 ** 18,
        "new_token_balance": 1030 * 10 ** 18
    }

    repository.insert_transaction(tx_data)
    # fr"Inserted \'buy\' transaction -> txId: (?s)  at {datetime.fromtimestamp(tx_data['tx_time'])}")
    assert len(repository.get_transactions()) == 1
