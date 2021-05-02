import os
import json
from pprint import pprint


def dir_loop():
    header = 'C:\\Users\\Administrator\\Dropbox\\ArchBugFix\\commit-fixing-log-fse20'
    write_list = []
    for dir_name in os.listdir(header):
        commit_file_path = header+'\\'+dir_name+'\\commit-fix.txt'
        print dir_name
        if os.path.exists('C:\\Users\\Administrator\\Dropbox\\ArchBugFix\\arch-bug-issta\\'+dir_name+'.json'):
            commit_fix_data = json_load_data(commit_file_path)
            write_list.append(dir_name+';'+str(len(commit_fix_data))+'\n')
    with open('arch-fix-1.txt', 'w') as f:
        f.writelines(write_list)
    pass


def dir_loop1():
    header = 'C:\\Users\\Administrator\\Dropbox\\ArchBugFix\\commit-fixing-log-fse20'
    write_list = []
    for dir_name in os.listdir(header):
        arch_num, type_1_num, type_2_num, type_3_num = 0, 0, 0, 0
        commit_file_path = header+'\\'+dir_name+'\\commit-fix.txt'
        print dir_name
        commit_fix_data = json_load_data(commit_file_path)
        for commit_id in commit_fix_data.keys():
            print commit_id
            summary_path = 'J:\\fse2020-data\\arch-fix-commit\\'+dir_name+'\\'+commit_id+'\\summary.json'
            t1, t2, t3, t4 = summary_reader(summary_path)
            arch_num += int(t1)
            type_1_num += int(t2)
            type_2_num += int(t3)
            type_3_num += int(t4)
        write_list.append(dir_name+';'+str(arch_num)+';'+str(type_1_num)+';'+str(type_2_num)+';'+str(type_3_num)+'\n')
    with open('arch-fix.txt', 'w') as f:
        f.writelines(write_list)
    pass



def summary_reader(path):
    if not os.path.exists(path):
        return 0, 0, 0, 0
    with open(path, 'r') as f:
        lines = f.readlines()
        t1 = lines[0].strip().split(':')[1]
        t1 = True if t1 == 'True' else False
        t2 = lines[1].strip().split(':')[1]
        t2 = True if t2 == 'True' else False
        return t1 | t2, t1, t2, t1 & t2


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)
    pass


if __name__ == '__main__':
    dir_loop()
    print ''