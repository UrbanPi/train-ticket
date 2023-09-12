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
argAll=0

function quick_end {
  echo "quick end"
  tsMysqlName="ts-db"

  update_tt_dp_cm $nacosRelease $rabbitmqRelease
  gen_secret_for_services $tsUser $tsPassword $tsDB "${tsMysqlName}-mysql-leader"
}


function reset_all {
  update_tt_sw_dp_cm $nacosRelease $rabbitmqRelease
  gen_secret_for_services $tsUser $tsPassword $tsDB

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

#    deploy_infrastructures $namespace

    if [ $argDB == 1 ]; then
#      deploy_tt_mysql_each_service  $namespace
      gen_secret_for_services $tsUser $tsPassword $tsDB

    else
#      deploy_tt_mysql_all_in_one $namespace
      gen_secret_for_services $tsUser $tsPassword $tsDB "${tsMysqlName}-mysql-leader"
    fi

#    deploy_tt_secret  $namespace
#    deploy_tt_svc $namespace

    if [ $argTracing == 1 ]; then
#      deploy_tt_dp_sw  $namespace
#      deploy_tracing  $namespace
      update_tt_sw_dp_cm $nacosRelease $rabbitmqRelease
    else
#      deploy_tt_dp $namespace
      update_tt_dp_cm $nacosRelease $rabbitmqRelease

    fi

#    if [ $argMonitoring == 1 ]; then
#      deploy_monitoring
#    fi
}
#prepare-reset
function parse_args {
    echo "Parse ResetArgs"
    for arg in $args
    do
      echo $arg
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
      "--with-tracing")
        argTracing=1
        ;;
      esac
    done
}

echo "args num: $#"
if [ $# == 2 ]; then
  argNone=0
  parse_args $args
fi
prepare-reset