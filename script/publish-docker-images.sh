#!/usr/bin/env bash
set -eux
# Problem: Building and pushing each container sequentially is awfully slow but building and pushing
# in parallel is too fast (hits the request limit of the GitHub instance).
# Hence, we build in parallel and wait for each process to finish and then push sequentially.
tag=$2
echo
echo "Publishing images, Repo: $1, Tag: " "${tag}"
echo
pids=()
for dir in ts-*; do
    if [[ -d $dir ]]; then
        if [[ -n $(ls "$dir" | grep -i Dockerfile) ]]; then
            echo "build ${dir}"
	    # Must use `buildx` as docker build tool
            docker build -t "$1"/"${dir}":"${tag}" "$dir"\
            --label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" \
            --label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket" &
            pids+=( $! )
        fi
    fi
done

# wait for all pids
for pid in ${pids[*]}; do
    wait "$pid"
done

# Push to registry (direct docker push is not possible because the image is not stored. However, it should be in the cache.
# Since nothing changed, the build step should finish fast.
for dir in ts-*; do
    if [[ -d $dir ]]; then
        if [[ -n $(ls "$dir" | grep -i Dockerfile) ]]; then
            echo "Pushing ${dir}"
            docker build --push -t "$1"/"${dir}":"${tag}" "$dir"\
                        --label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" \
                        --label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket"
        fi
    fi
done

