import re
import os
import shutil
import tarfile
import json
from collections import defaultdict


def save_evo_stats():
    usable_endpoints = re.compile(r"\* There are (\d+) usable RESTful API endpoints defined in the schema configuration")
    successful_endpoints = re.compile(r"\* Successfully executed \(HTTP code 2xx\) (\d+) endpoints out of")
    final_num_tests = re.compile(r"\* Going to save (\d+) tests to")
    bytecode_line_coverage = re.compile(r"\* Bytecode line coverage: (\d+% \(\d+ out of \d+ in \d+ units/classes\))")
    duration = re.compile(r"\* Passed time \(seconds\): (\d*)")

    def get_stat(patter: re.Pattern, logs):
        res = patter.search(logs)
        if res:
            return res[1]
        else:
            return -1

    header = ["date", "total_duration_(minutes)", "target_service", "usable_endpoints", "successful_endpoints(http 200)", "saved_tests", "bytecode_line_cov", "target_service_api_calls"]
    data = [header]

    result_archive = re.compile(r"(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})-generated-with-([a-zA-Z0-9-]+).tar.gz")
    jaeger_traces_in = []
    for f in os.listdir("./"):
        match = result_archive.search(f)
        if match:
            with tarfile.open(f) as tf:
                evo_log = list(filter(lambda x: "evomaster.log" in x.name, tf.getmembers()))
                if len(evo_log) == 0:
                    continue
                tf.extractall("./", evo_log)

                jaeger_service = list(filter(lambda x: match[2] + ".json" in x.name, tf.getmembers()))
                if len(jaeger_service) == 0:
                    continue
                tf.extractall("./", jaeger_service)
                jaeger_traces = list(filter(lambda x: x.name.startswith("ts-") and x.name.endswith(".json"), tf.getmembers()))
                jaeger_traces_in.append(f"{len(jaeger_traces)} ;; {match[0]}")

            try:
                os.makedirs("./evo_logs/", exist_ok=True)
                os.makedirs("./traces-jaeger/", exist_ok=True)
                with open("./evo_logs/evomaster.log", "r", encoding="utf8") as rf:
                    logs = rf.read()
                with open("./traces-jaeger/" + match[2] + ".json", "r", encoding="utf8") as rf:
                    traces = json.loads(rf.read())["data"]
                os.remove("./traces-jaeger/" + match[2] + ".json")
            except FileNotFoundError:
                continue
            print(f)
            seconds = get_stat(duration, logs)
            if isinstance(seconds, str):
                minutes = str(round(int(seconds) / 60.0))
            else:
                minutes = "-1"
            data.append(
                [
                    match[1],
                    minutes,
                    match[2],
                    str(get_stat(usable_endpoints, logs)),
                    str(get_stat(successful_endpoints, logs)),
                    str(get_stat(final_num_tests, logs)),
                    str(get_stat(bytecode_line_coverage, logs)),
                    str(count_production_spans(traces))
                ]
            )
    print("\n".join(jaeger_traces_in))
    data_csv = "\n".join(",".join(entry) for entry in data)
    header_separator = "|---|---|---|---|---|---|---|---|"
    data_md = [f"| {' | '.join(entry)} |" for entry in data]
    data_md = "\n".join([data_md[0]] + [header_separator] + data_md[1::])
    with open("evostats.csv", "w", encoding="utf8") as f:
        f.write(data_csv)

    with open("evostats.md", "w", encoding="utf8") as f:
        f.write(data_md)

    shutil.rmtree("./evo_logs/", ignore_errors=True)
    shutil.rmtree("./jaeger/", ignore_errors=True)


def count_production_spans(data):
    production_api_call_count = 0
    api_endpoint_counts = defaultdict(int)
    for trace in data:
        start_time_endpoint = {}
        for span in trace["spans"]:
            # When "net.host.name" is not localhost this span is targeted to a different service
            if True not in [t["value"] == "localhost" for t in span["tags"] if "net.host.name" in t.values()]:
                continue
            for tag in span["tags"]:
                if ("http.route" in tag.values()
                        and "/controller/api/" not in tag["value"]
                        and "/v2/api-docs" not in tag["value"] and tag):
                    start_time_endpoint[span['startTime']] = tag['value']
        # The spans in each trace are not ordered by time or appearance.
        # To find out the initial request we order the span by start time and assume that the oldest span / target is
        # the initial request.
        if len(start_time_endpoint) > 0:
            initial_endpoint = sorted(start_time_endpoint.items())[0][1]
            api_endpoint_counts[initial_endpoint] += 1
            production_api_call_count += 1

    print(f"Production apis called: {dict(api_endpoint_counts)}")
    print(f"Total production apis called: {production_api_call_count}")
    return production_api_call_count


if __name__ == '__main__':
    save_evo_stats()
