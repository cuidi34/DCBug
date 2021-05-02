import json
from pprint import pprint
from operator import add


def one_pattern_measure(name):
    header = '/home/cuidi/Dropbox/ArchBugFix/round2-pattern-finder'
    # read fixes and files
    bug_file_list = json_load_data('/home/cuidi/Dropbox/ArchBugFix/round2-file-proneness/'+name+'.json')
    bug_file_list = map(lambda x: x[0], bug_file_list)
    arch_fix_list = json_load_data('/home/cuidi/Dropbox/ArchBugFix/round2-arch-commit/'+name+'.json')
    # read pattern
    lambda_pattern = json_load_data(header+'/'+name+'-l.json')
    wilson_pattern = json_load_data(header+'/'+name+'-w.json')
    domino_pattern = json_load_data(header+'/'+name+'-d.json')
    # lambda: instances, fix, file
    lambda_files = set(reduce(add, map(lambda x: [x[0]]+x[1][0], lambda_pattern.items())))
    lambda_files = list(lambda_files & set(bug_file_list))
    lambda_fixes = list(set(reduce(add, map(lambda x: x[1][1], lambda_pattern.items()))))
    lambda_instance_num = len(lambda_pattern)
    lambda_file_num = float(len(lambda_files)) / float(len(bug_file_list))
    lambda_fix_num = float(len(lambda_fixes)) / float(len(arch_fix_list))
    # wilson: instances, fix, file
    wilson_files = set(reduce(add, map(lambda x: [x[0]] + x[1][0], wilson_pattern.items())))
    wilson_files = list(wilson_files & set(bug_file_list))
    wilson_fixes = list(set(reduce(add, map(lambda x: x[1][1], wilson_pattern.items()))))
    wilson_instance_num = len(wilson_pattern)
    wilson_file_num = float(len(wilson_files)) / float(len(bug_file_list))
    wilson_fix_num = float(len(wilson_fixes)) / float(len(arch_fix_list))
    # domino: instances, fix, file
    d_list = map(lambda x: x[1], domino_pattern)
    domino_files, domino_fixes = [], []
    for d in d_list:
        for e in d:
            print e
            domino_files += e[0]
            domino_fixes += e[1]
    domino_files, domino_fixes = list(set(domino_files) & set(bug_file_list)), list(set(domino_fixes))
    domino_instance_num = len(domino_pattern)
    domino_file_num = float(len(domino_files)) / float(len(bug_file_list))
    domino_fix_num = float(len(domino_fixes)) / float(len(arch_fix_list))
    # write files in pattern
    with open('/home/cuidi/Dropbox/ArchBugFix/round2-pattern-file/' + name + '-l.json', 'w') as f1:
        json.dump(lambda_files, f1, indent=4)
    with open('/home/cuidi/Dropbox/ArchBugFix/round2-pattern-file/' + name + '-w.json', 'w') as f2:
        json.dump(wilson_files, f2, indent=4)
    with open('/home/cuidi/Dropbox/ArchBugFix/round2-pattern-file/' + name + '-d.json', 'w') as f3:
        json.dump(domino_files, f3, indent=4)
    return [[name, 'lambda', lambda_instance_num, lambda_file_num, lambda_fix_num],
            [name, 'wilson', wilson_instance_num, wilson_file_num, wilson_fix_num],
            [name, 'domino', domino_instance_num, domino_file_num, domino_fix_num]]
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)
    pass


def calc_all_pattern_data():
    t_list = []
    project_list = ['pig', 'hadoop', 'cassandra', 'camel', 'cxf', 'openjpa', 'hbase', 'pdfbox']
    for project in project_list:
        print project
        t = one_pattern_measure(project)
        t_list += t
    pprint(t_list)
    pass


if __name__ == '__main__':
    # one_pattern_measure('pig')
    calc_all_pattern_data()
    print 'cuidi'
    pass
