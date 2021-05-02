import json
import os
from pprint import pprint
from issta_tool_dep_diff import depends_diff


def calc_correlation_rate(name):
    commit_list = json_load_data('/home//Dropbox/ArchBugFix/round2-arch-commit/' + name + '.json')
    commit_file_dict = {}
    isolated_list = []
    for commit_id in commit_list:
        print commit_id
        file_list = []
        arch_cmt_path = '/home//arch-fix-commit/' + name + '/' + commit_id
        if os.path.exists(arch_cmt_path) and os.path.exists(arch_cmt_path + '/summary.json'):
            # parse type1 data
            dict1, dict2 = depends_diff(arch_cmt_path, arch_cmt_path + '/pre.json', arch_cmt_path + '/curr.json')
            for i in dict1['+']+dict1['-']+dict2['+']+dict2['-']:
                file_list.append(i[0][0])
                file_list.append(i[0][1])
        file_list = list(set(file_list))
        commit_file_dict[commit_id] = file_list
    for commit_i in commit_list:
        print commit_i
        index = False
        for commit_j in commit_list:
            if commit_i == commit_j:
                continue
            if len(set(commit_file_dict[commit_i]) & set(commit_file_dict[commit_j])) > 0:
                index = True
                print 'break'
                break
        if not index:
            isolated_list.append(commit_i)
    return len(isolated_list), len(commit_list)
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def collect_all_coverage_data():
    project_list = ['pig', 'hadoop', 'cassandra', 'camel', 'cxf', 'openjpa', 'hbase', 'pdfbox']
    value_list = []
    for project in project_list:
        print project
        t1, t2 = calc_correlation_rate(project)
        value_list.append((project, t1, t2))
    for i in value_list:
        print str(i[0])+','+str(i[1])+','+str(i[2])
    print ''
    pass


if __name__ == '__main__':
    collect_all_coverage_data()
    print ''
    pass
