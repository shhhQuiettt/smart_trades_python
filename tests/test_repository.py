import mariadb
import pytest
from scripts.repository.Repository import Repository
import time


def test_with_invalid_db_programm_exits():
    with pytest.raises(SystemExit) as e:
        invalid_repository = Repository("invalid", "args", "what", "the hell", "isgoingon")
    assert e.type == SystemExit
    assert e.value.code == 1


def test_insert_transaction():
    db_address = "localhost"
    db_user = "root"
    db_password = ""
    db_name = "test_smart_trades_db"
    db_port = 3306
    repository = Repository(db_address, db_user, db_password, db_port, db_name)

    tx_data = {
        "tx_time": time.time(),
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
