#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Must enter migration name e.g. migration_name"
    exit 1
fi

migrate create -digits 3 -ext sql -dir migrations/ -seq $1
