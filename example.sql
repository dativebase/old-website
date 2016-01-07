-- WARNING: do not run this script. These are examples.
--
-- start-block: mysql-create-database
CREATE DATABASE myold DEFAULT CHARACTER SET utf8;
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP ON myold.* TO 'myuser'@'localhost';
-- end-block: mysql-create-database

