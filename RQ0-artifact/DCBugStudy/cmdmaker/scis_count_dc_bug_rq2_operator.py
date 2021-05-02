import json
import os
from pprint import pprint
from issta_tool_dep_diff import depends_diff

'''
count statistics
'''


def count_all_bug_fix_operator():
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    arch_type_dict = {'type1': 0, 'type2': 0, 'type1+2': 0}
    type1_dict, type2_dict = {}, {}
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        arch_type_path = '/home//Dropbox/ArchBugFix/arch-type-issta/'+project_name+'.json'
        # load arch type data
        arch_type_data = json_load_data(arch_type_path)
        for type_item in arch_type_data:
            print type_item
            # count type item
            if len(type_item[1][0]) > 0:
                arch_type_dict['type1'] += 1
            if len(type_item[1][1]) > 0:
                arch_type_dict['type2'] += 1
            if len(type_item[1][0]) > 0 and len(type_item[1][1]) > 0:
                arch_type_dict['type1+2'] += 1
            print type_item[1][0]
            print type_item[1][1]
            # count type dict
            for tr in type_item[1][0]:
                type1_dict[tr] = type1_dict[tr]+1 if tr in type1_dict else 1
            for tr in type_item[1][1]:
                type2_dict[tr] = type2_dict[tr]+1 if tr in type2_dict else 1
    print 'type count:'
    pprint(arch_type_dict)
    print 'type1:'
    pprint(type1_dict)
    print 'type2:'
    pprint(type2_dict)
    pass


def count_all_bug_fix_operator_v2():
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    arch_type_dict = {'type1': 0, 'type2': 0, 'type1+2': 0}
    type1_dict, type2_dict, type3_dict = {}, {}, {}
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        arch_type_path = '/home//Dropbox/ArchBugFix/arch-type-issta/'+project_name+'.json'
        # load arch type data
        arch_type_data = json_load_data(arch_type_path)
        for type_item in arch_type_data:
            print type_item
            # count type item
            if len(type_item[1][0]) > 0:
                arch_type_dict['type1'] += 1
            if len(type_item[1][1]) > 0:
                arch_type_dict['type2'] += 1
            if len(type_item[1][0]) > 0 and len(type_item[1][1]) > 0:
                arch_type_dict['type1+2'] += 1
            print type_item[1][0]
            print type_item[1][1]
            # count type dict
            for tr in set(type_item[1][0])-set(type_item[1][1]):
                type1_dict[tr] = type1_dict[tr]+1 if tr in type1_dict else 1
            for tr in set(type_item[1][1])-set(type_item[1][0]):
                type2_dict[tr] = type2_dict[tr]+1 if tr in type2_dict else 1
            for tr in set(type_item[1][0]) & set(type_item[1][1]):
                type3_dict[tr] = type3_dict[tr] + 1 if tr in type3_dict else 1
    print 'type count:'
    pprint(arch_type_dict)
    print 'type1:'
    pprint(type1_dict)
    print 'type2:'
    pprint(type2_dict)
    print 'type3:'
    pprint(type3_dict)
    pass


'''
data collection
'''


def collect_all_bug_fix_operator():
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        project_path = header_path + '/' + pro_path
        # load bug fix data
        bug_fix_path = '/home//Dropbox/ArchBugFix/commit-fixing-log-fse20/'+project_name+'/bug-fix.txt'
        bug_fix_data = json_load_data(bug_fix_path)
        # load arch bug data
        load_data = json_load_data(project_path)
        operator_list = []
        for item in load_data:
            bug_head = item[0][:item[0].index('-')]
            bug_id = item[0]
            print bug_id
            type1, type2 = [], []
            if item[1]:
                for fix_cmt in bug_fix_data[bug_id]:
                    print fix_cmt
                    t1, t2 = operator_collector('/home//arch-fix-commit/' + project_name + '/' + fix_cmt)
                    type1 += t1
                    type2 += t2
            type1, type2 = list(set(type1)), list(set(type2))
            operator_list.append((bug_id, [type1, type2]))
        # write results
        with open('/home//Dropbox/ArchBugFix/arch-type-issta/'+project_name+'.json', 'w') as f:
            json.dump(operator_list, f)
    pass


def operator_collector(path):
    if os.path.exists(path + '/pre.json') and os.path.exists(path + '/curr.json'):
        dict1, dict2 = depends_diff(path, path + '/pre.json', path + '/curr.json')
        # type 1
        type1, type2 = [], []
        for i in dict1['+']+dict1['-']:
            for ij in i[1]:
                type1.append(ij)
        # type 2
        for i in dict2['+']+dict2['-']:
            for ij in i[1]:
                type2.append(ij)
        return list(set(type1)), list(set(type2))
    return [], []
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    # collect_all_bug_fix_operator()
    count_all_bug_fix_operator_v2()
    print ''