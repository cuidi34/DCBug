import json
from pprint import pprint


def pattern_combination_increase_measure(name):
    header = '/home/cuidi/Dropbox/ArchBugFix/round2-pattern-file'
    # read fixes and files
    bug_file_list = json_load_data('/home/cuidi/Dropbox/ArchBugFix/round2-file-proneness/'+name+'.json')
    # read pattern
    lambda_pattern_file = json_load_data(header+'/'+name+'-l.json')
    wilson_pattern_file = json_load_data(header+'/'+name+'-w.json')
    domino_pattern_file = json_load_data(header+'/'+name+'-d.json')
    pattern_time_dict = {}
    with open('/home/cuidi/Dropbox/ArchBugFix/round2-arch-dsm/'+name+'.dsm', 'r') as f:
        lines = f.readlines()
        arch_file_list = map(lambda x: x.strip(), lines[2+int(lines[1]):])
    simply_bug_file_list = map(lambda x: x[0], bug_file_list)
    for bug_file in arch_file_list:
        if bug_file not in simply_bug_file_list:
            continue
        times = (1 if bug_file in lambda_pattern_file else 0) + \
                (1 if bug_file in wilson_pattern_file else 0) + \
                (1 if bug_file in domino_pattern_file else 0)
        if times not in pattern_time_dict:
            pattern_time_dict[times] = []
        pattern_time_dict[times].append(bug_file)
    # collect the data of (0, 1, 2, 3) times of bug file
    list_0, list_1, list_2, list_3 = pattern_time_dict[0], pattern_time_dict[1], pattern_time_dict[2], pattern_time_dict[3]
    fre_0, churn_0 = 0, 0
    fre_1, churn_1 = 0, 0
    fre_2, churn_2 = 0, 0
    fre_3, churn_3 = 0, 0
    total_fre, total_churn = 0, 0
    for bug_item in bug_file_list:
        if bug_item[0] in list_0:
            fre_0 += int(bug_item[1])
            churn_0 += int(bug_item[2])
            pass
        if bug_item[0] in list_1:
            fre_1 += int(bug_item[1])
            churn_1 += int(bug_item[2])
            pass
        if bug_item[0] in list_2:
            fre_2 += int(bug_item[1])
            churn_2 += int(bug_item[2])
            pass
        if bug_item[0] in list_3:
            fre_3 += int(bug_item[1])
            churn_3 += int(bug_item[2])
            pass
        total_fre += int(bug_item[1])
        total_churn += int(bug_item[2])
        print bug_item
    return [[name + '-fre', '0', float(fre_0) / float(len(list_0)),
             '1', float(fre_1) / float(len(list_1)),
             '2', float(fre_2) / float(len(list_2)),
             '3', float(fre_3) / float(len(list_3)),
             'total', float(total_fre) / float(len(bug_file_list))],
            [name + '-churn', '0', float(churn_0) / float(len(list_0)),
             '1', float(churn_1) / float(len(list_1)),
             '2', float(churn_2) / float(len(list_2)),
             '3', float(churn_3) / float(len(list_3)),
             'total', float(total_churn) / float(len(bug_file_list))]]
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
        t = pattern_combination_increase_measure(project)
        t_list += t
    for t in t_list:
        print t
    pass


if __name__ == '__main__':
    # pattern_combination_increase_measure('pig')
    calc_all_pattern_data()
    print 'cuidi'
    pass