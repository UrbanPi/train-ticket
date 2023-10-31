#!/bin/bash

rabbitmqCharts=deployment/kubernetes-manifests/quickstart-k8s/charts/rabbitmq

# rabbitmq parameters
rabbitmqRelease="rabbitmq"


function deploy_infrastructures {
  namespace=$1
  echo "Start deployment Step <1/3>------------------------------------"
  echo "Start to deploy rabbitmq."
  helm install $rabbitmqRelease $rabbitmqCharts -n $namespace
  echo "Waiting for rabbitmq to be ready ......"
  kubectl rollout status deployment/$rabbitmqRelease -n $namespace
  echo "Deploying mongo DBs ..."
  kubectl apply -f deployment/kubernetes-manifests/quickstart-k8s/yamls/mongo-dbs.yml
  echo "End deployment Step <1/3>--------------------------------------"

}

function deploy_monitoring {
  echo "Start deploy prometheus and grafana"
  kubectl apply -f deployment/kubernetes-manifests/prometheus
}

function deploy_tracing {
  echo "Start deploy skywalking"
  namespace=$1
  kubectl apply -f deployment/kubernetes-manifests/skywalking -n $namespace
}

function deploy_otel_collector {
  echo "Start deploy otel_collector"
  namespace=$1
  kubectl apply -f deployment/kubernetes-manifests/otel -n $namespace
}

function deploy_jaeger {
  echo "Start deploy jaeger"
  namespace=$1
  kubectl apply -f deployment/kubernetes-manifests/jaeger -n $namespace
}


function deploy_tt_svc {
  namespace=$1
  kubectl apply -f deployment/kubernetes-manifests/quickstart-k8s/yamls/svc.yaml -n $namespace > /dev/null
}


function deploy_tt_dp_otel {
  namespace=$1
  echo "Start to deploy train-ticket deployments with otel agent."
#  update_tt_otel_dp_cm $nacosRelease $rabbitmqRelease
  kubectl apply -f deployment/kubernetes-manifests/quickstart-k8s/yamls/otel_deploy.yaml -n $namespace > /dev/null
  echo "End deployment Step <3/3>----------------------------------------------------------------------"
}