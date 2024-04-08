#!/bin/bash

cd mx-chain-go/scripts/testnet
./clean.sh

cd ..
cd ..
cd ..

sudo rm -rf mx-chain-deploy-go/ mx-chain-go/ mx-chain-proxy-go/
