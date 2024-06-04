import sqlite3

class ConnectionSQLite:
    def __init__(self, database_name):
        self.name = database_name
    
    def get_con(self):
        connection_db = sqlite3.connect(self.name)
        return connection_db
        
    def query(self, query):
        # Connect to DB
        connection_db = sqlite3.connect(self.name)
        cursor_obj = connection_db.cursor()
        try:
            # Execute query
            cursor_obj.execute(query)
            # Disconnect DB
            connection_db.commit()
            connection_db.close()
            # Status return
            return f"Berhasil Query"
        except Exception as e:
            print(f"Gagal Query {str(e)}")
    
    def createTable(self, table_name, *columns):
        # Drop table if exists
        self.query(f"DROP TABLE IF EXISTS {table_name}")
        query = f"CREATE TABLE {table_name} ("
        # Insert column
        for column in columns:
            query += f"{column}"
            if column == columns[-1]:
                query += ");"
            else:
                query += ", "
        # Create Table
        try:
            self.query(query)
            return query
        except Exception as e:
            print(f"Gagal Membuat Table {str(e)}")
    
    def insertTable(self, table_name, *values, **column_values):
        query = f"INSERT INTO {table_name}"
        # Just values insert
        if values:
            query += " VALUES ("
            for value in values:
                query += f"'{value}'"
                if value == values[-1]:
                    query += ");"
                else:
                    query += ", "
        # With column name insert
        elif column_values:
            columns = list(column_values.keys())
            values = list(column_values.values())
            # Insert columns
            query += " ("
            for column in columns:
                query += f"{column}"
                if column == columns[-1]:
                    query += ")"
                else:
                    query += ", "
            # insert values
            query += " VALUES ("
            for value in values:
                query += f"'{value}'"
                if value == values[-1]:
                    query += ");"
                else:
                    query += ", "
        # Insert table
        try:
            self.query(query)
            return f"Berhasil Insert Table {table_name}"
        except Exception as e:
            print(f"Gagal Insert Table {str(e)}")
        
    def selectTable(self, table_name, columns='*', *conditions, ordetByColumn=None, orderByType='DESC', limit=None):
        query = f"SELECT {columns} FROM {table_name}"
        # IF condition set
        if conditions:
            query += " WHERE"
            for condition in conditions:
                query += f" {condition}"
        # IF OrderBy set
        if ordetByColumn and orderByType:
            query += f" ORDER BY {ordetByColumn} {orderByType}"
        # IF Limit set
        if limit:
            query += f" LIMIT {limit}"
        query += ";"
        try:
            # Select Object
            con = self.get_con()
            obj = con.cursor()
            obj.execute(query)
            # Get Object
            data = obj.fetchall()
            # Disconnect DB
            con.commit()
            con.close()
            # Return object data
            return data
        except Exception as e:
            print(f"Gagal Select Object {str(e)}")
            
    def dropRecord(self, table_name, id):
        query = f"DELETE FROM {table_name} WHERE id = {id}"
        # Delete Record
        try:
            self.query(query)
            return f"Behashil menghapus Record pada Table {table_name}"
        except Exception as e:
            print(f"Gagal Menghapus Record pada Table: {str(e)}")
        