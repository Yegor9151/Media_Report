# for use this module install:
# pip install pandas
# pip install pyodbc


import pandas as pd
import pyodbc


class SQLReader:

    def __init__(self, server_ip: str, database: str):
        """Get data from DWH
        
        Params:
            server_ip: server ip
            database: where take data
        """
        self.__connection = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            f"Server={server_ip};"
            f"Database={database};"
            "Trusted_Connection=yes;"
            "autocommit=True;"
        )

    def reading_data(self, query: str):
        """Read SQL query from DWH
        
        Params:
            query: SQL query
            
        Return: result - dataframe
        """
        return pd.read_sql_query(query, self.__connection)