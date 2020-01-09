#!/bin/sh
sudo systemctl stop cassandra.service
sudo systemctl stop postgresql
echo "Cassandra and PostgreSQL are turned OFF!"
