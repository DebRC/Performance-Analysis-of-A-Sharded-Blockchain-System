#!/bin/bash

# Total Shard Validators = SHARDCOUNT * SHARD_VALIDATORCOUNT
# Total Shard Observers = SHARDCOUNT * SHARD_OBSERVERCOUNT
# Total Metachain Validators = META_VALIDATORCOUNT
# Total Metachain Observers = META_OBSERVERCOUNT

cd mx-chain-go/scripts/testnet

./config.sh

./start.sh debug
