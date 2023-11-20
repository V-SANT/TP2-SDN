#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <host1> <host2>"
    exit 1
fi

xterm -e "ssh $1" &
xterm -e "ssh $2" &
