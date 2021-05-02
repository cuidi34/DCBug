import os
import json
from nltk.stem.porter import PorterStemmer
from pprint import pprint
from jira.client import JIRA


def collect_all_bug_fix_type():
    # init stemmer
    porter_stemmer = PorterStemmer()
    type_dict = json_load_data('type/type.json')
    # load header
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    for pro_path in os.listdir(header_path):
        type_list = []
        project_path = header_path + '/' + pro_path
        load_data = json_load_data(project_path)
        for item in load_data:
            bug_head = item[0][:item[0].index('-')]
            bug_id = item[0]
            print bug_id
            bug_item_path = '/home//bugID-fse20/' + bug_head + '/' + bug_id + '.txt'
            t = json_load_data(bug_item_path)
            key_word_list = [i.lower() for i in t['summary'].strip('.').split(' ')] + \
                            [j.lower() for j in t['description'].strip('.').split(' ')]
            bug_type = bug_type_classifier(porter_stemmer, key_word_list, type_dict)
            print bug_type
            type_list.append((bug_id, bug_type))
        with open('/home//Dropbox/ArchBugFix/bug-type-issta/' + pro_path, 'w') as f:
            json.dump(type_list, f, indent=4)


'''
classify description
'''


def bug_type_classifier(porter_stemmer, key_word_list, type_dict):
    score_list = []
    print key_word_list
    key_word_list = [i.strip(';') for i in key_word_list]
    key_word_list = [porter_stemmer.stem(i) for i in key_word_list]
    # round-1 matching: representativeness
    match_list = [('security', 'security-issue'),
                  ('permission', 'permission-issue'),
                  ('performance', 'performance-issue'),
                  ('SQL', 'database-issue'),
                  ('Query', 'database-issue'),
                  ('Database', 'database-issue'),
                  ('HTTP', 'network-issue'),
                  ('NullPointerExeption', 'functional-issue')]
    for match_item in match_list:
        target_word = match_item[0]
        target_type = match_item[1]
        for key_word in key_word_list:
            if target_word in key_word or porter_stemmer.stem(target_word) in key_word:
                return target_type
    # round-2 matching: key word matching
    for type_key, type_value in type_dict.items():
        score_list.append((type_key, len(set(type_value) & set(key_word_list))))
    final_type = max(score_list, key=lambda x: x[1])
    # round-3 matching: test and exception
    if final_type != 'security-issue' and final_type != 'permission-issue' \
            and final_type != 'performance-issue' and final_type != 'network-issue':
        match_list = [('test', 'test-issue'),
                      ('exception', 'functional-issue')]
        for match_item in match_list:
            target_word = match_item[0]
            target_type = match_item[1]
            for key_word in key_word_list:
                if target_word in key_word or porter_stemmer.stem(target_word) in key_word:
                    return target_type
        pass
    return final_type[0] if final_type[1] > 0 else 'not sure'
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


'''
count classification
'''


def count_all_bug_fix_type():
    # setting count dict including type1 and type2
    # four items: issue_count, arch_count, type_1_count, type_2_count
    # 0-3: num, arch-num, type1-num, type2-num
    # 4-14: call, cast, contain, create, extend, implement, import, parameter, return, throw, use
    count_dict = {'configuration-issue': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  'network-issue': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  'database-issue': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  'gui-issue': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  'performance-issue': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  'permission-issue': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  'security-issue': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  'functional-issue': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  'test-issue': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  'not sure': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    # iter each fix
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        # load arch type data
        arch_type_data = json_load_data('/home//Dropbox/ArchBugFix/arch-type-issta/'+pro_path)
        arch_type_dict = build_arch_type_dict(arch_type_data)
        pprint(arch_type_dict)
        # load bug type data
        bug_type_data = json_load_data('/home//Dropbox/ArchBugFix/bug-type-issta/'+pro_path)
        print project_name
        for bug_item in bug_type_data:
            print bug_item
            t1 = arch_type_dict[bug_item[0]][0]
            t2 = arch_type_dict[bug_item[0]][1]
            relation_type_list = arch_type_dict[bug_item[0]][4]
            relation_type_list = type_index_generator(relation_type_list)
            print relation_type_list
            count_dict[bug_item[1]] = [count_dict[bug_item[1]][0]+1,
                                       count_dict[bug_item[1]][1]+int(t1 or t2),
                                       count_dict[bug_item[1]][2]+int(t1),
                                       count_dict[bug_item[1]][3]+int(t2),
                                       count_dict[bug_item[1]][4]+relation_type_list[0],
                                       count_dict[bug_item[1]][5]+relation_type_list[1],
                                       count_dict[bug_item[1]][6]+relation_type_list[2],
                                       count_dict[bug_item[1]][7]+relation_type_list[3],
                                       count_dict[bug_item[1]][8]+relation_type_list[4],
                                       count_dict[bug_item[1]][9]+relation_type_list[5],
                                       count_dict[bug_item[1]][10]+relation_type_list[6],
                                       count_dict[bug_item[1]][11]+relation_type_list[7],
                                       count_dict[bug_item[1]][12]+relation_type_list[8],
                                       count_dict[bug_item[1]][13]+relation_type_list[9],
                                       count_dict[bug_item[1]][14]+relation_type_list[10]]
            # count_dict[bug_item[1]] += 1
    for k, v in count_dict.items():
        print k
        print v
    pass


def count_arch_fix_type():
    # setting count dict including type1 and type2
    # four items: issue_count, arch_count, type_1_count, type_2_count
    # 0-3: num, arch-num, type1-num, type2-num
    # 4-14: call, cast, contain, create, extend, implement, import, parameter, return, throw, use
    count_dict = {'Call': [0, 0, 0, 0],
                  'Cast': [0, 0, 0, 0],
                  'Contain': [0, 0, 0, 0],
                  'Create': [0, 0, 0, 0],
                  'Extend': [0, 0, 0, 0],
                  'Implement': [0, 0, 0, 0],
                  'Import': [0, 0, 0, 0],
                  'Parameter': [0, 0, 0, 0],
                  'Return': [0, 0, 0, 0],
                  'Throw': [0, 0, 0, 0],
                  'Use': [0, 0, 0, 0]}
    # iter each fix
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    all_bug, t1_bug, t2_bug, t3_bug = 0, 0, 0, 0
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        # load arch type data
        arch_type_data = json_load_data('/home//Dropbox/ArchBugFix/arch-type-issta/'+pro_path)
        for temp in arch_type_data:
            bug_id = temp[0]
            type1_list = temp[1][0]
            type2_list = temp[1][1]
            print bug_id
            i = -1
            if len(type1_list) > 0 and len(type2_list) > 0:
                t3_bug += 1
                i = 3
            if len(type1_list) > 0 and len(type2_list) == 0:
                t1_bug += 1
                i = 1
            if len(type2_list) > 0 and len(type1_list) == 0:
                t2_bug += 1
                i = 2
            if len(type1_list) > 0 or len(type2_list) > 0:
                all_bug += 1
            for t in list(set(type1_list+type2_list)):
                if t == 'Annotation':
                    continue
                count_dict[t] = [count_dict[t][0]+1, count_dict[t][1], count_dict[t][2], count_dict[t][3]]
                if i == 1:
                    count_dict[t] = [count_dict[t][0], count_dict[t][1] + 1, count_dict[t][2], count_dict[t][3]]
                    pass
                if i == 2:
                    count_dict[t] = [count_dict[t][0], count_dict[t][1], count_dict[t][2] + 1, count_dict[t][3]]
                    pass
                if i == 3:
                    count_dict[t] = [count_dict[t][0], count_dict[t][1], count_dict[t][2], count_dict[t][3] + 1]
                    pass
                pass
    for k, v in count_dict.items():
        print k
        print v
    print 'all:' + str(all_bug)
    print 't1:' + str(t1_bug)
    print 't2:' + str(t2_bug)
    print 't3:' + str(t3_bug)
    pass


def build_arch_type_dict(arch_type_data):
    arch_type_dict = {}
    for item in arch_type_data:
        type_1_list = list(set(filter_annotation(item[1][0])))
        type_2_list = list(set(filter_annotation(item[1][1])))
        type_list = list(set(filter_annotation(item[1][0]) +
                             filter_annotation(item[1][1])))
        # filter annotation
        arch_type_dict[item[0]] = [True if len(item[1][0]) > 0 else False,
                                   True if len(item[1][1]) > 0 else False,
                                   type_1_list,
                                   type_2_list,
                                   type_list]
    return arch_type_dict
    pass


def filter_annotation(target_list):
    if 'Annotation' in target_list:
        target_list.remove('Annotation')
        return target_list+['use']
    else:
        return target_list
    pass


'''
1. call 2. cast 3. contain 4. create 5. extend
6. implement 7. import 8. parameter 9. return 10. throw 11. use
'''


def type_index_generator(relation_type_list):
    return [1 if 'Call' in relation_type_list else 0,
            1 if 'Cast' in relation_type_list else 0,
            1 if 'Contain' in relation_type_list else 0,
            1 if 'Create' in relation_type_list else 0,
            1 if 'Extend' in relation_type_list else 0,
            1 if 'Implement' in relation_type_list else 0,
            1 if 'Import' in relation_type_list else 0,
            1 if 'Parameter' in relation_type_list else 0,
            1 if 'Return' in relation_type_list else 0,
            1 if 'Throw' in relation_type_list else 0,
            1 if 'Use' in relation_type_list else 0]
    pass


if __name__ == '__main__':
    # collect_all_bug_fix_type()
    # count_all_bug_fix_type()
    count_arch_fix_type()
    print ''