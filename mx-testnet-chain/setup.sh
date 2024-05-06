#!/bin/bash

git clone git@github.com:multiversx/mx-chain-go.git
git clone git@github.com:multiversx/mx-chain-proxy-go.git

cp local.sh mx-chain-go/scripts/testnet/

cd mx-chain-go/scripts/testnet
./prerequisites.sh
