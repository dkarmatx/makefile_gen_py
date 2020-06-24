import fnmatch
import os


def is_unix_expression(exp):
    return "*" in exp or "?" in exp or ("[" in exp and "]" in exp)


def proccess_src_list_expressions(src_list, path):
    matched = list()
    files = os.listdir(path)
    for exp in src_list:
        matched += fnmatch.filter(files, exp) if is_unix_expression(exp) else [exp]
    return matched
