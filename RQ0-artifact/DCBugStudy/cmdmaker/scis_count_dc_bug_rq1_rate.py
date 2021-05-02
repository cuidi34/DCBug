import os
import json
from pprint import pprint
import csv

'''
collect data
'''


def iter_bug_fix():
    path = '/home/cuidi/Dropbox/ArchBugFix/commit-fixing-log-fse20'
    i = 0
    for project_name in os.listdir(path):
        i += 1
        print i
        issue_index_list = iter_bug_fix_one_project(path, project_name)
        pprint(issue_index_list)
        with open('/home/cuidi/Dropbox/ArchBugFix/arch-bug-issta/'+project_name+'.json', 'w') as f:
            json.dump(issue_index_list, f)


def iter_bug_fix_one_project(header, project):
    issue_index_list = []
    with open(header+'/'+project+'/bug-fix.txt', 'r') as f:
        data = json.load(f)
        for issue_id, cmt_list in data.items():
            print issue_id
            index = False
            for cmt in cmt_list:
                cmt_path = '/home/cuidi/arch-fix-commit/'+project+'/'+cmt
                print cmt_path
                temp_index = summary_reader(cmt_path)
                index = index | temp_index
            issue_index_list.append((issue_id,index))
    return issue_index_list
    pass


def summary_reader(path):
    if os.path.exists(path + '/summary.json'):
        with open(path + '/summary.json', 'r') as f:
            lines = f.readlines()
            type1 = 1 if 'True' in lines[0] else 0
            type2 = 1 if 'True' in lines[1] else 0
            return bool(type1) | bool(type2)
    return False
    pass


'''
analyze data
'''


def count_bug_fix():
    # count each project
    write_list = []
    header_path = '/home/cuidi/Dropbox/ArchBugFix/arch-bug-issta'
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        project_path = header_path+'/'+pro_path
        load_data = json_load_data(project_path)
        temp_report_num = len(load_data)
        temp_arch_report_num = len(filter(lambda x: x[1] == True, load_data))
        write_list.append([project_name, temp_report_num, temp_arch_report_num])
    # write results
    with open('issta/arch_rate.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, lineterminator='\n')
        csv_writer.writerows(write_list)
    pass


def count_all_bug_fix():
    header_path = '/home/cuidi/Dropbox/ArchBugFix/arch-bug-issta'
    all_list = []
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        project_path = header_path + '/' + pro_path
        load_data = json_load_data(project_path)
        all_list = all_list+load_data
    all_list = dict(all_list).items()
    temp_report_num = len(all_list)
    temp_arch_report_num = len(filter(lambda x: x[1] == True, all_list))
    print temp_report_num
    print temp_arch_report_num
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    #iter_bug_fix()
    count_all_bug_fix()
    print 'cuidi'