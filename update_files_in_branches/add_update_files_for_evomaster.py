import os
from glob import glob
from pathlib import Path
import re


def add_embedded_evo_master_controller(ssl: bool = False):
    embedded_evo_master_controller_templ = Path("./../update_files_in_branches/files_to_update/EmbeddedEvoMasterController.java").read_text(
        encoding="utf8")
    package_mapping = {}
    service_pat = re.compile(r".*/(ts-[a-z0-9-]*(service)?)/.*")
    for f in glob("./../TrainTicket/ts-*/src/main/java/**/*Application.java", recursive=True):
        p = Path(f)
        file = p.read_text()
        package_info = file[0:file.find("\n")]
        # print(f)
        package = package_info[8:-1]
        service = service_pat.search(p.as_posix())[1]
        package_mapping[service] = package
        prefix_and_import = f"{package_info}\n"
        embedded_evo_master_controller = prefix_and_import + (embedded_evo_master_controller_templ
                                                              .replace("MAIN_APPLICATION", p.name[0:-5])
                                                              .replace("PACKAGE_PATH", package + "."))
        if ssl:
            embedded_evo_master_controller = embedded_evo_master_controller.replace("http://", "https://")
        with open(p.parent.joinpath("EmbeddedEvoMasterController.java"), "w", encoding="utf8") as contr:
            contr.write(embedded_evo_master_controller)
    return package_mapping

def add_spring_fox_config():
    spring_fox_tmpl = Path("./../update_files_in_branches/files_to_update/SpringFoxConfig.java").read_text(
        encoding="utf8")
    for f in glob("./../TrainTicket/ts-*/src/main/java/**/conf*/HttpAspect*.java", recursive=True):
        p = Path(f)
        file = p.read_text(encoding="utf8")
        package_info = file[0:file.find("\n")]
        package = package_info[8:-1]
        prefix_and_import = f"{package_info}\n"
        spring_fox = prefix_and_import + spring_fox_tmpl
        with open(p.parent.joinpath("SpringFoxConfig.java"), "w", encoding="utf8") as contr:
            contr.write(spring_fox)


def remove_spring_fox_config():
    # spring_fox_tmpl = Path("./files_to_update/SpringFoxConfig.java").read_text(
    #     encoding="utf8")
    for f in glob("./../TrainTicket/ts-*/src/main/java/**/config/SpringFoxConfig.java", recursive=True):
        p = Path(f)
        os.remove(p)


def add_table_names_to_entities():
    entity = re.compile(r"^@Entity", re.MULTILINE)
    table = re.compile(r"^@Table.*$", re.MULTILINE)
    table_with_args = re.compile(r"^@Table\(", re.MULTILINE)
    table_with_name = re.compile(r"^@Table\(.*name\s*=\s*[\"\'].*$", re.MULTILINE)
    idx_definition = re.compile(r"@Index\([a-zA-Z=\"\',_ ]*\)")
    unique_definition = re.compile(r"@UniqueConstraint\([a-zA-Z=\"\',_ ]*\)")

    def format_table_name(file_name: str):
        file_name = file_name[0].lower() + file_name[1::]
        class_name = re.compile(r"[A-Z]+")
        return class_name.sub("_\g<0>", file_name).lower()

    for f in glob("./../TrainTicket/ts-*/src/main/java/**/entity/*.java", recursive=True):
        p = Path(f)
        name = format_table_name(p.name[0:-5])
        file = p.read_text(encoding="utf8")
        if entity.search(file):
            table_def_match = table.search(file)
            if table_def_match:
                if table_with_args.search(file):
                    table_def = table_def_match.group()
                    cleaned = idx_definition.sub("", table_def)
                    cleaned = unique_definition.sub("", cleaned)
                    print(f"File: {p}\nMatch: {table_def}\nCleaned: {cleaned}\n")
                    table_name = table_with_name.search(cleaned)
                    if table_name:
                        print(f"File with table name: {p}\nMatch: {table_name.group()}\n")
                    else:
                        # insert name = "TABLE_NAME"
                        file = table_with_args.sub(fr'\g<0>name = "{name}", ', file)
                else:
                    # insert (name = "TABLE_NAME")
                    file = table.sub(fr'(\g<0> name = "{name}")', file)
            else:
                # insert @Table(name = "TABLE_NAME")
                file = entity.sub(fr'\g<0>\n@Table(name = "{name}")', file)
        p.write_text(file, encoding="utf8")


# pom_dependency = """
#         <dependency>
#             <groupId>org.evomaster</groupId>
#             <artifactId>evomaster-client-java-controller</artifactId>
#             <version>2.0.0</version>
#         </dependency>
# """
# def add_evomaster_dependency_to_pom():
#     for f in glob("./../TrainTicket/ts-*/pom.xml", recursive=True):
#         p = Path(f)
#         file = p.read_text(encoding="utf8")
#         last_dependency = file.rfind("</dependency>")
#         file = (f"{file[0:last_dependency + 13]}"
#                 f"{pom_dependency}"
#                 f"{file[last_dependency + 13::]}")
#         p.write_text(file, encoding="utf8")


if __name__ == '__main__':
    # add_embedded_evo_master_controller()
    # remove_spring_fox_config()
    add_spring_fox_config()
    # add_evomaster_dependency_to_pom()
