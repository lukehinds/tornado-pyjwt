#!/bin/sh

if [ -f ./data.db ]; then
   mv ./data.db ./data.db.old
fi

sqlite3 ./data.db < ./schema.bak
