#!/bin/bash

#if set to 1, each observer will turn off the antiflooding capability, allowing spam in our network
export OBSERVERS_ANTIFLOOD_DISABLE=1

# Shard structure
export SHARDCOUNT=5
export SHARD_VALIDATORCOUNT=5
export SHARD_OBSERVERCOUNT=3
export SHARD_CONSENSUS_SIZE=5

# Metashard structure
export META_VALIDATORCOUNT=5
export META_OBSERVERCOUNT=3
export META_CONSENSUS_SIZE=$META_VALIDATORCOUNT

# ROUNDS_PER_EPOCH represents the number of rounds per epoch. If set to 0, it won't override the node's config
export ROUNDS_PER_EPOCH=100
export ROUND_DURATION=6000

# HYSTERESIS defines the hysteresis value for number of nodes in shard
# export HYSTERESIS=0

# Extra account
export NUM_ADITIONAL_ACCOUNTS=0
export TOTAL_SUPPLY=20000000000000000000000000
export NODE_PRICE=2500000000000000000000
export ADAPTIVITY=false
# export USETMUX=1
# export NODETERMUI=0
