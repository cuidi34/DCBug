import sys


def merge_import_list(path_1, path_2, path_3):
    with open(path_1, 'r') as f1:
        lines1 = f1.readlines()
    with open(path_2, 'r') as f2:
        lines2 = f2.readlines()
    with open(path_3, 'w') as f3:
        f3.writelines(list(set(lines1) | set(lines2)))
    pass


if __name__ == '__main__':
    path1 = sys.argv[1]
    path2 = sys.argv[2]
    path3 = sys.argv[3]
    merge_import_list(path1, path2, path3)
    pass
