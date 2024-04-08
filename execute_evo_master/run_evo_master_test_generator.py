import argparse
import ast
from collections import defaultdict
from datetime import datetime, timedelta
import http.client
import os
import subprocess
import sys
import time
from urllib import request, parse
import json
from concurrent.futures import ThreadPoolExecutor
import logging
import shutil

from service_availability import available_versions, filter_services

START_TIME: datetime = datetime.now()  # datetime(2024,3,20,8,43,0)
START_TIME_FORMATTED: str = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
STOP_TIME: datetime = datetime.now()

plain_format = logging.Formatter("%(message)s")
regular_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setFormatter(regular_format)

fileHandler = logging.FileHandler(f"./{START_TIME_FORMATTED}-run_evo_master_test_generator.log")
fileHandler.setFormatter(regular_format)


logger = logging.getLogger()  # Logger
logger.addHandler(logger_handler)
logger.addHandler(fileHandler)
logger.setLevel(logging.DEBUG)
# logger.basicConfig(stream=sys.stdout,  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     encoding='utf-8', level=logger.DEBUG)



def call_microservice_controller_of(services: list[dict], with_method):
    with ThreadPoolExecutor() as executor:
        results = executor.map(with_method, services)
        for res in results:
            if res:
                if res.startswith("Error"):
                    logger.error("{}".format(res))
                else:
                    logger.info("{}".format(res))
    executor.shutdown(wait=True)


def start_service(service: dict):
    url = f"http://localhost:{service.get('port')}/api/control/startNormal"
    try:
        response: str = request.urlopen(url, timeout=30).read().decode("utf8")
        if not response.startswith("Starting main Spring application"):
            return f"Could not start service {service.get('name')}: {response}"
    except Exception as e:
        return f"Error when starting service {service.get('name')}:\n{e}"


def start_evo_master_driver(service: dict):
    logger.info(f"Stopping service {service.get('name')} and waiting 30 sec for the process to finish")
    error = stop_service(service)
    if error:
        logger.error(error)
    else:
        time.sleep(30)

    url = f"http://localhost:{service.get('port')}/api/control/startWithEvoDriver"
    try:
        response: str = request.urlopen(url, timeout=30).read().decode("utf8")
        time.sleep(30)
        if not response.startswith("Starting jar"):
            logger.error(f"Error when starting service {service.get('name')} with evomaster driver:\n{response}")
    except Exception as e:
        logger.error(f"Error when starting service {service.get('name')} with evomaster driver:\n{e}")


def stop_service(service: dict):
    url = f"http://localhost:{service.get('port')}/api/control/stop"
    try:
        response: str = request.urlopen(url, timeout=30).read().decode("utf8")
        if not response.startswith("Stopping jar"):
            return f"Could not stop service {service.get('name')}:\n{response}"
    except Exception as e:
        return f"Error when stopping service {service.get('name')}:\n{e}"


def check_service_availability(services_to_check: list[dict]):
    with ThreadPoolExecutor() as executor:
        wait_count = 0
        while len(services_to_check) != 0:
            results = executor.map(check_readiness, services_to_check)
            services_to_check = []
            for res in results:
                if res:
                    services_to_check.append(res[0])
                    # if res[1]:
                    #     logger.error(f"{res[0].get('name')}\n{res[1]}")
            if len(services_to_check) != 0:
                # logger_handler.terminator = "\x1b[1K\r"  # Clear line, carriage return
                logger_handler.terminator = ""
                fileHandler.terminator = ""
                logger.info(
                    f"\x1b[1K\rWaiting on {len(services_to_check)} services to get ready: {','.join([s.get('name') for s in services_to_check])}")
                logger_handler.terminator = "\n"
                fileHandler.terminator = "\n"
                time.sleep(10)
                if wait_count > 18:
                    logger.info("")
                    logger.info(f"Waited for around 4 minutes on services {','.join([s.get('name') for s in services_to_check])}. Restarting them now.")
                    logger.info("Stopping services and waiting for 30 sec...")
                    call_microservice_controller_of(services_to_check, stop_service)
                    time.sleep(30)
                    logger.info("Starting services and waiting for 2 min")
                    call_microservice_controller_of(services_to_check, start_service)
                    time.sleep(60 * 2)
                    wait_count = 0
            wait_count += 1

    executor.shutdown(wait=True)
    logger.info("")


def check_readiness(service: dict):
    url = f"http://localhost:{service.get('port') - 600}/v2/api-docs"
    try:
        res: http.client.HTTPResponse = request.urlopen(url, timeout=30)
        if res.status != 200:
            return service, None
    except Exception as e:
        return service, e


def start_evo_master(service: dict, arguments: str):
    url = f"http://localhost:{service.get('port')}/api/control/startGenerating"
    try:
        req = request.Request(url, method="POST", data=f'{{"args": "{arguments}"}}'.encode("utf8"))
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Accept', 'application/json')
        response: str = request.urlopen(req, timeout=30).read().decode("utf8")
        logger.info(response)
        if not response.startswith("Starting EvoMaster to generate"):
            logger.error(f"Error when starting generating tests with {service.get('name')}:\n{response}")
    except Exception as e:
        logger.error(f"Error when starting generating tests with {service.get('name')}:\n{e}")


def show_evo_master_log(service: dict):
    logger.info("EvoMaster logs:")
    url = f"http://localhost:{service.get('port')}/api/control/evoMasterLogs"
    lines = 0
    logger_handler.setFormatter(plain_format)
    fileHandler.setFormatter(plain_format)
    while True:
        try:
            resp: http.client.HTTPResponse = request.urlopen(url, timeout=30)
            log: str = resp.read().decode("utf8")
            if resp.status == 200:
                log_lines = log.strip().split("\n")
                logger.info("\n".join(log_lines[lines::]))
                break
            elif resp.status == 206:
                log_lines = log.strip().split("\n")
                if lines != len(log_lines):
                    logger.info("\n".join(log_lines[lines::]))
                lines = len(log_lines)
            else:
                logger.error(f"Getting logs of EvoMaster failed with HTTP status {resp.status}")
        except Exception as e:
            logger_handler.setFormatter(regular_format)
            fileHandler.setFormatter(regular_format)
            logger.error(f"Error when getting logs for EvoMaster from service {service.get('name')}:\n{e}")
            logger_handler.setFormatter(plain_format)
            fileHandler.setFormatter(plain_format)
        time.sleep(2)
    logger_handler.setFormatter(regular_format)
    fileHandler.setFormatter(regular_format)


def retrieve_and_save_pod_logs(destination: str, service_pod_names: dict[str:str]):
    logger.info("Retrieving pod logs")
    service_names, pod_names = zip(*service_pod_names.items())
    with ThreadPoolExecutor() as executor:
        results = executor.map(copy_from_kubernetes_pod_to,
                               pod_names, [":app/app.logs"] * len(pod_names),
                               [destination + "/" + m + ".log" for m in service_names], service_names)
        for res in results:
            if res:
                logger.error("{}".format(res))
    executor.shutdown(wait=True)


def copy_from_kubernetes_pod_to(pod_name: str, pod_src: str, destination: str, service_name: str):
    service_and_file = pod_name + pod_src
    sub = subprocess.run(["kubectl", "-c", service_name, "cp", service_and_file, destination])
    if sub.returncode != 0:
        return "No log for {} ".format(pod_name)


def retrieve_and_save_otel_traces(destination: str):
    logger.info("Retrieving otel traces")
    out = subprocess.check_output(["kubectl", "get", "pods", "-l", "app=otel-collector", "-o", "name"], shell=False)
    pod_name = list(filter(lambda pod: pod.startswith("otel-collector"),
                           out.decode("utf8").replace("pod/", "").split("\n")))[0]
    copy_from_kubernetes_pod_to(pod_name, ":/otel/traces.txt",
                                destination + "/otel.txt",
                                "otel-collector")  # slash / in front of otel is needed here. Was not working without


def retrieve_and_save_prometheus_metrics(destination: str):
    def get_metrix_names():
        req = request.Request(method="GET",
                              url=f"http://localhost:30003/api/v1/label/__name__/values",
                              headers={"Accept": "application/json"})
        try:
            response = request.urlopen(req, timeout=120).read().decode("utf8")
        except Exception as e:
            return f"Could not get metric names from prometheus because: {e}"
        return json.loads(response)["data"]

    def get_and_save(prometheus_query: str, destination: str, query_name: str):
        cur_start: datetime = START_TIME
        responses = []
        while cur_start < STOP_TIME:
            start: datetime = cur_start
            end: datetime = cur_start + timedelta(minutes=10)
            cur_start = end
            request_params = parse.urlencode({'query': prometheus_query,
                                              "start": start.timestamp(),
                                              "end": end.timestamp(),
                                              "step": 14,
                                              "_": int(round(datetime.now().timestamp() * 1_000_000))})
            req = request.Request(method="GET",
                                  url=f"http://localhost:30003/api/v1/query_range?{request_params}",
                                  headers={"Accept": "application/json"})
            try:
                response = request.urlopen(req, timeout=600).read().decode("utf8")
                responses.append(json.loads(response))

            except Exception as e:
                return prometheus_query, query_name, e
        try:
            metrics_p_id = [{str(m["metric"]): m for m in resp["data"]["result"]} for resp in responses]
        except KeyError as e:
            return prometheus_query, query_name, e
        accumulated = defaultdict(list)
        metadata = {}
        for part in metrics_p_id:
            for pod in part.items():
                accumulated[pod[0]].extend(pod[1]["values"])
                if "__name__" not in pod[1]["metric"]:
                    pod[1]["metric"]["__name__"] = query_name
                metadata[pod[0]] = pod[1]["metric"]
        merged = [{"metric": metadata[k], "values": accumulated[k]} for k in metadata.keys()]
        complete = responses[0]
        complete["data"]["result"] = merged
        with open(destination, 'w', encoding="utf8") as file:
            file.write(json.dumps(complete))

    def handle_result(result: tuple | None, failed_metrics: list[tuple[str, str]]):
        if result:
            logger.error(f"Could not get prometheus metrik for {result[1]} because: {result[2]}")
            failed_metrics.append((result[0], result[1]))

    logger.info("Retrieving prometheus metrics")
    metrix_names = get_metrix_names()
    failed_retrievals = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(get_and_save, metrix_names,
                               [f"{destination}/{m}.json" for m in metrix_names], metrix_names)
        for res in results:
            handle_result(res, failed_retrievals)
    executor.shutdown(wait=True)
    err = get_and_save(
        "sum(rate(container_cpu_usage_seconds_total{namespace='default'}[5m])) by (pod, instance, container)",
        destination + "/container_cpu_usage_seconds_total_by_pod_instance_container.json",
        "container_cpu_usage_seconds_total_by_pod_instance_container")
    handle_result(err, failed_retrievals)

    # Retry failed jaeger retrievals
    retry_count = 0
    limit = 5
    while retry_count < limit and len(failed_retrievals) > 0:
        logger.info(f"({retry_count}/{limit}) Retrying getting metrics for: {failed_retrievals} after waiting one minute...")
        time.sleep(60)
        new_results = []
        for tup in failed_retrievals:
            err = get_and_save(tup[0], destination + "/" + tup[1] + ".json", tup[1])
            handle_result(err, new_results)
        failed_retrievals = new_results
        retry_count += 1


def retrieve_and_save_jaeger_traces(destination: str, service_pod_names: dict[str:str], service_pod_under_test_name: str):
    def get_and_save(service_name: str, destination: str):
        cur_start: datetime = START_TIME
        sequence_num = 0
        responses = []
        while cur_start < STOP_TIME:
            start: datetime = cur_start
            end: datetime = cur_start + timedelta(minutes=5)
            cur_start = end
            request_params = parse.urlencode({'service': service_name,
                                              'limit': -1,
                                              'start': int(round(start.timestamp() * 1_000_000)),
                                              'end': int(round(end.timestamp() * 1_000_000)),
                                              'lookback': "5m"})
            req = request.Request(method="GET",
                                  url=f"http://localhost:32688/api/traces?{request_params}",
                                  headers={"Accept": "application/json"})
            try:
                response = request.urlopen(req, timeout=600).read().decode("utf8")
                responses.append(json.loads(response))
            except Exception as e:
                return service_name, e
            # with open(destination+str(sequence_num), 'w', encoding="utf8") as file:
            #     file.write(response)
            sequence_num += 1
        complete = responses[0]
        for r in responses[1::]:
            complete["data"].extend(r["data"])
        with open(destination, 'w', encoding="utf8") as file:
            file.write(json.dumps(complete))

    def handle_result(result: tuple | None, failed_services: list[str]):
        if result:
            logger.error(f"Could not get jaeger traces for {result[0]} because: {result[1]}")
            failed_services.append(result[0])

    logger.info("Retrieving jaeger traces")
    service_names, _ = zip(*service_pod_names.items())
    service_names = [sn + "-1.0" if "ts-user-service" == sn or "ts-auth-service" == sn else sn for sn in service_names]
    failed_retrievals = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(get_and_save, service_names, [destination + "/" + n + ".json" for n in service_names if n != service_pod_under_test_name])
        for res in results:
            handle_result(res, failed_retrievals)
    executor.shutdown(wait=True)
    err = get_and_save(service_pod_under_test_name, destination + "/" + service_pod_under_test_name + ".json")
    handle_result(err, failed_retrievals)

    # Retry failed jaeger retrievals
    retry_count = 0
    limit = 5
    while retry_count < limit and len(failed_retrievals) > 0:
        logger.info(f"({retry_count}/{limit}) Retrying getting traces for: {failed_retrievals} after waiting one minute...")
        time.sleep(60)
        new_results = []
        for service_name in failed_retrievals:
            err = get_and_save(service_name, destination + "/" + service_name + ".json")
            handle_result(err, new_results)
        failed_retrievals = new_results
        retry_count += 1


def retrieve_and_save_evo_tests(destination: str, pod_name: str, service_name: str):
    logger.info("Retrieving EvoMaster tests")
    copy_from_kubernetes_pod_to(pod_name, ":app/src/em", destination + "/", service_name)


def retrieve_and_save_evomaster_logs(destination: str, pod_name: str, service_name: str):
    logger.info("Retrieving EvoMaster execution log")
    copy_from_kubernetes_pod_to(pod_name, ":app/evomaster-log", destination + "/evomaster.log", service_name)


def cleanup(service_pod_names: dict[str:str], service_name: str = None):
    clean_service_logs(service_pod_names)
    if service_name:
        clean_generated_tests(service_name=service_name, pod_name=service_pod_names.get(service_name))
    reset_data_collection_infra()


def reset_data_collection_infra():
    logger.info("Deleting data collection deployments")
    subprocess.run(["kubectl", "delete", "-f", "./data_collection_infra/jaeger"], shell=False)
    subprocess.run(["kubectl", "delete", "-f", "./data_collection_infra/prometheus"], shell=False)
    subprocess.run(["kubectl", "delete", "-f", "./data_collection_infra/otel"], shell=False)

    logger.info("Deploying data collection...")
    subprocess.run(["kubectl", "apply", "-f", "./data_collection_infra/jaeger"], shell=False)
    subprocess.run(["kubectl", "apply", "-f", "./data_collection_infra/prometheus"], shell=False)
    subprocess.run(["kubectl", "apply", "-f", "./data_collection_infra/otel"], shell=False)


def clean_service_logs(service_pod_names: dict[str:str]):
    def clean(service_name: str, pod_name: str):
        sub = subprocess.run(
            ["kubectl", "exec", "-c", service_name, pod_name, "--", "cp", "/dev/null", "/app/app.logs"])
        if sub.returncode != 0:
            return "Could not clean logs for {} ".format(pod_name)

    service_names, pod_names = zip(*service_pod_names.items())
    with ThreadPoolExecutor() as executor:
        results = executor.map(clean, service_names, pod_names)
    for res in results:
        if res:
            logger.error("{}\n".format(res))


def clean_generated_tests(service_name: str, pod_name: str):
    sub = subprocess.run(["kubectl", "exec", "-c", service_name, pod_name, "--", "rm", "-r", "/app/src/"])
    if sub.returncode != 0:
        logger.error("Could not clean tests for {} ".format(pod_name))


def retrieve_and_save_all_data(service_pod_names, service_under_test_name):
    """Get monitoring, tracing data, logs and generated tests and archive them"""
    base_destination = "./results/tmp"
    prometheus = f"{base_destination}/monitoring-prometheus"
    otel = f"{base_destination}/otel"
    logs = f"{base_destination}/logs"
    jaeger = f"{base_destination}/traces-jaeger"
    tests = f"{base_destination}/tests"
    evomaster_logs = f"{base_destination}/evo_logs"

    # Clean up previous data
    if os.path.exists(base_destination):
        shutil.rmtree(base_destination)

    # Re-create directories
    os.makedirs(prometheus, exist_ok=True)
    os.makedirs(logs, exist_ok=True)
    os.makedirs(otel, exist_ok=True)
    os.makedirs(jaeger, exist_ok=True)
    os.makedirs(evomaster_logs, exist_ok=True)

    retrieve_and_save_prometheus_metrics(prometheus)
    retrieve_and_save_otel_traces(otel)
    retrieve_and_save_pod_logs(logs, service_pod_names=service_pod_names)
    retrieve_and_save_jaeger_traces(jaeger, service_pod_names=service_pod_names,
                                    service_pod_under_test_name=service_under_test_name)
    retrieve_and_save_evomaster_logs(evomaster_logs, pod_name=service_pod_names.get(service_under_test_name),
                                     service_name=service_under_test_name)

    # Get generated tests
    retrieve_and_save_evo_tests(tests, pod_name=service_pod_names.get(service_under_test_name),
                                service_name=service_under_test_name)
    shutil.make_archive(f"{START_TIME_FORMATTED}-{version_arg}-generated-with-{service_under_test_name}", "gztar", root_dir=base_destination)


def start_generating(version_argument: str, service: str, evo_master_args: str):
    if not version_argument:
        logger.error("No version selected defaulting to version \"master\"")
        version_argument = "master"
    else:
        logger.info("Selected version: {}".format(version_argument))

    selected_services, service_to_test = filter_services(version_argument, service)
    all_services: list[dict] = selected_services + [service_to_test]
    service_pod_names = {
        s.get("name"): subprocess.check_output(["kubectl", "get", "pods", "-l", "app=" + s.get("name"), "-o", "name"],
                                               shell=False).decode("utf8").lstrip("pod/")[:-1] for s in all_services}

    if not service_to_test:
        logger.error(f"Service {service} not available in version {version_argument}."
                     f"\n Available services: {', '.join([s.get('name') for s in selected_services])}")
        exit(-1)

    # Pre run cleaning
    cleanup(service_pod_names)

    start_evo_master_driver(service_to_test)

    call_microservice_controller_of(services=selected_services, with_method=start_service)

    if version_argument == "master":
        logger.info("Waiting 3 min before checking availability")
        time.sleep(60 * 3)
    else:
        logger.info("Waiting 2 min before checking availability")
        time.sleep(60 * 2)

    check_service_availability(selected_services)

    logger.info("All services started!")
    logger.info(f"Start generating tests with {service}")
    start_evo_master(service_to_test, evo_master_args)

    show_evo_master_log(service_to_test)

    # Stop all services
    call_microservice_controller_of(services=all_services, with_method=stop_service)

    global STOP_TIME
    STOP_TIME = datetime.now()

    retrieve_and_save_all_data(service_pod_names, service)

    # Post run cleaning
    cleanup(service_pod_names, service)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Start generating tests with EvoMaster for a specific TrainTicket version')
    parser.add_argument("--version", metavar='-v', type=str, choices=available_versions,
                        help="Version of the deployed TrainTicket system")
    parser.add_argument("--service", metavar="-s", type=str,
                        help="Service for which to generate tests with EvoMaster or 'all'")
    parser.add_argument("--evoArgs", metavar="-ea", type=str, help="Arguments passed to EvoMaster")
    parser.add_argument("--skip_until_including", metavar="-skip", type=str,
                        help="Skip testing all services including this one. See service_availability for ordering.",
                        required=False)
    parser.add_argument("--skip_count", metavar="-skip_count", type=int,
                        help="Skip the number of services.",
                        required=False)
    parser.add_argument("--num_services_to_test", metavar="-num_to_tes", type=int,
                        help="Test the x next services. x > |services| has no effect.",
                        required=False)

    args = parser.parse_args()
    service_arg = args.service
    version_arg = args.version
    skip_stop = args.skip_until_including
    skip_count = args.skip_count if args.skip_count else 0
    num_services_to_test = args.num_services_to_test if args.num_services_to_test else 999

    count_skipped = 0
    count_tested = 0
    if service_arg == "all":
        logger.info(f"Start running EvoMaster for all services with OpenAPI specification in version {version_arg}")
        selected_services, _ = filter_services(version_argument=version_arg)
        skip = skip_stop is not None
        for serv in selected_services:
            if skip or count_skipped < skip_count or count_tested > num_services_to_test:
                logger.info(f"Skipping {serv.get('name')}")
                skip = skip_stop is not None and serv.get("name") != skip_stop
                count_skipped += 1
                continue
            logger.info("\n-------------------------------------------------------------\n"
                        "-------------------------------------------------------------\n"
                        "-------------------------------------------------------------\n"
                        "-------------------------------------------------------------\n"
                        "-------------------------------------------------------------\n"
                        )
            start_generating(version_argument=version_arg, service=serv.get("name"), evo_master_args=args.evoArgs)
            count_tested += 1
            logger.info("Finished!! Waiting 10 sec...")
            time.sleep(10 * 1)

    else:
        start_generating(version_argument=version_arg, service=args.service, evo_master_args=args.evoArgs)
