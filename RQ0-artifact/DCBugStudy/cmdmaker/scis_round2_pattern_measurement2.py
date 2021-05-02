import json
from pprint import pprint


def one_pattern_increase_measure(name):
    header = '/home/cuidi/Dropbox/ArchBugFix/round2-pattern-file'
    # read fixes and files
    bug_file_list = json_load_data('/home/cuidi/Dropbox/ArchBugFix/round2-file-proneness/'+name+'.json')
    # read pattern
    lambda_pattern_file = json_load_data(header+'/'+name+'-l.json')
    wilson_pattern_file = json_load_data(header+'/'+name+'-w.json')
    domino_pattern_file = json_load_data(header+'/'+name+'-d.json')
    # collect lambda, wilson and domino files increase
    lambda_fre, lambda_churn = 0, 0
    wilson_fre, wilson_churn = 0, 0
    domino_fre, domino_churn = 0, 0
    total_fre, total_churn = 0, 0
    for bug_item in bug_file_list:
        if bug_item[0] in lambda_pattern_file:
            lambda_fre += int(bug_item[1])
            lambda_churn += int(bug_item[2])
            pass
        if bug_item[0] in wilson_pattern_file:
            wilson_fre += int(bug_item[1])
            wilson_churn += int(bug_item[2])
            pass
        if bug_item[0] in domino_pattern_file:
            domino_fre += int(bug_item[1])
            domino_churn += int(bug_item[2])
            pass
        total_fre += int(bug_item[1])
        total_churn += int(bug_item[2])
        print bug_item
    return [[name+'-fre', 'lambda', float(lambda_fre)/float(len(lambda_pattern_file)),
             'wilson', float(wilson_fre)/float(len(wilson_pattern_file)),
             'domino', float(domino_fre)/float(len(domino_pattern_file)),
             'total', float(total_fre)/float(len(bug_file_list))],
            [name+'-churn', 'lambda', float(lambda_churn) / float(len(lambda_pattern_file)),
             'wilson', float(wilson_churn) / float(len(wilson_pattern_file)),
             'domino', float(domino_churn) / float(len(domino_pattern_file)),
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
        t = one_pattern_increase_measure(project)
        t_list += t
    for t in t_list:
        print t
    pass


if __name__ == '__main__':
    calc_all_pattern_data()
    print 'cuidi'