EXEC_PATH="$1"
REMOTE_BASE_DIR="/home/ec2-user/forecast_error_cap_planning/src/experiment/output/"
MAIN_PATH="${REMOTE_BASE_DIR}/${EXEC_PATH}"

EC2_IP="172.31.21.41"
REMOTE_USER="ec2-user"

ssh -i ~/.ssh/solr.pem $REMOTE_USER@"$EC2_IP" << EOF
    total_num_families=0
    optimized_families=0

    for scenario_path in "$MAIN_PATH"*/; do
        for family_path in "\$scenario_path"*; do
            total_num_families=\$((total_num_families + 1))
            if [ -f "\$family_path/output/result_cost.csv" ]; then
                optimized_families=\$((optimized_families + 1))
                continue
            fi
        done
    done

    echo "Total families: \$total_num_families"
    echo "Optimized families: \$optimized_families"

    if [ \$optimized_families -eq \$total_num_families ]; then
        echo "All families (\$total_num_families) optimized successfully."
    else
        echo "\$((total_num_families - optimized_families)) families were not optimized."
    fi
EOF

