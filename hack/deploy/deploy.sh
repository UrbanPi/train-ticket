#!/bin/bash

TT_ROOT=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

source "$TT_ROOT/utils.sh"



namespace="$1"
args="$2"

argNone=1
argMonitoring=0
argOTEL=0
argAll=0

function quick_start {
  echo "quick start"
  deploy_infrastructures  $namespace
  deploy_tt_svc $namespace
  deploy_tt_dp_otel  $namespace
}

function deploy_all {
  deploy_infrastructures  $namespace
  deploy_tt_svc $namespace
  deploy_monitoring
  deploy_otel_collector $namespace
  deploy_jaeger $namespace
  deploy_tt_dp_otel $namespace
}


function deploy {
    if [ $argNone == 1 ]; then
      quick_start
      exit $?
    fi

    if [ $argAll == 1 ]; then
      deploy_all
      exit $?
    fi

    deploy_infrastructures $namespace

    deploy_tt_svc $namespace
    deploy_tt_dp_otel $namespace

    if [ $argOTEL == 1 ]; then
      deploy_otel_collector $namespace
      deploy_jaeger $namespace
    fi

    if [ $argMonitoring == 1 ]; then
      deploy_monitoring
    fi
}

#deploy
function parse_args {
    echo "Parse DeployArgs"
    for arg in $args
    do
      echo $arg
      case $arg in
      "--all")
        argAll=1
        ;;
      "--with-monitoring")
        argMonitoring=1
        ;;
      "--with-otel")
        argOTEL=1
        ;;
      esac
    done
}

echo "args num: $#"
if [ $# == 2 ]; then
  argNone=0
  parse_args $args
fi
deploy