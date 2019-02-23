# questrade-client
(Simple) Python wrapper for QT

#Start swarm
docker stack deploy -c docker-compose.yml qp

#Kill swarm
docker stack rm qp

#Read logs
docker service logs -f qp_client