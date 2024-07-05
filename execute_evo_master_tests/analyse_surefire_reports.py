import itertools
import re
import os
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
idx = pd.IndexSlice


def read_reports(report_source: str):
    dfs = []
    for f in glob(report_source, recursive=True):
        tmp = pd.read_xml(f, encoding="utf8",
                          iterparse={"testcase": ["name", "time", "type", "message"]})
        filename = f.split("\\")[-1]
        tmp["version"] = filename.split(".")[0][5::]
        tmp["service"] = filename.split(".")[1]
        tmp["test_class"] = filename.split(".")[2]
        tmp["SUT"] = f.split("\\")[-2].split("-")[4]

        dfs.append(tmp)
    df = pd.concat(dfs)
    df["message"] = df["message"].str.replace("\n"," ")
    df.loc[df["type"].isna(), ["type", "message"]] = None  # columns "type" and "message" have the same NaN rows
    df.reset_index(drop=True, inplace=True)
    return df


def read_reports_from_local_execution(report_source: str):
    dfs = []
    for f in glob(report_source, recursive=True):
        tmp = pd.read_xml(f, encoding="utf8",
                          iterparse={"testcase": ["name", "time", "type", "message"]})
        filename = f.split("\\")[-1]
        tmp["version"] = filename.split(".")[0][5::]
        tmp["service"] = filename.split(".")[1]
        tmp["test_class"] = filename.split(".")[2]
        # tmp["SUT"] = f.split("\\")[-2].split("-")[4]

        dfs.append(tmp)
    df = pd.concat(dfs)
    df["message"] = df["message"].str.replace("\n"," ")
    df.loc[df["type"].isna(), ["type", "message"]] = None  # columns "type" and "message" have the same NaN rows
    df.reset_index(drop=True, inplace=True)
    return df


def find_duplicate_tests(base: str, version: str):
    test_name_pat = re.compile(r"public void ([^(]+)")

    duplicates = []
    for service in os.listdir(f"{base}/{version}"):
        data = []
        for test in os.listdir(f"{base}/{version}/{service}/tests"):
            f = Path(f"{base}/{version}/{service}/tests/{test}")
            content = f.read_text(encoding="utf8")
            # Create a list, where each element is a test
            tests = [c[0:c.rfind("}")].strip() for c in content[content.find("@Test(timeout = 60000)"):content.rfind("}")].split("@Test(timeout = 60000)") if len(c) > 0]
            test_names = [test_name_pat.match(c)[1] for c in tests]
            data.append([f"{version}/{service}/{test}", test_names, tests])

        df_s = pd.DataFrame(data, columns=["file", "test_names", "tests"])
        for r1, r2 in itertools.combinations(df_s.to_records(), 2):
            t1 = list(zip(r1["tests"], r1["test_names"], [r1["file"]] * len(r1["test_names"])))
            t2 = list(zip(r2["tests"], r2["test_names"], [r2["file"]] * len(r2["test_names"])))
            for t_1, tn_1, tf_1 in t1:
                for t_2, tn_2, tf_2 in t2:
                    # If the tests without the test name (that's why find(\n)) are equal, we found a duplicate
                    if t_1[t_1.find("\n")::] == t_2[t_2.find("\n")::]:
                        print(f"{tn_1} == {tn_2} in {tf_1} and {tf_2}")
                        duplicates.append([tn_1, tn_2, tf_1, tf_2])
    return duplicates


def get_duplicate_test_list():
    dupes = []
    base = "./execute_evo_master/test_suites/"
    for branch in os.listdir(base):
        if branch.startswith("ts-error-"):
            dupes.extend(find_duplicate_tests(base=base, version=branch))

    return pd.DataFrame(dupes, columns=["test_name1", "test_name2", "test_file1", "test_file2"])


evaluations = []
evaluations_std = []


def group(df: pd.DataFrame):
    df["original_message"] = df["message"].copy()
    df["fault_type"] = None
    deserialization_error = re.compile(r"Can not deserialize value of type ((?:[a-zA-Z0-9]+\.)*[a-zA-Z0-9]+\.?)+ from")
    df["deserialization"] = df.join(df["message"].str.extract(r"Can not deserialize value of type ((?:[a-zA-Z0-9]+\.)*[a-zA-Z0-9]+\.?)+ from").dropna()).loc[:, 0]
    df["construction"] = df.join(df["message"].str.extract(r"Can not construct instance of ((?:[a-zA-Z0-9_]+\.)*[a-zA-Z0-9]+\.?)+:").dropna()).loc[:, 0]
    df["status_code"] = df.join(df["message"].str.extract(r"Expected status code (<\d+> but was <\d+>)").dropna()).loc[:, 0]
    df["list_size"] = df.join(df["message"].str.extract(r"JSON path ((?:'[a-zA-Z0-9]+'\.)?size\(\)) doesn't match").dropna()).loc[:, 0]
    df["boolean_status"] = df.join(df["message"].str.extract(r"(JSON path 'status') doesn't match").dropna(subset=[0])).loc[:, 0]
    df.loc[df["message"].str.contains(r"JSON path 'status' doesn't match", na=False).values, "boolean_status"] = "bool JSON status"
    df["boolean_status"] = df.join(df["message"].str.extract(r"(Response body) doesn't match expectation. Expected: a string containing \"(?:false)|(?:true)\"").dropna(subset=[0])).loc[:, 0]
    df.loc[df["message"].str.contains(r"Response body doesn't match expectation. Expected: a string containing \"(?:false)|(?:true)\"", na=False).values, "boolean_status"] = "bool response body"
    df.loc[df["message"].str.contains(r"JSON path 'exception' doesn't match.", na=False).values, "json_exception"] = "json wrong exception"
    df.loc[df["message"].str.contains(r"Response body doesn't match expectation. Expected: a string containing \"(?:[a-zA-Z0-9\._]+ )+(?:[a-zA-Z0-9\._]+)*\"", na=False).values, "response_message"] = "response body wrong message"
    df.loc[df["message"].str.contains(r"Expected: a string containing \"shanghai\"\s*Actual: 上海", na=False, regex=True).values, "default_values"] = "Different default values in constructor"
    df.loc[df["message"].str.contains(r"Expected: a string containing \"上海\"\s*Actual: shanghai", na=False, regex=True).values, "default_values"] = "Different default values in constructor"
    df.loc[df["message"].str.contains(r"Expected: a string containing \"太原\"\s*Actual: taiyuan", na=False, regex=True).values, "default_values"] = "Different default values in constructor"

    df["melted"] = [[v for v in row[0].tolist() + [row[1][0], None] if isinstance(v, str) or v is None][0] for row in zip(df.loc[:,"deserialization"::].values, df.loc[:,"message":].values)]
    return df


def analyse_tests_from_ts_error_cleaned_on_different_branches(df_grouped:pd.DataFrame):
    from_ts_error_cleaned = df_grouped.loc[df_grouped["version"] == "ts_error_cleaned_reset", :]
    counts = from_ts_error_cleaned.groupby(["SUT"], dropna=False).count().loc[:, ["name", "type"]]
    counts.columns = ["#Total", "#Fails"]
    print(counts)
    fails = (from_ts_error_cleaned.loc[~from_ts_error_cleaned["type"].isna(), :]
             .sort_values(by=["SUT", "service", "name"], axis=0))
    for gr, df in fails.groupby(["SUT"]):
        print(f"Group: {gr}")
        for r in df.to_dict(orient="records"):
            print(f"""
            Service:{r['service']}
            Class: {r['test_class']}
            Test: {r['name']}
            Short message: {r['melted']}
            Message: {r['message']}
            """)
        print("")




def cluster():
    df_dup = get_duplicate_test_list()
    df_dup[["ver", "serv", "test_cl"]] = pd.DataFrame(data=df_dup["test_file2"].str.replace("-", "_").str.split("/").tolist(), index=df_dup.index)
    df_dup = df_dup.loc[:, ["test_name2", "ver", "serv", "test_cl"]]
    df_dup["test_cl"] = df_dup["test_cl"].str.strip(".java")
    df_dup["ver"] = df_dup["ver"].str.lower()

    df = read_reports("./execute_evo_master_tests/surefire-reports/**/TEST-**.xml")
    to_drop = pd.merge(df.reset_index(), df_dup, how="inner", left_on=["name", "version", "service", "test_class"], right_on=["test_name2", "ver", "serv", "test_cl"])
    not_found = pd.concat([df_dup, to_drop.loc[:, ["test_name2", "ver", "serv", "test_cl"]]]).drop_duplicates(keep=False)
    if len(not_found) != 0:
        print("""--- WARNING: Sanity check failed --- 
        Some duplicates could not be found in the imported tests. You really should investigate this.""")
    df_dedup = df.drop(index=to_drop.set_index("index").index)

    df_grouped = group(df_dedup)


    # df = read_reports_from_local_execution("./ExecutableTestSuites/target/surefire-reports/TEST-**.xml")
    grp = df_grouped.groupby("melted", dropna=False).count()
    grp2 = df_grouped.groupby(["SUT", "melted"], dropna=False).count()

    grp3 = df_grouped.groupby(["SUT", "version", "melted"], dropna=False).count().sort_values("name", ascending=False).sort_index(level=[0,1])
    grp3 = df_grouped.groupby(["SUT", "version", "melted"], dropna=False).count().reset_index().sort_values(["SUT", "version", "name"], ascending=False)


if __name__ == '__main__':
    read_reports()
