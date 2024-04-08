from execute_evo_master.run_evo_master_test_generator import start_service, call_microservice_controller_of, \
    stop_service
from service_availability import filter_services

if __name__ == '__main__':
    selected_services, service_to_test = filter_services("ts-error-F1")
    call_microservice_controller_of(services=selected_services, with_method=start_service)  # To start
    # call_microservice_controller_of(services=selected_services, with_method=stop_service)  # To stop

