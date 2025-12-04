echo
echo "Publishing Microservicecontroller image for fault branches"
echo

docker build --push -t containers.github.scch.at/contest/trainticket/microservicecontroller:fault-branches ./ \
--label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" \
--label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket"
