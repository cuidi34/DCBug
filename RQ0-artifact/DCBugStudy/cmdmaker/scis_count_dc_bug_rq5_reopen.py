import json
import os
from pprint import pprint


def count_all_bug_fix_reopen():
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    reopen_list = []
    for pro_path in os.listdir(header_path):
        project_path = header_path + '/' + pro_path
        # load transition data
        trans_path = '/home//Dropbox/ArchBugFix/bug-transition-issta/'+pro_path
        trans_data = json_load_data(trans_path)
        trans_dict = {}
        for bug_id, trans_list in trans_data.items():
            trans_dict[bug_id] = calc_reopen_times(trans_list)
        # load arch bug data
        load_data = json_load_data(project_path)
        # load bug type dict
        bug_type_data = json_load_data('/home//Dropbox/ArchBugFix/bug-type-issta/' + pro_path)
        bug_type_dict = {i[0]: i[1] for i in bug_type_data}
        for item in load_data:
            bug_id = item[0]
            reopen_list.append([bug_id, item[1], trans_dict[bug_id], bug_type_dict[bug_id]])
    pprint(reopen_list)
    reopen_dict = count_dist(reopen_list)
    print '###########################'
    for k, v in reopen_dict.items():
        print 'reopen times:'+str(k)
        print 'num:'+str(v[0])
        pprint(v[1])


def count_dist(bug_induce_list):
    induce_dict = {}
    for item in bug_induce_list:
        print item
        print item[0]
        print item[1]
        print item[2]
        print item[3]
        arch_type = item[1]
        ice = item[2]
        bug_type = item[3]
        if ice not in induce_dict:
            induce_dict[ice] = (0, {})
        # set pri dict
        induce_num = induce_dict[ice][0] + 1
        induce_sub_dict = induce_dict[ice][1]
        induce_sub_dict[bug_type] = induce_sub_dict[bug_type] + 1 if bug_type in induce_sub_dict else 1
        if arch_type:
            induce_sub_dict['arch'] = induce_sub_dict['arch'] + 1 if 'arch' in induce_sub_dict else 1
        # set priority dict
        induce_dict[ice] = (induce_num, induce_sub_dict)
    return induce_dict
    pass


def calc_reopen_times(trans_list):
    word_list = []
    for t in trans_list:
        word_list.append(t[0])
        word_list.append(t[1])
    return int(float(word_list.count('Reopened'))/2)
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    count_all_bug_fix_reopen()
    print ''