import argparse
import socket
import sys
import urllib.request
import json
from concurrent.futures import ThreadPoolExecutor
from http.client import RemoteDisconnected
from json import JSONDecodeError
from urllib.error import URLError

available_versions = ["master", "ts-error-F1", "ts-error-F2", "ts-error-F3", "ts-error-F4", "ts-error-F5",
                      "ts-error-F6", "ts-error-F7",
                      "ts-error-F8", "ts-error-F9", "ts-error-F10", "ts-error-F11", "ts-error-F12", "ts-error-F13",
                      "ts-error-F14", "ts-error-F15",
                      "ts-error-F16", "ts-error-F17", "ts-error-F18", "ts-error-F19", "ts-error-F20", "ts-error-F21",
                      "ts-error-F22"]

version_groups = {"master_grp": ["master"],
                  "error_grp": ["ts-error-F1", "ts-error-F3", "ts-error-F4", "ts-error-F6", "ts-error-F8",
                                "ts-error-F9", "ts-error-F10", "ts-error-F11",
                                "ts-error-F12", "ts-error-F13", "ts-error-F14", "ts-error-F15", "ts-error-F16",
                                "ts-error-F17",
                                "ts-error-F18", "ts-error-F19", "ts-error-F20", "ts-error-F21", "ts-error-F22"],
                  "error_grp_2": ["ts-error-F2", "ts-error-F5"],
                  "error_grp_3": ["ts-error-F7"],
                  "error_grp_4": [
                      "ts-error-F13"]}  # is the same as the "error_grp" but has an additional Java service without swagger

services = [{"name": "ts-admin-basic-info-service", "port": 30030,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-admin-order-service", "port": 30031,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-admin-route-service", "port": 30032,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-admin-travel-service", "port": 30033,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-admin-user-service", "port": 30034,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-assurance-service", "port": 30035,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-auth-service", "port": 30036,
             "versions": ["master_grp"]},
            # {"name": "ts-avatar-service", "port": 30037,  # No swagger definition, written in Python
            #  "versions": ["master_grp"]},
            {"name": "ts-basic-service", "port": 30038,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-cancel-service", "port": 30039,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-config-service", "port": 30040,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-consign-price-service", "port": 30041,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-consign-service", "port": 30042,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-contacts-service", "port": 30043,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            # {"name": "ts-delivery-service", "port": 30044,  # No REST endpoints, Java
            #  "versions": ["master_grp"]},
            {"name": "ts-execute-service", "port": 30045,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-food-service", "port": 30046,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-inside-payment-service", "port": 30047,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            # {"name": "ts-news-service", "port": 30048,  # No swagger definition (service is basically an oneliner in written in Go
            #  "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-notification-service", "port": 30049,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-order-other-service", "port": 30050,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-order-service", "port": 30051,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-payment-service", "port": 30052,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-preserve-other-service", "port": 30053,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-preserve-service", "port": 30054,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-price-service", "port": 30055,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-rebook-service", "port": 30056,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-route-plan-service", "port": 30057,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-route-service", "port": 30058,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-seat-service", "port": 30059,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-security-service", "port": 30060,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-station-food-service", "port": 30061,
             "versions": ["master_grp"]},
            {"name": "ts-station-service", "port": 30062,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            # {"name": "ts-ticket-office-service", "port": 30063,  # No swagger definition, written in JS
            #  "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-train-food-service", "port": 30064,
             "versions": ["master_grp"]},
            {"name": "ts-train-service", "port": 30065,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-travel-plan-service", "port": 30066,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-travel-service", "port": 30067,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-travel2-service", "port": 30068,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-user-service", "port": 30069,
             "versions": ["master_grp"]},
            {"name": "ts-verification-code-service", "port": 30070,
             "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
            # {"name": "ts-voucher-service", "port": 30071,  # No swagger definition, written in Python
            #  "versions": ["master_grp"]},
            {"name": "ts-food-map-service", "port": 30073,
             "versions": ["error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-ticketinfo-service", "port": 30074,
             "versions": ["error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-login-service", "port": 30075,
             "versions": ["error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-sso-service", "port": 30076,
             "versions": ["error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-register-service", "port": 30077,
             "versions": ["error_grp", "error_grp_2", "error_grp_3"]},
            {"name": "ts-click-twice-service", "port": 30078,
             "versions": ["error_grp_2"]},
            # {"name": "ts-rest-external-service", "port": 30079,  # No swagger definition, written in JS
            #  "versions": ["error_grp_3"]},
            # {"name": "ts-launcher", "port": 30080, # Java,no swagger definition, executes a workflow which has a chance to trigger the fault.
            #  "versions": ["error_grp_4"]},
            {"name": "ts-food-delivery-service", "port": 30081,
             "versions": ["master_grp"]},
            {"name": "ts-wait-order-service", "port": 30082,
             "versions": ["master_grp"]},
            # {"name": "ts-gateway-service", "port": 30467,  # No swagger definition available (Java)
            #  "versions": ["master_grp"]},

            ]
unwanted_tags = [
    "loggers-mvc-endpoint",
    "endpoint-mvc-adapter",
    "metrics-mvc-endpoint",
    "environment-mvc-endpoint",
    "heapdump-mvc-endpoint",
    "audit-events-mvc-endpoint",
    "health-mvc-endpoint",
    "basic-error-controller",
    "log-file-mvc-endpoint",
    "operation-handler",
    "web-mvc-links-handler",
]

unwanted_paths = [
    "/actuator",
    "/actuator/health",
    "/actuator/health/**",
    "/actuator/info",
    "/auditevents",
    "/auditevents.json",
    "/autoconfig",
    "/autoconfig.json",
    "/beans",
    "/beans.json",
    "/configprops",
    "/configprops.json",
    "/dump",
    "/dump.json",
    "/env",
    "/env.json",
    "/env/{name}",
    "/error",
    "/features",
    "/features.json",
    "/health",
    "/health.json",
    "/heapdump",
    "/heapdump.json",
    "/info",
    "/info.json",
    "/loggers",
    "/loggers.json",
    "/loggers/{name}",
    "/logfile",
    "/logfile.json",
    "/mappings",
    "/mappings.json",
    "/metrics",
    "/metrics.json",
    "/metrics/{name}",
    "/trace",
    "/trace.json",
]


def retrieve_and_save(service: dict):
    url = "http://localhost:{}/v2/api-docs".format(service.get("port"))
    # print("Getting definition of {} from url: {}".format(service.get("name"), url))
    try:
        definition: dict = json.loads(urllib.request.urlopen(url, timeout=30).read().decode("utf8"))
        definition["tags"] = list(
            filter(lambda tag: not any(tag.get("name") == not_wanted for not_wanted in unwanted_tags),
                   definition.get("tags")))
        definition["paths"] = dict(filter(lambda item: not any(item[0] == not_wanted for not_wanted in unwanted_paths),
                                          definition.get("paths").items()))
        with open(service.get("name") + ".json", "w", encoding="utf8") as f:
            f.write(json.dumps(definition))
    except KeyError:
        return "{}: Invalid json from url: {}".format(service.get("name"), url)
    except AttributeError:
        return "{}: Invalid json from url: {}".format(service.get("name"), url)
    except JSONDecodeError:
        return "{}: Invalid json from url: {}".format(service.get("name"), url)
    except RemoteDisconnected as error:
        return '{}: URL Error: Data of not retrieved because {}\nURL: {}'.format(service.get("name"), error, url)
    except URLError as error:
        if isinstance(error.reason, socket.timeout):
            return '{}: Timeout Error for {} '.format(service.get("name"), url)
        else:
            return '{}: URL Error: Data of not retrieved because {}\nURL: {}'.format(service.get("name"), error, url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get swagger definitions of a specific TrainTicket version')
    parser.add_argument("--version", metavar='-v', type=str, choices=available_versions,
                        help="Version of the deployed TrainTicket system")

    args = parser.parse_args()
    version_argument = args.version
    if not version_argument:
        print("No version selected defaulting to version \"ts-error-F22\"", file=sys.stderr)
        version_argument = "ts-error-F22"
    else:
        print("Selected version: {}".format(version_argument))
    selected_version_group = list(filter(lambda item: version_argument in item[1], version_groups.items()))[0][0]
    selected_services = list(filter(lambda service: selected_version_group in service.get("versions"), services))

    print("Services with swagger in this version:\n"
          "{}".format("\n".join([service.get("name") for service in selected_services])))

    with ThreadPoolExecutor() as executor:
        results = executor.map(retrieve_and_save, selected_services)

        for res in results:
            if res:
                print("{}\n".format(res), file=sys.stderr)
    input("Finished, press enter to end the program")
