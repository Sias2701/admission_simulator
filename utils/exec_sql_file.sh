#!/bin/sh

PASSWORD='12345678a@'
SERVER='192.168.43.78'

sqlcmd -y 30 -Y 30 -S $SERVER -U sa -C -P $PASSWORD -i $1
