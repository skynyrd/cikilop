#!/usr/bin/env bash

usage() {
    echo "Usage: $0 [-c <string>] [-m <string>] [-e <string>] [-r <bool>]" 1>&2;
    echo "c: path to config"
    echo "m: path to migration file directory"
    echo "e: environment"
    echo "r: revert"
    exit 1;
}

while getopts ":c:m:e:r:" o; do
    case "${o}" in
        c)
            c=${OPTARG}
            ;;
        m)
            m=${OPTARG}
            ;;
        e)
            e=${OPTARG}
            ;;
        r)
            r=${OPTARG}
            r=$(echo "$r" | awk '{print tolower($0)}')
            if ! [[ "$r" = "false" ]] && ! [[ "$r" = "true" ]]; then
              usage
            fi
            ;;
        *)
            usage
            ;;
    esac
done

shift $((OPTIND-1))

if [ -z "$c" ] || [ -z "$m" ] || [ -z "$e" ]; then
    usage
fi

if [ -z "$r" ] || [[ "$r" = "false" ]]; then
    docker run -e env=$e -v $c:/app/src/config/config.local.json -v $m:/app/src/migrations skynyrd/cikilop
else
    docker run -e env=$e -v $c:/app/src/config/config.local.json -v $m:/app/src/migrations skynyrd/cikilop --revert
fi
