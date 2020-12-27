import mysql.connector as connector
import os
from dotenv import load_dotenv
class DbModule:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(base_path, '.env')
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

    
    def insert(self, table: str, columns: list, values: list):
        cnx = self.__db_connect()
        cur = cnx.cursor()
        parameters=[]
        for parameter in values:
            if isinstance(parameter, str):
                parameters.append(str('\'' + parameter + '\''))
            else:
                if parameter==None:
                    parameters.append("NULL")
                else:
                    parameters.append(str(parameter))
        new_columns=[f"%({x})s" for x in columns]
        new_columns=", ".join(columns)
        parameters=", ".join(parameters)
        sql=f"INSERT INTO {table} ({new_columns}) VALUES ({parameters})"
        try:
            cur.execute(sql)
            cnx.commit()
            return True
        except:
            cnx.rollback()
            raise
        
        


    def allinsert(self, table: str,values: list):
        cnx = self.__db_connect()
        cur = cnx.cursor()
        parameters=[]
        for parameter in values:
            if isinstance(parameter, str):
                parameters.append(str('\'' + parameter + '\''))
            else:
                if parameter==None:
                    parameters.append("NULL")
                else:
                    parameters.append(str(parameter))
        parameters=", ".join(parameters)
        sql=f"INSERT INTO {table} VALUES ({parameters})"
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
    
