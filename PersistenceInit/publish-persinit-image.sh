echo
echo "Publishing PersInit image"
echo

docker build --push -t containers.github.scch.at/contest/trainticket/persinit:latest ./PersistenceInit \
--label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" \
--label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket"
