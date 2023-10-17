#!/usr/bin/env bash
set -eux

echo
echo "Publishing OTEL images"
echo

docker build --push -t containers.github.scch.at/contest/trainticket/otel-agent:latest ./OTEL/otel_agent \
--label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" \
--label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket"

docker build --push -t containers.github.scch.at/contest/trainticket/otel-collector:latest ./OTEL/otel_collector \
--label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" \
--label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket"