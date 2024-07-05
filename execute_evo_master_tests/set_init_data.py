import argparse
import subprocess


def remove_old_dumps(service_name: str, pod_name: str):
    sub = subprocess.run(["kubectl", "exec", "-c", service_name, pod_name, "--", "rm", "-r", "/app/dumps/"])


def copy_new_dumps(service_name: str, pod_name: str, dumps_to_copy: str):
    sub = subprocess.run(["kubectl", "exec", "-c", service_name, pod_name, "--", "mkdir", "/app/dumps/"])
    service_and_file = pod_name + ":/app/dumps/new_dumps.tar.gz"
    sub = subprocess.run(["kubectl", "-c", service_name, "cp", dumps_to_copy, service_and_file])


def extract_dumps(service_name: str, pod_name: str):
    sub = subprocess.run(
        ["kubectl", "exec", "-c", service_name, pod_name, "--", "tar", "-xf", "/app/dumps/new_dumps.tar.gz", "-C", "/app/dumps"])
    sub = subprocess.run(["kubectl", "exec", "-c", service_name, pod_name, "--", "rm", "/app/dumps/new_dumps.tar.gz"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Update mongoDB dumps in a given service with dumps from a given version')
    parser.add_argument("--version", metavar='-v', type=str,  # choices=available_versions,
                        help="Version of the dumps, which should be used")
    parser.add_argument("--service", metavar="-s", type=str,
                        help="Service for which to remove old dumps")
    args = parser.parse_args()
    version = args.version  # "ts-admin-order-service"
    service = args.service  # "ts-error-cleaned"

    # 1. Get services and pod names
    pod_name = subprocess.check_output(["kubectl", "get", "pods", "-l", "app=" + service, "-o", "name"],
                                       shell=False).decode("utf8").replace("pod/", "")[:-1]
    # 2. Remove old dumps
    remove_old_dumps(service, pod_name)

    # 3. Copy new dumps compressed
    copy_new_dumps(service, pod_name, f"./dumps/dumps-enhanced-{version}.tar.gz")

    # 4. Extract
    extract_dumps(service, pod_name)

