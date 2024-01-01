#!/bin/sh

PASSWORD='guest@456'
SERVER='192.168.43.78'

sqlcmd -y 30 -Y 30 -S $SERVER -U aguest_login -C -P $PASSWORD -d admission