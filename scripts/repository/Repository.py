import mariadb
import sys
import logging
from typing import List


class Repository():
    """
    A class used to store transactions data in database
    """

    def __init__(self, db_address: str, db_user: str, db_password: str, db_port: int, db_name: str):
        try:
            self.conn = mariadb.connect(host=db_address, user=db_user, password=db_password, port=db_port,
                                        database=db_name)

        except mariadb.Error as e:
            logging.error(f"Error connecting to MariaDB Platform: {e}")
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

        return [str(tx_dict["tx_time"]), int(tx_dict["tx_type"], tx_dict["base_token_exchanged"],
                tx_dict["token_exchanged"], tx_dict["amount_out_min"], tx_dict["oracle_price"], tx_dict["gas_price"],
                tx_dict["gas_used"], tx_dict["gas_estimated"], tx_dict["new_base_token_balance"],
                tx_dict["new_token_balance"]]

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
            logging.error(f"Error selecting from MariaDB: {e}")

    def insert_transaction(self, tx_data: dict):
        """
        A method that inserts single transaction into a database

        Parameters
        ----------
        tx_data: dict
            all transaction data, that are passed to _serializer method
        """
        tx_serialized_data = self._tx_serializer(tx_data)
        print(tx_serialized_data)
        sql = """insert into transactions (
              txTime, txType, baseTokenExchanged, 
              tokenExchanged, amountOutMin, oraclePrice, gasPrice, gasUsed,
              gasEstimated, newBaseTokenBalance, newTokenBalance 
            ) 
            values 
              (
                %s,
                %s,
                %d,
                %d,
                %d,
                %d,
                %d,
                %d,
                %d,
                %d,
                %d
              )
"""
        try:
            self.cur.execute(sql, tx_serialized_data)
        except mariadb.Error as e:
            logging.error(f"Error inserting to MariaDB: {e}")
