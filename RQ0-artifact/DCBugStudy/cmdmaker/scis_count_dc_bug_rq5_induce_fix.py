import json
import os
from pprint import pprint


def count_all_bug_fix_time():
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    supply_fix_list = []
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        project_path = header_path + '/' + pro_path
        # load bug fix data
        bug_fix_path = '/home//Dropbox/ArchBugFix/commit-fixing-log-fse20/'+project_name+'/bug-fix.txt'
        bug_fix_data = json_load_data(bug_fix_path)
        # load arch bug data
        load_data = json_load_data(project_path)
        # load bug type dict
        bug_type_data = json_load_data('/home//Dropbox/ArchBugFix/bug-type-issta/' + pro_path)
        bug_type_dict = {i[0]: i[1] for i in bug_type_data}
        for item in load_data:
            bug_head = item[0][:item[0].index('-')]
            bug_id = item[0]
            print bug_id
            print len(bug_fix_data[bug_id])
            supply_fix_list.append((bug_id, item[1], len(bug_fix_data[bug_id]), bug_type_dict[bug_id]))
    pprint(supply_fix_list)
    fix_times_dict = count_dist(supply_fix_list)
    for k, v in fix_times_dict.items():
        print str(k)+','+str(v[0])+','+str(v[1])
    # pprint(fix_times_dict)
    pass


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
            induce_dict[ice] = (0, {'arch': 0, 'configuration-issue': 0, 'database-issue': 0,
                                    'functional-issue': 0, 'gui-issue': 0, 'network-issue': 0,
                                    'not sure': 0, 'performance-issue': 0, 'permission-issue': 0,
                                    'security-issue': 0, 'test-issue': 0})
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


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    count_all_bug_fix_time()
    print ''
    pass