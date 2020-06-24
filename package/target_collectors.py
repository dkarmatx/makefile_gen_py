def collect_target(target, targets_map=dict()):
    if target.get("type", "prog") != "bundle":
        targets_map[target["name"]] = target
    peers = target.get("peerdirs", list())
    if isinstance(peers, list):
        for sub_target in peers:
            collect_target(sub_target, targets_map)


def collect_target_libs(target, lib_targets=dict(), externals=dict()):
    for (x,p) in target.get("external_libs", dict()).items():
        externals[x] = p
    peers = target.get("peerdirs", list())
    if isinstance(peers, list):
        for sub_target in target.get("peerdirs", list()):
            sub_type = sub_target.get("type", "prog")
            if sub_type != "prog":
                if sub_type == "lib":
                    lib_targets[sub_target["name"]] = sub_target
                collect_target_libs(sub_target, lib_targets, externals)


def collect_target_libs_string(target):
    externals = dict()
    lib_targets = dict()
    lib_strings = list()

    collect_target_libs(target, lib_targets, externals)

    lib_strings += ["-l %s -L %s" % (lib["name"], lib.get("out", lib.get("path", "."))) for lib in lib_targets.values()]
    lib_strings += [("-l %s -L %s" % (lib, pth) if len(pth) != 0 else ("-l %s" % lib)) for lib, pth in externals.items()]

    return " ".join(lib_strings)


def collect_libs_rules(target):
    lib_targets = dict()
    rule_strings = list()

    collect_target_libs(target, lib_targets)

    rule_strings += ["$(%s_FILE)" % lib["name"].upper() for lib in lib_targets.values()]
    return " ".join(rule_strings)