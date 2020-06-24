import target_collectors


def generate_compile_rules(target, compilers_options):
    if "c" in compilers_options:
        generate_c_compile_rule(target, compilers_options["c"])
    if "cpp" in compilers_options:
        generate_cpp_compile_rule(target, compilers_options["cpp"])
    if "nasm" in compilers_options:
        generate_nasm_compile_rule(target, compilers_options["nasm"])


def generate_link_rule(target):
    target_type = target.get("type", "prog")
    target_compiler = target.get("compiler", "c")

    if target_type == "prog":
        if target_compiler == "c":
            generate_c_link_rule(target)
        elif target_compiler == "cpp":
            generate_cpp_link_rule(target)

    elif target_type == "lib":
        generate_static_lib_rule(target)


def generate_c_compile_rule(target, compiler_options):
    print("\n".join([
        "$(OBJ_DIR)/%.{f}.o: $({t_upc}_PATH)/%.{f}",
        "\t@mkdir -p $(OBJ_DIR)",
        "\t@printf 'Compiling\t\\033[1;33m$<\\033[0m ...\\n'",
        "\t@$(C_COMPILER) $(C_CFLAGS) $(C_STANDART) $({t_upc}_INCS) -o $@ -c $< -MMD",
        ""
    ]).format(
        t_upc=target["name"].upper(),
        f=compiler_options.get("file_extension", "c"),
    ))


def generate_cpp_compile_rule(target, compiler_options):
    print("\n".join([
        "$(OBJ_DIR)/%.{f}.o: $({t_upc}_PATH)/%.{f}",
        "\t@mkdir -p $(OBJ_DIR)",
        "\t@printf 'Compiling\t\\033[1;33m$<\\033[0m ...\\n'",
        "\t@$(CPP_COMPILER) $(CPP_CFLAGS) $(CPP_STANDART) $({t_upc}_INCS) -o $@ -c $< -MMD",
        ""
    ]).format(
        t_upc=target["name"].upper(),
        f=compiler_options.get("file_extension", "cpp"),
    ))


def generate_nasm_compile_rule(target, compiler_options):
    print("\n".join([
        "$(OBJ_DIR)/%.{f}.o: $({t_upc}_PATH)/%.{f}",
        "\t@mkdir -p $(OBJ_DIR)",
        "\t@printf 'Compiling\t\\033[1;33m$<\\033[0m ...\\n'",
        "\t@$(NASM_COMPILER) $(NASM_FLAGS) $< -o $@ $(NASM_FORMAT) -MD $(OBJ_DIR)/`basename $@ .o`.d -I$({t_upc}_PATH)",
        ""
    ]).format(
        t_upc=target["name"].upper(),
        f=compiler_options.get("file_extension", "s"),
    ))


def generate_c_link_rule(target):
    print("\n".join([
        "$({t_upc}_FILE): {lib_targets} $({t_upc}_OBJS)",
        "\t@$(C_COMPILER) $(C_LFLAGS) $(C_STANDART) -o $({t_upc}_FILE) $({t_upc}_OBJS) {pt} $({t_upc}_LIBS)",
        "\t@printf 'Finished\t\\033[1;32m\\033[7m$@ \\033[0m\\n\\n'",
        ""
    ]).format(
        t_upc=target["name"].upper(),
        lib_targets=target_collectors.collect_libs_rules(target),
        pt="-pthread" if target.get("pthread") else ""
    ))


def generate_cpp_link_rule(target):
    print("\n".join([
        "$({t_upc}_FILE): {lib_targets} $({t_upc}_OBJS)",
        "\t@$(CPP_COMPILER) $(CPP_LFLAGS) $(CPP_STANDART) -o $({t_upc}_FILE) $({t_upc}_OBJS) {pt} $({t_upc}_LIBS)",
        "\t@printf 'Finished\t\\033[1;32m\\033[7m$@ \\033[0m\\n\\n'",
        ""
    ]).format(
        t_upc=target["name"].upper(),
        lib_targets=target_collectors.collect_libs_rules(target),
        pt="-pthread" if target.get("pthread") else ""
    ))


def generate_static_lib_rule(target):
    print("\n".join([
        "$({t_upc}_FILE): $({t_upc}_OBJS)",
        "\t@ar rc $({t_upc}_FILE) $({t_upc}_OBJS)",
        "\t@ranlib $({t_upc}_FILE)",
        "\t@printf 'Finished\t\\033[1;36m\\033[7m$@ \\033[0m\\n\\n'",
        ""
    ]).format(
        t_upc=target["name"].upper()
    ))