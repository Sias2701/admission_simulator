#!/bin/sh

PASSWORD='12345678a@'
SERVER='172.16.50.128'

sqlcmd -y 30 -Y 30 -S $SERVER -U sa -C -P $PASSWORD -i $1
