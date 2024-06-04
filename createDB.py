from module.db import ConnectionSQLite

db = ConnectionSQLite("database.sqlite")

db.createTable("forests", 'id INTEGER PRIMARY KEY AUTOINCREMENT', 'name TEXT NOT NULL', 'ndvi DECIMAL(10,2) NOT NULL', 'reflectance DECIMAL(10,2) NOT NULL', 'status VARHAR(255) NOT NULL CHECK (status IN ("sehat", "sakit"))', 'quality INTEGER NOT NULL', 'path_forest TEXT NOT NULL', 'path_plot TEXT DEFAULT NULL')

db.createTable("users", "username VARCHAR(255) PRIMARY KEY", "name TEXT NOT NULL", "password TEXT NOT NULL")