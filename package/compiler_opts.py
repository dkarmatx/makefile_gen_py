def generate_c_opts(options):
    print("\n".join([
        "C_COMPILER = {binary}",
        "C_STANDART = {std}",
        "C_CFLAGS = {compile_flags} $(CFLAGS) $(CPPFLAGS) {flags}",
        "C_LFLAGS = {linker_flags} $(CFLAGS) $(CPPFLAGS) {flags}",
        ""
    ]).format(
        binary=options.get("binary", "clang"),
        std=options.get("std", ""),
        compile_flags=options.get("compile_flags", ""),
        linker_flags=options.get("link_flags", ""),
        flags=options.get("flags", "")
    ))


def generate_cpp_opts(options):
    print("\n".join([
        "CPP_COMPILER = {binary}",
        "CPP_STANDART = {std}",
        "CPP_CFLAGS = {compile_flags} $(CXXFLAGS) $(CPPFLAGS) {flags}",
        "CPP_LFLAGS = {linker_flags} $(CXXFLAGS) $(CPPFLAGS) {flags}"
        ""
    ]).format(
        binary=options.get("binary", "clang++"),
        std=options.get("std", ""),
        compile_flags=options.get("compile_flags", ""),
        linker_flags=options.get("link_flags", ""),
        flags=options.get("flags", "")
    ))


def generate_nasm_opts(options):
    print("\n".join([
        "NASM_COMPILER = {binary}",
        "NASM_FORMAT = {out_format}",
        "NASM_FLAGS = {flags}",
        ""
    ]).format(
        binary=options.get("binary", "nasm"),
        flags=options.get("flags", ""),
        out_format="-f %s" % options["format"] if "format" in options else ""
    ))


def generate_compilers_options(compiler_options=dict()):
    print("# **************************************************************************** #")
    print("# COMPILER_OPTIONS\n")
    if len(compiler_options) == 0 or "c" in compiler_options:
        generate_c_opts(compiler_options.get("c", dict()))
    if "cpp" in compiler_options:
        generate_cpp_opts(compiler_options["cpp"])
    if "nasm" in compiler_options:
        generate_nasm_opts(compiler_options["nasm"])