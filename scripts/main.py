from scripts.repository.Repository import Repository
from os import environ
import time


def main():
    db_address = environ["DB_ADDRESS"]
    db_user = environ["DB_USER"]
    db_password = environ["DB_PASSWORD"]
    db_name = environ["TEST_DB_NAME"]
    db_port = int(environ["DB_PORT"])
    repository = Repository(db_address=db_address, db_user=db_user,
                            db_password=db_password, db_port=db_port,
                            db_name=db_name)

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


if __name__ == '__main__':
    main()
