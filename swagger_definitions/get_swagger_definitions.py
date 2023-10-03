import urllib.request
from concurrent.futures import ThreadPoolExecutor

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
            {"name": "ts-voucher-service", "port": 30072}]


def retrieve_and_save(service: dict):
    url = "http://localhost:{}/v2/api-docs".format(service.get("port"))
    print("Getting definition of {} from url: {}".format(service.get("name"), url))
    definition: str = urllib.request.urlopen(url).read().decode("utf8")
    if len(definition) > 0:
        with open(service.get("name") + ".json", "w", encoding="utf8") as f:
            f.write(definition)


with ThreadPoolExecutor() as executor:
    executor.map(retrieve_and_save, services)
