main_path="$1"

for scenario_path in "$main_path"*/; do
    echo "Starting: $scenario_path"
    for family_path in "$scenario_path"*; do
        echo "Optimizing: $family_path"
        docker run -v "${family_path}:/optimizer-files" -v "${family_path}/output:/optimizer-logs" registry-git.lsd.ufcg.edu.br/pedro.serey/awsome-savings:optimizer /bin/sh -c "./run_optimization.sh /optimizer-files /optimizer-logs"
    done
done