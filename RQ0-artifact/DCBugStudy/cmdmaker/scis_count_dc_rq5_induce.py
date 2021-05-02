import json
import os
from pprint import pprint


def count_all_bug_fix_induce():
    bug_induce_list = []
    issue_link_keyword = ['blocks', 'is depended upon by', 'requires', 'breaks', 'causes', 'blocked',
                          'contains', 'incorporates', 'is a parent of']
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    for pro_path in os.listdir(header_path):
        project_path = header_path + '/' + pro_path
        load_data = json_load_data(project_path)
        # load bug type dict
        bug_type_data = json_load_data('/home//Dropbox/ArchBugFix/bug-type-issta/' + pro_path)
        bug_type_dict = {i[0]: i[1] for i in bug_type_data}
        for item in load_data:
            bug_head = item[0][:item[0].index('-')]
            bug_id = item[0]
            bug_item_path = '/home//bugID-fse20/' + bug_head + '/' + bug_id + '.txt'
            t = json_load_data(bug_item_path)
            print bug_id
            print item[1]
            is_induce = False
            for link_item in t['issue_link']:
                if link_item[1] in issue_link_keyword:
                    is_induce = True
                    break
            bug_induce_list.append([bug_id, item[1], is_induce, bug_type_dict[bug_id]])
    pprint(bug_induce_list)
    temp_dict = count_dist(bug_induce_list)
    print '###########################'
    for k, v in temp_dict.items():
        print k
        print v[0]
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


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    count_all_bug_fix_induce()
    print ''