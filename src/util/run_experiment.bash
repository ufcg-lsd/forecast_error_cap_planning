#!/bin/bash

# Usage: ./run_experiment.sh <EXEC_DIR> <DEMAND_FILE>
# Example: ./run_experiment.sh exec_2_1_2023_spot 2023_with_spot.csv

set -e

EXEC_DIR="$1"
DEMAND_FILE="$2"

EC2_IP="172.31.21.41"
PEM_KEY="$HOME/.ssh/solr.pem"
REMOTE_USER="ec2-user"

LOCAL_BASE_DIR="$HOME/Documents/data_experiments_forecast"
REMOTE_PROJ_DIR="/home/ec2-user/forecast_error_cap_planning"
REMOTE_BASE_DIR="$REMOTE_PROJ_DIR/src/experiment"

if [ -z "$EXEC_DIR" ] || [ -z "$DEMAND_FILE" ]; then
    echo "Usage: <EXEC_DIR> <DEMAND_FILE>"
    exit 1
fi

echo ">>> Copying $EXEC_DIR to instance $EC2_IP..."
scp -r -i "$PEM_KEY" "$LOCAL_BASE_DIR/$EXEC_DIR" \
    $REMOTE_USER@"$EC2_IP":"$REMOTE_BASE_DIR/data"

echo ">>> Running commands on $EC2_IP..."
ssh -i "$PEM_KEY" $REMOTE_USER@"$EC2_IP" << EOF
    set -e

    echo ">>> Creating output directory..."
    mkdir -p $REMOTE_BASE_DIR/output/$EXEC_DIR

    echo ">>> Starting Docker..."
    sudo systemctl start docker

    echo ">>> Running before_opt.py..."
    cd $REMOTE_PROJ_DIR && \
    poetry run python3 $REMOTE_BASE_DIR/before_opt.py \
        $REMOTE_BASE_DIR/data/$EXEC_DIR/$DEMAND_FILE \
        $REMOTE_BASE_DIR/data/$EXEC_DIR/prices.csv \
        $REMOTE_BASE_DIR/data/$EXEC_DIR/error_configs.csv \
        $REMOTE_BASE_DIR/output/$EXEC_DIR

    echo ">>> Running optimization script in background..."
    nohup sudo bash $REMOTE_BASE_DIR/run_opt.sh \
        $REMOTE_BASE_DIR/output/$EXEC_DIR/optimizations/
    
    # Check if background process started successfully
    sleep 2  # Allow time for process to start
    if ! ps -p $! > /dev/null; then
        echo "ERROR: Optimization script failed to start."
        exit 1
    fi
EOF

echo ">>> Done! Experiment $EXEC_DIR with demand file $DEMAND_FILE started on $EC2_IP."
