import mariadb
import sys
import logging
from typing import List
from datetime import datetime
import mysql.connector as mariadb


class Repository():
    """
    A class used to store transactions data in database
    """

    def __init__(self, db_address: str, db_user: str, db_password: str,
                 db_port: int, db_name: str,
                 log_file: str = "transactions.log"):

        # setting logger
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s] - %(message)s")

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.log.addHandler(stream_handler)

        try:
            self.conn = mariadb.connect(host=db_address, user=db_user,
                                        password=db_password,
                                        port=db_port,
                                        database=db_name,
                                        autocommit=True)

        except mariadb.Error as e:
            self.log.error(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        self.cur = self.conn.cursor(dictionary=True)

    def __del__(self):
        if hasattr(self, "conn"):
            self.conn.close()

    def _tx_serializer(self, tx_dict: dict) -> List:
        """A method used to convert dictionary with transaction
        data, into list of strings, compatibile to sql query in mariaDB exectute
        function"
        
        Parameters
        ----------
        tx_dict: dict
            dictionary with transaction data
        
        Returns
        -------
        List
            list of transaction data, that sholud be passed to insert statement
            [txTime, txType, baseTokenExchanged,
             tokenExchanged, amountOutMin, oraclePrice, gasPrice, gasUsed,
             gasEstimated, newBaseTokenBalance, newTokenBalance]
        """

        try:
            return [
                int(tx_dict["tx_time"]),
                tx_dict["tx_type"],
                int(tx_dict["base_token_exchanged"]),
                int(tx_dict["token_exchanged"]),
                int(tx_dict["amount_out_min"]),
                int(tx_dict["oracle_price"]),
                int(tx_dict["gas_price"]),
                int(tx_dict["gas_used"]),
                int(tx_dict["gas_estimated"]),
                int(tx_dict["new_base_token_balance"]),
                int(tx_dict["new_token_balance"])]
        except KeyError as e:
            self.log.error(f"Missing transaction attribute: {e.args}")

    def get_transactions(self, limit: int = None) -> List[dict]:
        """
        A method that 
        """
        sql = "SELECT * from transactions"
        if limit is not None:
            sql += f" limit {limit}"
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except mariadb.Error as e:
            self.log.error(f"Error selecting from MariaDB: {e}")

    def insert_transaction(self, tx_data: dict):
        """
        A method that inserts single transaction into a database

        Parameters
        ----------
        tx_data: dict
            all transaction data, that are passed to _serializer method
        """
        tx_serialized_data = self._tx_serializer(tx_data)
        sql = "insert into transactions ( txTime, txType, baseTokenExchanged, tokenExchanged, amountOutMin, oraclePrice, gasPrice, gasUsed, gasEstimated, newBaseTokenBalance, newTokenBalance ) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
        try:
            self.cur.execute(sql, tx_serialized_data)
            self.log.info(
                f"Inserted \'{tx_data['tx_type']}\' transaction -> txId: {self.cur.lastrowid} at timestamp: {datetime.fromtimestamp(tx_data['tx_time'])}")
        except mariadb.Error as e:
            self.log.error(f"Error inserting to MariaDB: {e}")
