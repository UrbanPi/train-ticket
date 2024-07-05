available_versions = ["master", "ts-error-F1", "ts-error-F2", "ts-error-F3", "ts-error-F4", "ts-error-F5",
                      "ts-error-F6", "ts-error-F7","ts-error-F8", "ts-error-F9", "ts-error-F10", "ts-error-F11",
                      "ts-error-F12", "ts-error-F13", "ts-error-F14", "ts-error-F15", "ts-error-F16", "ts-error-F17",
                      "ts-error-F18", "ts-error-F19", "ts-error-F20", "ts-error-F21", "ts-error-F22",
                      "ts-error-cleaned"]

version_groups = {"master_grp": ["master"],
                  "error_grp": ["ts-error-F1", "ts-error-F3", "ts-error-F4", "ts-error-F6", "ts-error-F8",
                                "ts-error-F9", "ts-error-F10", "ts-error-F11",
                                "ts-error-F12", "ts-error-F13", "ts-error-F14", "ts-error-F15", "ts-error-F16",
                                "ts-error-F17", "ts-error-F18", "ts-error-F19", "ts-error-F20", "ts-error-F21",
                                "ts-error-F22", "ts-error-cleaned"],
                  "error_grp_2": ["ts-error-F2", "ts-error-F5"],
                  "error_grp_3": ["ts-error-F7"],
                  "error_grp_4": [
                      "ts-error-F13"]}  # is the same as the "error_grp" but has an additional Java service without swagger

services = {
    "ts-admin-basic-info-service": {"port": 30630, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-admin-order-service": {"port": 30631, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-admin-route-service": {"port": 30632, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-admin-travel-service": {"port": 30633, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-admin-user-service": {"port": 30634, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-assurance-service": {"port": 30635, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-auth-service": {"port": 30636, "versions": ["master_grp"]},
    "ts-basic-service": {"port": 30638, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-cancel-service": {"port": 30639, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-click-twice-service": {"port": 30678, "versions": ["error_grp_2"]},
    "ts-config-service": {"port": 30640, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-consign-price-service": {"port": 30641, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-consign-service": {"port": 30642, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-contacts-service": {"port": 30643, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-execute-service": {"port": 30645, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-food-delivery-service": {"port": 30681, "versions": ["master_grp"]},
    "ts-food-map-service": {"port": 30673, "versions": ["error_grp", "error_grp_2", "error_grp_3"]},
    "ts-food-service": {"port": 30646, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-inside-payment-service": {"port": 30647, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-login-service": {"port": 30675, "versions": ["error_grp", "error_grp_2", "error_grp_3"]},
    "ts-notification-service": {"port": 30649, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-order-other-service": {"port": 30650, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-order-service": {"port": 30651, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-payment-service": {"port": 30652, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-preserve-other-service": {"port": 30653, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-preserve-service": {"port": 30654, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-price-service": {"port": 30655, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-rebook-service": {"port": 30656, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-register-service": {"port": 30677, "versions": ["error_grp", "error_grp_2", "error_grp_3"]},
    "ts-route-plan-service": {"port": 30657, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-route-service": {"port": 30658, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-seat-service": {"port": 30659, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-security-service": {"port": 30660, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-sso-service": {"port": 30676, "versions": ["error_grp", "error_grp_2", "error_grp_3"]},
    "ts-station-food-service": {"port": 30661, "versions": ["master_grp"]},
    "ts-station-service": {"port": 30662, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-ticketinfo-service": {"port": 30674, "versions": ["error_grp", "error_grp_2", "error_grp_3"]},
    "ts-train-food-service": {"port": 30664, "versions": ["master_grp"]},
    "ts-train-service": {"port": 30665, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-travel-plan-service": {"port": 30666, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-travel-service": {"port": 30667, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-travel2-service": {"port": 30668, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-user-service": {"port": 30669, "versions": ["master_grp"]},
    "ts-verification-code-service": {"port": 30670, "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-wait-order-service": {"port": 30682, "versions": ["master_grp"]}
}
unavailable_services = {
    "ts-avatar-service": {"port": 30037,  # No swagger definition, written in Python
                          "versions": ["master_grp"]},
    "ts-delivery-service": {"port": 30044,  # No REST endpoints, Java
                            "versions": ["master_grp"]},
    "ts-news-service": {"port": 30048,  # No swagger definition (service is basically an oneliner in written in Go
                        "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-ticket-office-service": {"port": 30063,  # No swagger definition, written in JS
                                 "versions": ["master_grp", "error_grp", "error_grp_2", "error_grp_3"]},
    "ts-voucher-service": {"port": 30071,  # No swagger definition, written in Python
                           "versions": ["master_grp"]},
    "ts-rest-external-service": {"port": 30079,  # No swagger definition, written in JS
                                 "versions": ["error_grp_3"]},
    "ts-launcher": {"port": 30080, # Java,no swagger definition, executes a workflow which has a chance to trigger the fault.
                    "versions": ["error_grp_4"]},
    "ts-gateway-service": {"port": 30467,  # No swagger definition available (Java)
                           "versions": ["master_grp"]}
}


def filter_services(version_argument: str, selected_service_name: str = None) -> (list[dict], dict | None):
    """
    :param version_argument: Fault branch name e.g. ts-error-F1, ts-error-cleaned, etc.
    :param selected_service_name: (Optional) Name of the service for which to generate tests with evomaster
    :return: tuple containing a list with info on services in the selected version and info on the service under test.
    The list does NOT contain the service under test. If no selected_service_name is specified all in this version
    available services are contained in the list.
    """
    selected_version_group = list(filter(lambda item: version_argument in item[1], version_groups.items()))[0][0]
    serv_names = list(filter(lambda key: selected_version_group in services[key].get("versions"), services.keys()))
    selected_services = []
    service_to_test = None
    for name in serv_names:
        service_dict = services[name]
        service_dict["name"] = name
        if selected_service_name == name:
            service_to_test = service_dict
        else:
            selected_services.append(service_dict)

    return selected_services, service_to_test
