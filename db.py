from psycopg_pool import ConnectionPool

conninfo = "postgres://postgres:oeasypg@localhost:5432/oeasydb"
pool = ConnectionPool(conninfo)
