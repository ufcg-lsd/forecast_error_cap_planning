#!/bin/bash

# Usage: ./run_experiment.sh <EC2_IP> <LOCAL_DIR> <DEMAND_FILE>
# Example: ./run_experiment.sh 172.31.21.41 exec_2_1_2023_spot 2023_with_spot.csv

EC2_IP="$1"
LOCAL_DIR="$2"
DEMAND_FILE="$3"
PEM_KEY="~/.ssh/solr.pem"
LOCAL_BASE_DIR="~/Documents/data_experiments_forecast"
REMOTE_USER="ec2-user"
REMOTE_BASE_DIR="~/forecast_error_cap_planning/src/experiment"

if [ -z "$EC2_IP" ] || [ -z "$LOCAL_DIR" ] || [ -z "$DEMAND_FILE" ]; then
    echo "Usage: $0 <EC2_IP> <LOCAL_DIR> <DEMAND_FILE>"
    exit 1
fi

echo ">>> Copying $LOCAL_DIR to instance $EC2_IP..."
scp -r -i "$PEM_KEY" "$LOCAL_BASE_DIR/$LOCAL_DIR" \
    $REMOTE_USER@"$EC2_IP":"$REMOTE_BASE_DIR/data"

echo ">>> Running commands on $EC2_IP..."
ssh -i "$PEM_KEY" $REMOTE_USER@"$EC2_IP" bash << EOF
    set -e
    cd ~/forecast_error_cap_planning

    echo ">>> Creating output directory..."
    mkdir -p src/experiment/output/$LOCAL_DIR

    echo ">>> Starting Docker..."
    sudo systemctl start docker

    echo ">>> Running before_opt.py..."
    poetry run python3 src/experiment/before_opt.py \
        src/experiment/data/$LOCAL_DIR/$DEMAND_FILE \
        src/experiment/data/$LOCAL_DIR/prices.csv \
        src/experiment/data/$LOCAL_DIR/error_configs.csv \
        src/experiment/output/$LOCAL_DIR

    echo ">>> Running optimization script in background..."
    nohup sudo bash src/experiment/run_opt.sh \
        /home/ec2-user/forecast_error_cap_planning/src/experiment/output/$LOCAL_DIR/optimizations/ \
        > ~/run_opt_${LOCAL_DIR}.log 2>&1 &
EOF

echo ">>> Done! Experiment $LOCAL_DIR with demand file $DEMAND_FILE started on $EC2_IP."
