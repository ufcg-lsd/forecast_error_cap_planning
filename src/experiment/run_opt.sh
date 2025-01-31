
#for familia no dir base

docker run -v "${family_path}:/optimizer-files" -v "${family_path}/output:/optimizer-logs" registry-git.lsd.ufcg.edu.br/pedro.serey/awsome-savings:optimizer /bin/sh -c "./run_optimization.sh /optimizer-files /optimizer-logs"