import mysql.connector as connector
import os
from dotenv import load_dotenv
class DbModule:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(base_path, 'src/.env')
        load_dotenv(dotenv_path)

    def __db_connect(self):
        try:
            db = connector.connect(
                user = os.getenv('DB_USER'),
                passwd = os.getenv('DB_PASSWORD'),
                host = os.getenv('DB_HOST'),
                db = os.getenv('DB_DATABASE'),
            )
            return db
        except Exception as e:
            print(e)
            raise
    
    def __get_value(self, values: list):
        return '({parameters})'.format(
            parameters = ', '.join(str('\'' + str(parameter) + '\'') for parameter in values)
        )

    def insert(self, table: str, values: dict):
        cnx = self.__db_connect()
        cur = cnx.cursor()

        columns = list(values.keys())
        parameters = list(values.values())


        sql = "INSERT INTO `{table}` ({columns}) VALUES ({values})".format(
            table = table,
            columns = ', '.join(columns),
            values =  ', '.join(str('\'' + str(parameter) + '\'') for parameter in parameters)
        )

        try:
            cur.execute(sql)
            cnx.commit()
            return True
        except:
            cnx.rollback()
            raise

    def multiple_insert(self, table: str, columns: list, values: list):
        cnx = self.__db_connect()
        cur = cnx.cursor()
        parameters = []
        for value in values:
            parameters.append(self.__get_value(value))

        sql = "INSERT INTO `{table}` ({columns}) VALUES {values}".format(
            table = table,
            columns = ', '.join(columns),
            values =  ', '.join(parameters)
        )

        try:
            cur.execute(sql)
            cnx.commit()
            return True
        except:
            cnx.rollback()
            raise

    def select(self, sql: str):
        cnx = self.__db_connect()
        cur = cnx.cursor(dictionary=True)
        try:
            cur.execute(sql)
            response = cur.fetchall()
            cur.close()
        except:
            raise

        return response
    
    def update(self, sql: str):
        cnx = self.__db_connect()
        cur = cnx.cursor()
        try:
            cur.execute(sql)
            cnx.commit()
        except:
            cnx.rollback()
            raise
    
