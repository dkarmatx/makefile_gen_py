import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from srcs_expression import proccess_src_list_expressions
from compiler_opts import generate_compilers_options
from compiler_rules import generate_link_rule, generate_compile_rules
import target_collectors


def generate_generic_variables(obj_dir):
    print("# **************************************************************************** #")
    print("# GENERIC_VARIABLES\n")
    print("OBJ_DIR = {obj_dir}\n".format(obj_dir=obj_dir))


def generate_target_variables(t):
    target_path = t.get("path", ".")
    target_type = t.get("type", "prog")
    print("\n".join([
        "# **************************************************************************** #",
        "# {target_upcase} TARGET DESCRIPTION",
        "",
        "{target_upcase}_NAME = {name}",
        "{target_upcase}_PATH = {path}",
        "{target_upcase}_FILE = {out}/{outfile}",
        "{target_upcase}_SRCS = {srcs}",
        "{target_upcase}_OBJS = $(patsubst %, $(OBJ_DIR)/%.o, $({target_upcase}_SRCS))",
        "{target_upcase}_DEPS = $(patsubst %, $(OBJ_DIR)/%.d, $({target_upcase}_SRCS))",
        "{target_upcase}_LIBS = {libs}",
        "{target_upcase}_INCS = {incs}",
        ""
    ]).format(
        target_upcase=t["name"].upper(),
        name=t["name"],
        path=target_path,
        out=t.get("out", target_path),
        outfile=t["name"] if target_type == "prog" else "lib%s.a" % t["name"],
        srcs=" ".join(proccess_src_list_expressions(t["sources"], target_path)),
        libs=target_collectors.collect_target_libs_string(t) if target_type == "prog" else "",
        incs=" ".join(["-I %s" % h for h in t.get("includes", ())])
    ))


def generate_generic_rules(targets):
    libs_files = " ".join(["$(%s_FILE)" % t["name"].upper() for t in targets.values() if t.get("type", "prog") == "lib"])
    progs_files = " ".join(["$(%s_FILE)" % t["name"].upper() for t in targets.values() if t.get("type", "prog") == "prog"])
    print("\n".join([
        "# **************************************************************************** #",
        "# GENERIC RULES",
        "",
        ".PHONY: all re clean fclean",
        ".DEFAULT_GOAL = all",
        "",
        "all: {all_filenames}",
        "",
        "clean:",
        "\t@rm -rf $(OBJ_DIR)",
        "",
        "fclean: clean",
        "\t@rm -rf {all_filenames}",
        "",
        "re: fclean all",
        ""
    ]).format(
        all_filenames=libs_files + " " + progs_files 
    ))


def generate_generic_bottom(targets):
    print("-include %s" % " ".join(["$(%s_DEPS)" % t["name"].upper() for t in targets.values()]))


def generate_makefile(schema, compilers_options=dict()):
    obj_dir = "build"
    if not ("c" in compilers_options):
        compilers_options["c"] = dict()
    generate_generic_variables(obj_dir)
    generate_compilers_options(compilers_options)
    targets = dict()
    target_collectors.collect_target(schema, targets)

    for t in targets.values():
        generate_target_variables(t)

    generate_generic_rules(targets)

    for t in targets.values():
        generate_link_rule(t)
        generate_compile_rules(t, compilers_options)
    
    generate_generic_bottom(targets)
