echo
echo "Publishing PersInit image VERSION_XXXXX"
echo

docker build --push -t containers.github.scch.at/contest/trainticket/persinit:VERSION_XXXXX ./PersistenceInit \
--label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" \
--label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket"
