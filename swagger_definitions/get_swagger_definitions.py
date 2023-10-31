import json
import socket
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from json import JSONDecodeError
from urllib.error import URLError

services = [{"name": "ts-admin-basic-info-service", "port": 30030},
            {"name": "ts-admin-order-service", "port": 30031},
            {"name": "ts-admin-route-service", "port": 30032},
            {"name": "ts-admin-travel-service", "port": 30033},
            {"name": "ts-admin-user-service", "port": 30034},
            {"name": "ts-assurance-service", "port": 30035},
            {"name": "ts-auth-service", "port": 30036},
            {"name": "ts-avatar-service", "port": 30037},
            {"name": "ts-basic-service", "port": 30038},
            {"name": "ts-cancel-service", "port": 30039},
            {"name": "ts-config-service", "port": 30040},
            {"name": "ts-consign-price-service", "port": 30041},
            {"name": "ts-consign-service", "port": 30042},
            {"name": "ts-contacts-service", "port": 30043},
            {"name": "ts-delivery-service", "port": 30044},
            {"name": "ts-execute-service", "port": 30045},
            {"name": "ts-food-service", "port": 30046},
            {"name": "ts-gateway-service", "port": 30047},
            {"name": "ts-inside-payment-service", "port": 30048},
            {"name": "ts-news-service", "port": 30049},
            {"name": "ts-notification-service", "port": 30050},
            {"name": "ts-order-other-service", "port": 30051},
            {"name": "ts-order-service", "port": 30052},
            {"name": "ts-payment-service", "port": 30053},
            {"name": "ts-preserve-other-service", "port": 30054},
            {"name": "ts-preserve-service", "port": 30055},
            {"name": "ts-price-service", "port": 30056},
            {"name": "ts-rebook-service", "port": 30057},
            {"name": "ts-route-plan-service", "port": 30058},
            {"name": "ts-route-service", "port": 30059},
            {"name": "ts-seat-service", "port": 30060},
            {"name": "ts-security-service", "port": 30061},
            {"name": "ts-station-food-service", "port": 30062},
            {"name": "ts-station-service", "port": 30063},
            {"name": "ts-ticket-office-service", "port": 30064},
            {"name": "ts-train-food-service", "port": 30065},
            {"name": "ts-train-service", "port": 30066},
            {"name": "ts-travel-plan-service", "port": 30067},
            {"name": "ts-travel-service", "port": 30068},
            {"name": "ts-travel2-service", "port": 30069},
            {"name": "ts-user-service", "port": 30070},
            {"name": "ts-verification-code-service", "port": 30071},
            {"name": "ts-voucher-service", "port": 30072},
            {"name": "ts-food-map-service", "port": 30073},
            {"name": "ts-ticketinfo-service", "port": 30074},
            {"name": "ts-login-service", "port": 30075},
            {"name": "ts-sso-service", "port": 30076},
            {"name": "ts-register-service", "port": 30077},

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

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def retrieve_and_save(service: dict):
    url = "https://localhost:{}/v2/api-docs".format(service.get("port"))
    print("Getting definition of {} from url: {}".format(service.get("name"), url))
    try:
        definition: dict = json.loads(urllib.request.urlopen(url, context=ctx, timeout=30).read().decode("utf8"))
        definition["tags"] = list(filter(lambda tag: not any(tag.get("name") == not_wanted for not_wanted in unwanted_tags), definition.get("tags")))
        definition["paths"] = dict(filter(lambda item: not any(item[0] == not_wanted for not_wanted in unwanted_paths), definition.get("paths").items()))
        with open(service.get("name") + ".json", "w", encoding="utf8") as f:
            f.write(json.dumps(definition))
    except JSONDecodeError | KeyError:
        print("Invalid json for {} from url: {}".format(service.get("name"), url))
    except URLError as error:
        if isinstance(error.reason, socket.timeout):
            print('Timeout Error for {} : This is a request with SSL which is only used in special scenarios of TrainTicket. Maybe you started the wrong file? '.format(url), flush=True)
        else:
            print('URL Error: Data of not retrieved because {}\nURL: {}'.format(error, url))


if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        res = executor.map(retrieve_and_save, services)

    executor.shutdown()
    print("\n".join([str(r) for r in res]))

    input("Finished, press enter to close this window")
