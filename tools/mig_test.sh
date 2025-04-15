#!/usr/bin/env bash

CONFIG=$1
CHECKPOINT=$2
GPUS=$3
NNODES=${NNODES:-1}
NODE_RANK=${NODE_RANK:-0}
PORT=${PORT:-29500}
MASTER_ADDR=${MASTER_ADDR:-"127.0.0.1"}

# Check CUDA version
CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $6}' | cut -c2-5)
echo "CUDA Version: $CUDA_VERSION"

# Set NCCL version based on CUDA version
if [ "$CUDA_VERSION" = "11.3" ]; then
    export NCCL_VERSION=2.11.4
elif [ "$CUDA_VERSION" = "11.6" ]; then
    export NCCL_VERSION=2.12.12
elif [ "$CUDA_VERSION" = "11.7" ]; then
    export NCCL_VERSION=2.14.3
else
    echo "Warning: Unsupported CUDA version $CUDA_VERSION"
    export NCCL_VERSION=2.11.4  # Default to a stable version
fi

echo "Using NCCL Version: $NCCL_VERSION"

# Set CUDA_VISIBLE_DEVICES for MIG
export CUDA_VISIBLE_DEVICES=0,1,2,3

# Set environment variables for distributed training
export MASTER_PORT=$PORT
export MASTER_ADDR=$MASTER_ADDR
export WORLD_SIZE=$GPUS
export LOCAL_RANK=$SLURM_LOCALID
export RANK=$SLURM_PROCID
export LOCAL_WORLD_SIZE=$SLURM_NTASKS_PER_NODE

# Set NCCL environment variables for MIG
export NCCL_DEBUG=INFO
export NCCL_IB_DISABLE=1
export NCCL_P2P_DISABLE=1
export NCCL_SOCKET_IFNAME=^docker0,lo
export NCCL_DEBUG_SUBSYS=ALL
export NCCL_SOCKET_NTHREADS=1
export NCCL_NSOCKS_PERTHREAD=1
export NCCL_MIN_NCHANNELS=1

# Set MKL threads
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1

PYTHONPATH="$(dirname $0)/..":$PYTHONPATH \
python -m torch.distributed.run \
    --nproc_per_node=$GPUS \
    --nnodes=$NNODES \
    --node_rank=$NODE_RANK \
    --master_addr=$MASTER_ADDR \
    --master_port=$PORT \
    $(dirname "$0")/test.py \
    $CONFIG \
    $CHECKPOINT \
    --launcher pytorch \
    ${@:4} 