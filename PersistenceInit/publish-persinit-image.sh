echo
echo "Publishing PersInit image ts-error-F15"
echo

docker build --push -t containers.github.scch.at/contest/trainticket/persinit:ts-error-F15 ./PersistenceInit \
--label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" \
--label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket"
