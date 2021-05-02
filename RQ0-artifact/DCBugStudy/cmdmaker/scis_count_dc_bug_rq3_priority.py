import json
import os
from pprint import pprint


'''
extend to multiple label 
'''


def count_all_bug_fix_priority():
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    priority_dict = {}
    for pro_path in os.listdir(header_path):
        # load bug type data
        bug_type_data = json_load_data('/home//Dropbox/ArchBugFix/bug-type-issta/'+pro_path)
        bug_type_dict = {i[0]: i[1] for i in bug_type_data}
        # load arch type data
        project_path = header_path + '/' + pro_path
        load_data = json_load_data(project_path)
        for item in load_data:
            bug_head = item[0][:item[0].index('-')]
            bug_id = item[0]
            bug_item_path = '/home//bugID-fse20/'+bug_head+'/'+bug_id+'.txt'
            t = json_load_data(bug_item_path)
            print bug_id
            arch_type = item[1]
            bug_type = bug_type_dict[bug_id]
            print arch_type
            print bug_type
            pri = t['priority']
            pprint(pri)
            # judge
            if pri not in priority_dict:
                priority_dict[pri] = (0, {})
            # set pri dict
            pri_num = priority_dict[pri][0]+1
            pri_dict = priority_dict[pri][1]
            pri_dict[bug_type] = pri_dict[bug_type]+1 if bug_type in pri_dict else 1
            if arch_type:
                pri_dict['arch'] = pri_dict['arch'] + 1 if 'arch' in pri_dict else 1
            # set priority dict
            priority_dict[pri] = (pri_num, pri_dict)
            # priority_dict[pri] = (priority_dict[pri][0]+1, priority_dict[pri][1]+(1 if item[1] == True else 0))
            # print priority_dict[pri]
    print '####################'
    pprint(priority_dict)
    print '###################'
    for k, v in priority_dict.items():
        print k
        print v[0]
        pprint(v[1])
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def json_load_bug_info(path):
    with open(path, 'r') as f:
        return json.loads(f.readline().decode("utf-8", "ignore"))
    pass


if __name__ == '__main__':
    count_all_bug_fix_priority()
    print ''