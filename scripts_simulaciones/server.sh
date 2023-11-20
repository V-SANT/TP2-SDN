#!/bin/bash

PORT=5001

if [ ! -z "$1" ]; then
    PORT=$1
fi

if [[ $2 == "-u" ]]; then
    iperf -s -p $PORT -i 1 -u
else
    iperf -s -p $PORT -i 1
fi
