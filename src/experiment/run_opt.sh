main_path="$1"

for family_path in "$main_path"/*/; do
    echo "Processing: $family_path"
    docker run -v "${family_path}:/optimizer-files" -v "${family_path}/output:/optimizer-logs" registry-git.lsd.ufcg.edu.br/pedro.serey/awsome-savings:optimizer /bin/sh -c "./run_optimization.sh /optimizer-files /optimizer-logs"
    fi
done