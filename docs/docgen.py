import itertools
import os
import os.path
import sys
import subprocess as sp
import collections
import json
from pprint import pprint

from sphinx.ext.napoleon.docstring import GoogleDocstring
from sphinx.ext.napoleon import Config

napoleon_config = Config(napoleon_use_param=True, napoleon_use_rtype=True)

json_path = os.path.abspath(sys.argv[1])
out_path = os.path.abspath(sys.argv[2])
roots = sys.argv[3:]
print(f"Generating documentation for {json_path}...")
with open(json_path) as f:
    j = json.load(f)
print("Load done!")

# 2. Get the list of modules and create the documentation tree
modules = {k: v["path"] for k, v in j.items() if v["kind"] == "module"}
parsed_modules = collections.defaultdict(set)

for mid, module in modules.items():
    while module not in roots:
        directory, name = os.path.split(module)
        directory = os.path.relpath(directory, "")  # remove the prefix
        directory = directory.partition("/")
        directory = directory[2] if directory[1] else ""
        os.makedirs(os.path.join(out_path, directory), exist_ok=True)
        if name.endswith(".codon"):
            name = name[:-6]  # drop suffix
        parsed_modules[directory].add((name, mid))
        module = os.path.split(module)[0]

print(f"Module read done!")

for directory, modules in parsed_modules.items():
    module = directory.replace("/", ".")
    with open(f"{out_path}/{directory}/index.md", "w") as f:
        if module:
            print(f"# `{module}`\n", file=f)
        else:
            print("# Standard Library Reference\n", file=f)

        for m in sorted(set(m for m, _ in modules)):
            if m == "__init__":
                continue
            base = os.path.join('libraries', 'api', directory, m)
            is_dir = os.path.isdir(os.path.join(out_path, directory, m))
            print(f"- [`{m}`](/{base}{'/' if is_dir else ''})", file=f)

print(f" - Done with directory tree")


def parse_docstr(s, level=0):
    """Parse docstr s and indent it with level spaces"""
    #lines = GoogleDocstring(s, napoleon_config).lines()
    #print(lines)
    #if isinstance(lines, str):  # Napoleon failed
    s = s.split("\n")
    while s and s[0] == "":
        s = s[1:]
    while s and s[-1] == "":
        s = s[:-1]
    if not s:
        return ""
    i = 0
    indent = len(list(itertools.takewhile(lambda i: i == " ", s[0])))
    lines = [l[indent:] for l in s]
    return "\n".join(("   " * level) + l for l in lines)


def parse_type(a):
    """Parse type signature"""
    if not a:
        return ""
    s = ""
    if isinstance(a, list):
        head, tail = a[0], a[1:]
    else:
        head, tail = a, []
    if head not in j:
        return "?"
    s += j[head]["name"] if head[0].isdigit() else head
    if tail:
        for ti, t in enumerate(tail):
            s += "[" if not ti else ", "
            s += parse_type(t)
        s += "]"
    return s


def parse_fn(v):
    """Parse function signature after the name"""
    s = ""
    if "generics" in v and v["generics"]:
        s += f'[{", ".join(v["generics"])}]'
    s += "("
    cnt = 0
    for ai, a in enumerate(v["args"]):
        s += "" if not cnt else ", "
        cnt += 1
        s += f'{a["name"]}'
        if "type" in a:
            s += ": " + parse_type(a["type"])
        if "default" in a:
            s += " = " + a["default"] + ""
    s += ")"
    if "ret" in v:
        s += " -> " + parse_type(v["ret"])
    # if "extern" in v:
    #     s += f" (_{v['extern']} function_)"
    # s += "\n"
    return s


# 3. Create documentation for each module
visited = set()
for directory, (name, mid) in {(d, m) for d, mm in parsed_modules.items() for m in mm}:
    if directory:
        module = f"{directory.replace('/', '.')}.{name}"
    else:
        module = name

    file, mode = f"{out_path}/{directory}/{name}.md", "w"

    if os.path.isdir(f"{out_path}/{directory}/{name}"):
        continue

    init = (name == "__init__")

    if init:
        file, mode = f"{out_path}/{directory}/index.md", "a"

    if file in visited:
        continue
    else:
        visited.add(file)

    with open(file, mode) as f:
        if not init:
            print(f"# module `{module}`", file=f)

        directory_prefix = directory + "/" if directory != "." else ""
        directory = directory.strip("/")
        dir_part = (directory + "/") if directory else ""
        print(
            f"\nSource: [`stdlib/{dir_part}{name}.codon`](https://github.com/exaloop/codon/blob/master/stdlib/{dir_part}{name}.codon)\n",
            file=f,
        )

        if "doc" in j[mid]:
            print(parse_docstr(j[mid]["doc"]), file=f)

        for i in j[mid]["children"]:
            v = j[i]

            if v["kind"] == "class" and v["type"] == "extension":
                v["name"] = j[v["parent"]]["name"]
            if v["name"].startswith("_"):
                continue

            icon = lambda name: f'<span style="color:#899499">:material-{name}:</span>'

            f.write("---\n")
            f.write("## ")
            if v["kind"] == "class":
                f.write(f'{icon("cube-outline")} **`{v["name"]}')
                if "generics" in v and v["generics"]:
                    f.write(f'[{",".join(v["generics"])}]')
                f.write("`**")
            elif v["kind"] == "function":
                f.write(f'{icon("function")} **`{v["name"]}{parse_fn(v)}`**')
            elif v["kind"] == "variable":
                f.write(f'{icon("variable")} **`{v["name"]}`**')
            # if v['kind'] == 'class' and v['type'] == 'extension':
            #     f.write(f'**{getLink(v["parent"])}**')
            # else:
            # f.write(f'{m}.**{v["name"]}**')
            f.write("\n")

            # f.write("\n")
            # if v['kind'] == 'function' and 'attrs' in v and v['attrs']:
            #     f.write("**Attributes:**" + ', '.join(f'{x}' for x in v['attrs']))
            #     f.write("\n")
            if "doc" in v:
                f.write("\n" + parse_docstr(v["doc"]) + "\n")
            f.write("\n")

            if v["kind"] == "class":
                # if 'args' in v and any(c['name'][0] != '_' for c in v['args']):
                #     f.write('#### Arguments:\n')
                #     for c in v['args']:
                #         if c['name'][0] == '_':
                #             continue
                #         f.write(f'- **{c["name"]} : **')
                #         f.write(parse_type(c["type"]) + "\n")
                #         if 'doc' in c:
                #             f.write(parse_docstr(c['doc'], 1) + "\n")
                #         f.write("\n")

                mt = [c for c in v["members"] if j[c]["kind"] == "function"]

                props = [c for c in mt if "property" in j[c].get("attrs", [])]
                if props:
                    print("## Properties\n", file=f)
                    for c in props:
                        v = j[c]
                        f.write(f'### `{v["name"]}`\n')
                        if "doc" in v:
                            f.write("\n" + parse_docstr(v["doc"]) + "\n\n")
                        f.write("\n")

                magics = [
                    c
                    for c in mt
                    if len(j[c]["name"]) > 4
                    and j[c]["name"].startswith("__")
                    and j[c]["name"].endswith("__")
                ]
                if magics:
                    print("## Magic methods\n", file=f)
                    for c in magics:
                        v = j[c]
                        f.write(
                            f'### `{v["name"]}{parse_fn(v)}`\n'
                        )
                        if "doc" in v:
                            f.write("\n" + parse_docstr(v["doc"]) + "\n\n")
                        f.write("\n")
                methods = [c for c in mt if j[c]["name"][0] != "_" and c not in props]
                if methods:
                    print("## Methods\n", file=f)
                    for c in methods:
                        v = j[c]
                        f.write(
                            f'### `{v["name"]}{parse_fn(v)}`\n'
                        )
                        if "doc" in v:
                            f.write("\n" + parse_docstr(v["doc"]) + "\n\n")
                        f.write("\n")
            f.write("\n\n")

        f.write("\n\n")

print(" - Done with modules")
