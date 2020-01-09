#!/bin/sh
sudo systemctl start cassandra.service
sudo systemctl start postgresql
echo "Cassandra and PostgreSQL are turned ON!"
