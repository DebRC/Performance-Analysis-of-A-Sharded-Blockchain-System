#!/bin/bash

# Total Shard Validators = SHARDCOUNT * SHARD_VALIDATORCOUNT
# Total Shard Observers = SHARDCOUNT * SHARD_OBSERVERCOUNT
# Total Metachain Validators = META_VALIDATORCOUNT
# Total Metachain Observers = META_OBSERVERCOUNT

cd mx-chain-go/scripts/testnet

touch local.sh

echo "export SHARDCOUNT=3
export SHARD_VALIDATORCOUNT=5
export SHARD_OBSERVERCOUNT=2
export SHARD_CONSENSUS_SIZE=3" > local.sh

./config.sh

./start.sh debug
