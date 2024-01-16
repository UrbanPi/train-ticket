echo
echo "Publishing EvoMaster image"
echo

docker build --push -t containers.github.scch.at/contest/trainticket/evomaster:latest ./EvoMaster \
--label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" \
--label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket"
