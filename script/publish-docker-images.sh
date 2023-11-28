#!/usr/bin/env bash
set -eux

echo
echo "Publishing images, Repo: $1, Tag: error-f16"
echo
for dir in ts-*; do
    if [[ -d $dir ]]; then
        if [[ -n $(ls "$dir" | grep -i Dockerfile) ]]; then
            echo "build ${dir}"
	    # Must use `buildx` as docker build tool
            docker build --push -t "$1"/"${dir}":error-f16 "$dir"\
            --label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" \
            --label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket" &
        fi
    fi
done
