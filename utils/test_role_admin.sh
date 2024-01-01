#!/bin/sh

PASSWORD='admin@123'
SERVER='192.168.43.78'

sqlcmd -y 30 -Y 30 -S $SERVER -U aadmin_login -C -P $PASSWORD -d admission