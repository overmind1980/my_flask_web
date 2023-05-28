ALTER USER postgres WITH PASSWORD 'oeasypg';
CREATE DATABASE oeasydb;
\c oeasydb;
CREATE TABLE IF NOT EXISTS test(id serial PRIMARY KEY, num integer, data text);
INSERT INTO test(num, data) VALUES (123, 'abc');
INSERT INTO test(num, data) VALUES (456, 'ooo');
