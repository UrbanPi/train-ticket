import sys
import time
import requests
import itertools
from datetime import datetime

from service_availability import available_versions, filter_containers

token = 'YOUR_GITHUB_PAT'
organisation = 'ConTest'
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github+json'
}
package_type = "container"  # One of: npm, maven, rubygems, docker, nuget, container

docker_command_template = 'docker build --push -t containers.github.scch.at/contest/trainticket/SERVICE:VERSION ./DIRECTORY --label "org.opencontainers.image.source=https://github.scch.at/ConTest/TrainTicket" --label "org.opencontainers.image.url=https://github.scch.at/ConTest/TrainTicket"'
def get_packages():
    package_url = f"https://github.scch.at/api/v3/orgs/{organisation}/packages?package_type={package_type}"
    res = requests.get(package_url, headers=headers, params={"per_page": 100})
    if res.status_code != 200:
        print("Error getting packages for organization '{}'.\nServer response: {}".format(organisation, res.json()), file=sys.stderr)
        return []

    packages = [p["name"] for p in res.json()]
    return packages


def get_package_versions(package_name, version) -> (int, str | list):
    package_versions_url = f"https://github.scch.at/api/v3/orgs/{organisation}/packages/{package_type}/trainticket%2F{package_name}/versions"
    res = requests.get(package_versions_url, headers=headers, params={"per_page": 100})
    if res.status_code != 200:
        directory = "ts-error-F"+version.split("-")[-1][1::]+"/"
        command = docker_command_template.replace("SERVICE", package_name).replace("VERSION", version).replace("DIRECTORY", directory + package_name)
        print("Error getting package info for {} :\n{}\nBuild command:\n{}".format(package_name, res.json(),command), file=sys.stderr)
        time.sleep(0.05)
        return -1, command
    return 0, res.json()


def find_missing_packages(version: str, has_to_be_updated_after: datetime):
    target_packages = {serv["name"] for serv in filter_containers(version_argument=version)[0]}
    target_packages = {"ts-click-twice" if "click-twice" in v else v for v in target_packages}
    commands = []
    for package in target_packages:
        package_name = requests.utils.quote(package, safe='')
        response_code, package_versions = get_package_versions(package_name, version)
        if response_code == -1:
            commands.append(package_versions)
            continue
        filtered = list(filter(lambda vers: version in vers["metadata"]["container"]["tags"], package_versions))
        if len(filtered) == 1:
            filtered = filtered[0]
            updated_at = datetime.fromisoformat(filtered["updated_at"])
            if updated_at < has_to_be_updated_after:  # If it was updated before the target date
                directory = version + "/"
                commands.append(docker_command_template.replace("SERVICE", package_name).replace("VERSION", version).replace("DIRECTORY", directory + package_name))

        elif len(filtered) == 0:
            directory = version+"/"
            commands.append(docker_command_template.replace("SERVICE", package_name).replace("VERSION", version).replace("DIRECTORY", directory + package_name))
        else:
            print(f"Multiple tags for version: {version} of package {package_name}. Check if this is intended: {filtered}")

    if len(commands) != 0:
        print("\n".join(commands))
        print(";".join(commands))
    return commands


if __name__ == '__main__':
    total = []
    newer_than = datetime.fromisoformat("2024-05-22T08:30:59Z")
    # for ver in available_versions:
    #     missing = find_missing_packages(ver, newer_than)
    #     total.extend(missing)
    #     print(f"Missing packages in {ver}: {len(missing)}")

    missing = find_missing_packages("ts-error-F8", newer_than)
    total.extend(missing)

    print(f"Total missing packages: {len(total)}")
    print(";".join(total))

