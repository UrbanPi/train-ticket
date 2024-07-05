import sys
import time
import requests

"""
This script deletes ALL untagged versions of packages in an organisation with the following workflow:
1. Get all packages with specific type of an organisation
2. Get all versions of a package, only keep untagged versions
3. Delete the untagged versions

The script can be modified to delete other versions of packages too. Beware that the script gets all packages of an 
organisation. Hence, take care that you do not delete packages from other repositories present in the specified 
organisation.

Relevant documentation of used endpoints in order of appearance:
(Future readers: Check if the endpoints are still valid for the currently installed GitHub Enterprise version)

List packages of an organization:
https://docs.github.com/en/enterprise-server@3.10/rest/packages/packages?apiVersion=2022-11-28#list-packages-for-an-organization
List package versions for a package owned by an organization:
https://docs.github.com/en/enterprise-server@3.10/rest/packages/packages?apiVersion=2022-11-28#list-package-versions-for-a-package-owned-by-an-organization
Delete package version for an organization
https://docs.github.com/en/enterprise-server@3.10/rest/packages/packages?apiVersion=2022-11-28#delete-package-version-for-an-organization

To successfully use this script the access token needs at least the "read:packages" and "delete:packages" permission. 
Detailed requirements should be documented in the link "Delete package version for an organization".

"""
# TODO ENTER YOUT TOKEN HERE
token = 'YOUR_TOKEN'
organisation = 'ConTest'
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github+json'
}
package_type = "container"  # One of: npm, maven, rubygems, docker, nuget, container


def get_packages():
    package_url = f"https://github.scch.at/api/v3/orgs/{organisation}/packages?package_type={package_type}"
    res = requests.get(package_url, headers=headers, params={"per_page": 100})
    if res.status_code != 200:
        print("Error getting packages for organization '{}'.\nServer response: {}".format(organisation, res.json()), file=sys.stderr)
        return []

    packages = [p["name"] for p in res.json()]
    return packages


def get_package_versions(package_name):
    package_versions_url = f"https://github.scch.at/api/v3/orgs/{organisation}/packages/{package_type}/{package_name}/versions"
    res = requests.get(package_versions_url, headers=headers, params={"per_page": 100})
    if res.status_code != 200:
        print("Error getting package info for {} :\n{}".format(package_name, res.json()), file=sys.stderr)
        time.sleep(0.1)
        return -1
    return res.json()


def delete_specific_packages():
    for package in get_packages():
        package_name = requests.utils.quote(package, safe='')
        package_versions = get_package_versions(package_name)
        if package_versions == -1:
            continue
        # You can edit the filter function to delete other versions of a package
        # package_versions_to_delete = [(version["id"], version["url"]) for version in filter(lambda v: len(v["metadata"][package_type]["tags"]) == 0, package_versions)]  # Delete all untagged packages
        package_versions_to_delete = [(version["id"], version["url"]) for version in filter(lambda v:  f"ts-error-F5" in v["metadata"][package_type]["tags"], package_versions)]  # Delete packages of error branches
        # for i in range(1,23):

            # package_versions_to_delete = [(version["id"], version["url"]) for version in filter(lambda v:  f"ts-error-F{i}" in v["metadata"][package_type]["tags"], package_versions)]  # Delete packages of error branches
            # package_versions_to_delete = [(version["id"], version["url"]) for version in filter(lambda v: True, package_versions)]

        for version_id, version_url in package_versions_to_delete:
            res = requests.delete(version_url, headers=headers)
            if res.status_code > 300:
                print("Error deleting version {} :\n{}".format(version_url, res.json()), file=sys.stderr)
            else:
                print("Deleted version {} of {}".format(version_id, package_name))
            time.sleep(0.1)

def delete_untagged_packages():
    for package in get_packages():
        package_name = requests.utils.quote(package, safe='')
        package_versions = get_package_versions(package_name)
        if package_versions == -1:
            continue
        # You can edit the filter function to delete other versions of a package
        package_versions_to_delete = [(version["id"], version["url"]) for version in filter(lambda v: len(v["metadata"][package_type]["tags"]) == 0, package_versions)]  # Delete all untagged packages
        for version_id, version_url in package_versions_to_delete:
            res = requests.delete(version_url, headers=headers)
            if res.status_code > 300:
                print("Error deleting version {} :\n{}".format(version_url, res.json()), file=sys.stderr)
            else:
                print("Deleted version {} of {}".format(version_id, package_name))
            time.sleep(0.1)


def delete_all_packages(starting_with: str):
    for package in get_packages():
        if starting_with and not package.replace("trainticket/", "").startswith(starting_with):
            continue
        package_name = requests.utils.quote(package, safe='')
        res = requests.delete(f"https://github.scch.at/api/v3/orgs/{organisation}/packages/{package_type}/{package_name}", headers=headers)
        if res.status_code > 300:
            print("Error deleting package {} :\n{}".format(package_name, res.json()), file=sys.stderr)
        else:
            print("Deleted package {} ".format(package_name, package_name))
        time.sleep(0.1)


if __name__ == '__main__':
    # delete_specific_packages()
    # delete_untagged_packages()
    delete_all_packages(starting_with="ts-")

