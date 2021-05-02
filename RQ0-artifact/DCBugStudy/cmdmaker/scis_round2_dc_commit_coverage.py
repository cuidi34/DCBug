import json
from pprint import pprint


def calc_bug_space_coverage(name):
    bug_space = json_load_data('/home/cuidi/Dropbox/ArchBugFix/round2-file-proneness/'+name+'.json')
    bug_fre_rank = sorted(bug_space, key=lambda x: x[1], reverse=True)
    bug_churn_rank = sorted(bug_space, key=lambda x: x[2], reverse=True)
    with open('/home/cuidi/Dropbox/ArchBugFix/round2-arch-dsm/'+name+'.dsm', 'r') as f:
        lines = f.readlines()
        arch_file_list = map(lambda x: x.strip(), lines[2+int(lines[1]):])
    # calculate precision and recall
    arch_file_list = list(set(arch_file_list) & set(map(lambda x: x[0],bug_space)))
    for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        print 'top: ' + str(i)
        count_top_percentage(bug_fre_rank, arch_file_list, i)
        count_top_percentage(bug_churn_rank, arch_file_list, i)
    calculate_increase(bug_fre_rank, arch_file_list)
    pass


def count_top_percentage(target_list, arch_list, percentage):
    target_list = map(lambda x: x[0], target_list)
    target_list = target_list[:int(float(len(target_list)) * percentage)]
    recall = float(len(set(arch_list) & set(target_list))) / float(len(target_list))
    precision = float(len(set(arch_list) & set(target_list))) / float(len(arch_list))
    print 'precision,'+str(precision)+',recall,'+str(recall)
    pass


def calculate_increase(target_list, arch_list):
    arch_fre, total_fre, arch_churn, total_churn = 0, 0, 0, 0
    for target in target_list:
        if target[0] in arch_list:
            arch_fre += target[1]
            arch_churn += target[2]
        total_fre += target[1]
        total_churn += target[2]
    print float(arch_fre)/float(len(arch_list))
    print float(total_fre)/float(len(target_list))
    print float(arch_churn)/float(len(arch_list))
    print float(total_churn)/float(len(target_list))
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def collect_all_coverage_data():
    project_list = ['pig', 'hadoop', 'cassandra', 'camel', 'cxf', 'openjpa', 'hbase', 'pdfbox']
    for project in project_list:
        print project
        calc_bug_space_coverage(project)
    print 'cuidi'
    pass


if __name__ == '__main__':
    collect_all_coverage_data()
    print 'cuidi'
    pass
