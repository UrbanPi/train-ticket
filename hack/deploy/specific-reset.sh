#!/bin/bash

TT_ROOT=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

source "$TT_ROOT/utils.sh"
source "$TT_ROOT/gen-mysql-secret.sh"

namespace="$1"
args="$2"

argNone=1
argDB=0
argMonitoring=0
argOTEL=0
argAll=0

function delete_tt_micro_services {
    kubectl delete -f deployment/kubernetes-manifests/quickstart-k8s/yamls -n "$namespace"
    helm ls -n "$namespace" | grep ^ts- | awk '{print $1}' | xargs helm uninstall -n "$namespace"
}

function delete_pvc {
    kubectl delete pvc data-tsdb-mysql-0 -n "$namespace"
    kubectl delete pvc data-tsdb-mysql-1 -n "$namespace"
    kubectl delete pvc data-tsdb-mysql-2 -n "$namespace"
    kubectl delete pvc data-nacosdb-mysql-0 -n "$namespace"
    kubectl delete pvc data-nacosdb-mysql-1 -n "$namespace"
    kubectl delete pvc data-nacosdb-mysql-2 -n "$namespace"
}

function quick_end {
  echo "quick end"
  tsMysqlName="ts-db"

  update_tt_dp_cm $nacosRelease $rabbitmqRelease
  gen_secret_for_services $tsUser $tsPassword $tsDB "${tsMysqlName}-mysql-leader"
  delete_tt_micro_services
}

function reset_all {
  update_tt_sw_dp_cm $nacosRelease $rabbitmqRelease
  gen_secret_for_services $tsUser $tsPassword $tsDB
  delete_tt_micro_services
  kubectl delete -f deployment/kubernetes-manifests/skywalking -n "$namespace"
  kubectl delete -f deployment/kubernetes-manifests/prometheus
}

function reset {
    if [ $argNone == 1 ]; then
      quick_end
      delete_pvc
      exit $?
    fi

    if [ $argAll == 1 ]; then
      reset_all
      delete_pvc
      exit $?
    fi

    if [ $argDB == 1 ]; then
      gen_secret_for_services $tsUser $tsPassword $tsDB
    else
      gen_secret_for_services $tsUser $tsPassword $tsDB "${tsMysqlName}-mysql-leader"
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
    helm uninstall $nacosRelease -n "$namespace"
    helm uninstall $nacosDBRelease -n "$namespace"
    delete_pvc
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
      "--independent-db")
        argDB=1
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
