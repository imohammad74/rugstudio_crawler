import sqlite3
from sqlite3 import Error


class DBManagement:

    @staticmethod
    def db_file():
        db_file = 'rugs_database.db'
        return db_file

    @staticmethod
    def db_table():
        db_table = ['rugstudio_url', 'brands', 'pdp', 'no_data', 'sqlite_sequence', 'check_prices', 'design_id']
        return db_table

    @staticmethod
    def create_connection(db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def create_table(db_file: str, table_name: str, columns: list):
        """Create table """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            for column in columns:
                query = f'''CREATE TABLE IF NOT EXISTS {table_name}
                                                        ([{column['name']}] 
                                                        {column['type']} 
                                                        {"PRIMARY KEY" if column['is_primary'] == True else ''}
                                                        {"not null" if column['is_null'] == True else ''}
                                                        {"AUTOINCREMENT" if column['is_autoincrement'] == True else ''}
                                                        )
                                                            '''
                c.execute(query)
                try:
                    query = f'''ALTER TABLE {table_name} ADD COLUMN 
                                                        [{column['name']}] 
                                                        {column['type']} 
                                                        {"PRIMARY KEY" if column["is_primary"] == True else ''}
                                                        {"not null" if column['is_null'] == False else ''}
                                                        {"AUTOINCREMENT" if column['is_autoincrement'] == True else ''}
                                                            '''
                    c.execute(query)
                    print(f'{column["name"]} added.')
                except Error as e:
                    print(e)
                    continue
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def add_columns(db_file: str, table_name: str, columns: list):
        """Add new columns to table"""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            for column in columns:
                try:
                    query = f'''ALTER TABLE {table_name} ADD COLUMN 
                                                        [{column['name']}] 
                                                        {column['type']} 
                                                        {"PRIMARY KEY" if column["is_primary"] == True else ''}
                                                        {"not null" if column['is_null'] == False else ''}
                                                        {"autoincrement" if column['is_autoincrement'] == True else ''} 
                                                            '''
                    c.execute(query)
                    print(f'{column["name"]} added.')
                except Error as e:
                    print(e)
                    continue
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete_columns(db_file: str, table_name: str, columns: list):
        """Delete list of columns"""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            for column in columns:
                try:
                    query = f'''ALTER TABLE {table_name} DROP {column['name']}'''
                    c.execute(query)
                    print(f'{column["name"]} deleted.')
                except Error as e:
                    print(e)
                    continue
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def insert_rows(db_file: str, table_name: str, columns: list, **kwargs):
        """Insert new rows to table
        columns example : [{'column':'col1', 'value':'value1'}]
        """
        log = kwargs['log'] if 'log' in kwargs else False
        conn = None
        if len(columns) > 1:
            columns_names = tuple([column['column'] for column in columns])
            columns_values = tuple([column['value'] if not None else "" for column in columns])
        else:
            columns_names = f'("{columns[0]["column"]}")'
            columns_values = f'("{columns[0]["value"]}")'
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            try:
                query = f'''INSERT INTO {table_name} {columns_names} VALUES {columns_values}'''
                c.execute(query)
                conn.commit()
                # c.close()
                if log is True:
                    print(f'{"All rows added." if len(columns_names) > 1 else "Row added."}')
            except Error as e:
                print(e)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete_rows(db_file: str, table_name: str, condition: str):
        """Delete rows from table with some condition"""
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            try:
                query = f'''DELETE FROM {table_name} WHERE {condition}'''
                c.execute(query)
                print('Rows deleted.')
            except Error as e:
                print(e)
        except Error as e:
            print(e)

    @staticmethod
    def update_rows(db_file: str, table_name: str, condition: str, columns: list):
        """Update rows with some conditions """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            columns_names = [column['column'].lower() for column in columns]
            columns_values = [column['value'] for column in columns]
            set_string = ""
            for i in range(len(columns)):
                set_string += f'{columns_names[i]} = "{columns_values[i]}", '
            set_string = set_string.strip(', ')
            try:
                query = f'''UPDATE {table_name} SET {set_string} WHERE {condition} '''
                c.execute(query)
                conn.commit()
                # print('Row updated.')
            except Error as e:
                print(e)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def fetch_datas(db_file: str, table_name: str, all_columns: bool, **kwargs):  # columns: list, condition: s tr
        """
        fetch data from table

        fetch all date: (db_file: 'db_file', table_name: 'table_name', all_data: True)

        fetch some columns : (db_file: 'db_file', table_name: 'table_name', all_data: False, columns= ['col1,'col2'])

        fetch with limitation : (db_file:'db_file', table_name:'table_name', all_data:False, limit="start_row,period")

        fetch with condition : (db_file: 'db_file', table_name: 'table_name', all_data: False, condition = "id =1 and
         col2= 3")
        """
        conn = None
        condition = kwargs['condition'] if 'condition' in kwargs else None
        columns = kwargs['columns'] if 'columns' in kwargs else None
        limit = kwargs['limit'] if 'limit' in kwargs else None
        col_string = ""
        if columns is not None:
            for i in range(len(columns)):
                col_string = f'{col_string}{columns[i]}, '
            col_string = col_string.strip(', ')
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            try:
                query = f'''SELECT {'*' if all_columns == True else col_string} FROM {table_name}
                            {"" if condition is None else "WHERE"} {condition if condition is not None else ""}
                            {"" if limit is None else "LIMIT"} {limit if limit is not None else ""} 
                         '''
                c.execute(query)
                conn.commit()
                datas = c.fetchall()
                # print(datas)
                # print('fetch datas.')
                return datas
            except Error as e:
                print(e)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def copy_column(db_file: str, table_name: str, columns: list):
        """Copy a column to another that
        example: copy_column(db_file= db.db_file, db_table= db.table_name, columns=['source_col', 'destination_col']
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            try:
                query = f'''UPDATE {table_name} SET {columns[1]} = {columns[0]} '''
                c.execute(query)
                conn.commit()
            except Error as e:
                print(e)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def custom_query(db_file: str, query: str):
        """Copy a column to another that
        example: custom_query(db_file= db.db_file, query="SELECT last_price, new_price,
        (CASE WHEN (new_price-last_price)=0 THEN NULL ELSE 0 END) as 'is_warning' FROM check_prices;"
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            try:
                query = f'''{query} '''
                print(query)
                c.execute(query)
                conn.commit()
            except Error as e:
                print(e)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    # todo:delete_table
