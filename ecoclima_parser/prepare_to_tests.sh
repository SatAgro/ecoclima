#!/bin/sh
sudo -u postgres psql <<EOF
drop database testdb;
drop user test;
create database testdb;
create user test with password 'test';
alter default privileges in schema public grant all on tables to test;
alter default privileges in schema public grant all on sequences to test;
grant all privileges on database testdb to test;
grant postgres to test;
EOF
