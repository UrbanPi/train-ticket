#!/bin/bash

TT_ROOT=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

source "$TT_ROOT/utils.sh"
source "$TT_ROOT/gen-mysql-secret.sh"

namespace="$1"
args="$2"

argNone=1
argDB=0
argMonitoring=0
argTracing=0
argOTEL=0
argAll=0

function delete_tt_micro_services {
    kubectl delete -f deployment/kubernetes-manifests/quickstart-k8s/yamls -n "$namespace"
}

function quick_end {
  echo "quick end"
  update_tt_dp_cm $nacosRelease $rabbitmqRelease
  delete_tt_micro_services

}

function reset_all {
  update_tt_otel_dp_cm $nacosRelease $rabbitmqRelease
  kubectl delete -f deployment/kubernetes-manifests/otel -n "$namespace"
  kubectl delete -f deployment/kubernetes-manifests/jaeger -n "$namespace"
  kubectl delete -f deployment/kubernetes-manifests/prometheus -n "$namespace"
  delete_tt_micro_services
}

function reset {
    if [ $argNone == 1 ]; then
      quick_end
      exit $?
    fi

    if [ $argAll == 1 ]; then
      reset_all

      exit $?
    fi


    if [ $argOTEL == 1 ]; then
      update_tt_otel_dp_cm $nacosRelease $rabbitmqRelease
      kubectl delete -f deployment/kubernetes-manifests/otel -n "$namespace"
      kubectl delete -f deployment/kubernetes-manifests/jaeger -n "$namespace"
    else
      update_tt_dp_cm $nacosRelease $rabbitmqRelease
    fi

    if [ $argMonitoring == 1 ]; then
      kubectl delete -f deployment/kubernetes-manifests/prometheus

    fi
    delete_tt_micro_services
    helm uninstall $rabbitmqRelease -n "$namespace"

}
#reset
function parse_args {
    echo "Parse ResetArgs"
    for arg in $args
    do
      echo "$arg"
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
if [ $# == 2 ] && [ "$args" != "" ]; then
  argNone=0
  parse_args "$args"
fi
reset
