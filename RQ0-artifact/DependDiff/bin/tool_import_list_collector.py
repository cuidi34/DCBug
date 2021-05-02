from pprint import pprint
import sys
import os


def read_by_line(path):
    with open(path, "r") as f:
        lines = f.readlines()
        # filter the invalid path and delete the duplicated items
        return list(set(filter(lambda x: '{' not in x and '}' not in x, lines)))
        pass


def read_name_dict(path):
    namedict = {}
    namelist = read_by_line(path)
    for name in namelist:
        if "/org/" in name:
            key = "org."+name.split("org/")[1].strip()
            key = key.strip(".java").replace("/", ".")
            value = name.strip()
            namedict[key] = namedict[key] + [value] if key in namedict else [value]
    # pprint(namedict)
    return namedict
    pass


def map_import_and_name(import_path, dict_path):
    importlist = walk_dir(import_path)
    namedict = read_name_dict(dict_path)
    import_file_list = []
    for oneimport in importlist:
        if oneimport in namedict:
            for i in namedict[oneimport]:
                import_file_list.append(i)
    return import_file_list
    pass


def test_map():
    import_file_list = map_import_and_name("C:\\Users\\11986\\Desktop\\paper-demo-2\\curr.xml", "G:\\ase2019\\name_dict\\cassandra.dict")
    write_name_info(import_file_list, "C:\\Users\\11986\\Desktop\\paper-demo-2\\importlist.txt")


def write_name_info(lines, path):
    with open(path, "w") as f:
        for line in lines:
            f.write(line+"\n")


def walk_dir(dirPath):
    name_list = []
    for maindir, subdir, file_name_list in os.walk(dirPath):
        for filename in file_name_list:
            if filename.endswith(".java"):
                result = os.path.join(maindir, filename)
                name_list.append(result)
    import_list = []
    for name in name_list:
        lines = read_by_line(name)
        lines = filter(lambda x: x.startswith("import "), lines)
        lines = map(lambda x: x.replace("import", "").strip().strip(";"), lines)
        import_list +=lines
    import_list = list(set(import_list))
    final_import_list = []
    for one_import in import_list:
        if " " in one_import or one_import.startswith("java") or one_import.endswith("*"):
            continue
        else:
            final_import_list.append(one_import)
    return final_import_list
    pass


if __name__ == '__main__':
    target_path = sys.argv[1]
    dict_path = sys.argv[2]
    import_path = sys.argv[3]
    # print info
    print "target_path:" + target_path
    print "dict_path:" + dict_path
    print "import_list_path:" + import_path
    # map information
    import_file_list = map_import_and_name(target_path, dict_path)
    write_name_info(import_file_list, import_path)
    print "candi"
