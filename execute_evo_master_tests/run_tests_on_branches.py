import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import logging
import shutil
from datetime import datetime
from pathlib import Path
from urllib import request

from service_availability import available_versions, filter_services

START_TIME_FORMATTED_ABS: str = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")

plain_format = logging.Formatter("%(message)s")
regular_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setFormatter(regular_format)

fileHandler = logging.FileHandler(f"./{START_TIME_FORMATTED_ABS}-run_evo_master_test_generator.log")
fileHandler.setFormatter(regular_format)

logger = logging.getLogger()  # Logger
logger.addHandler(logger_handler)
logger.addHandler(fileHandler)
logger.setLevel(logging.DEBUG)


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


def run_tests_on_sut_with_sut_data():
    for version in ["ts-error-cleaned"]:
        # Setup
        version_path = Path(f"~/traintickets/{version}").expanduser()
        os.chdir(version_path)
        logger.info(f"Deploying {version}")
        sub = subprocess.run(["./hack/deploy/deploy.sh", "default", "--with-otel --with-monitoring"])
        if sub.returncode != 0:
            logger.error(f"Failed to deploy services for {version}")
        logger.info("Waiting 5 minutes for services to deploy")
        time.sleep(60*5)

        # Start services
        selected_services, service_to_test = filter_services(version)
        call_microservice_controller_of(services=selected_services, with_method=start_service)
        logger.info("Waiting 3.5 minutes for services to start")
        time.sleep(60*3.5)

        # Execute maven tests
        p = Path("~/ExecutableTestSuites/").expanduser().absolute()
        os.chdir(p)
        logger.info("Start executing tests")
        sub = subprocess.run(["mvn", "clean", "verify"])
        if sub.returncode != 0:
            logger.error(f"Failed to executes tests for {version}")

        # Save test reports
        target_dir = f"./test-reports-{version}-{START_TIME_FORMATTED_ABS}"
        os.makedirs(target_dir, exist_ok=True)
        logger.info("Copying test reports to ~/ExecutableTestSuites/")
        shutil.copytree("./target/surefire-reports", target_dir, dirs_exist_ok=True)

        # Teardown
        os.chdir(version_path)
        logger.info(f"Terminating {version}")
        sub = subprocess.run(["./hack/deploy/specific-reset.sh", "default", "--with-otel --with-monitoring"])
        if sub.returncode != 0:
            logger.error(f"Failed to terminate services for {version}")
        logger.info("Waiting 30 seconds for services to terminate")
        time.sleep(30)


if __name__ == '__main__':
    for version in ["ts-error-cleaned"]:
        # Setup
        version_path = Path(f"~/traintickets/{version}").expanduser()
        os.chdir(version_path)
        logger.info("Adapt deployment with correct test data")
        #
        logger.info(f"Deploying {version}")
        sub = subprocess.run(["./hack/deploy/deploy.sh", "default", "--with-otel --with-monitoring"])
        if sub.returncode != 0:
            logger.error(f"Failed to deploy services for {version}")
        logger.info("Waiting 5 minutes for services to deploy")
        time.sleep(60*5)

        # Start services
        selected_services, service_to_test = filter_services(version)
        call_microservice_controller_of(services=selected_services, with_method=start_service)
        logger.info("Waiting 3.5 minutes for services to start")
        time.sleep(60*3.5)

        # Execute maven tests
        p = Path("~/ExecutableTestSuites/").expanduser().absolute()
        os.chdir(p)
        logger.info("Start executing tests")
        sub = subprocess.run(["mvn", "clean", "verify"])
        if sub.returncode != 0:
            logger.error(f"Failed to executes tests for {version}")

        # Save test reports
        target_dir = f"./test-reports-{version}-{START_TIME_FORMATTED_ABS}"
        os.makedirs(target_dir, exist_ok=True)
        logger.info("Copying test reports to ~/ExecutableTestSuites/")
        shutil.copytree("./target/surefire-reports", target_dir, dirs_exist_ok=True)

        # Teardown
        os.chdir(version_path)
        logger.info(f"Terminating {version}")
        sub = subprocess.run(["./hack/deploy/specific-reset.sh", "default", "--with-otel --with-monitoring"])
        if sub.returncode != 0:
            logger.error(f"Failed to terminate services for {version}")
        logger.info("Waiting 30 seconds for services to terminate")
        time.sleep(30)
