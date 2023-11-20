#!/bin/bash

PORT=5001

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <server_ip> <port> [-u]"
    exit 1
fi

SERVER_IP=$1
PORT=$2

if [[ $3 == "-u" ]]; then
    iperf -c $SERVER_IP -p $PORT -u
else
    iperf -c $SERVER_IP -p $PORT
fi
