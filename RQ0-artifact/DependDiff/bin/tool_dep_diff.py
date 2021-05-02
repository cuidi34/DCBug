import json
from pprint import pprint
import sys
import os

'''
parse json relation
'''


def depends_json_parser(header, path):
    with open(path, 'r') as f:
        t = json.load(f)
        t['variables'] = map(lambda y: y[y.index(os.sep)+1:], map(lambda x: x.replace(header+os.sep, ''), t['variables']))
        return t
    pass


def relation_dict_generator(t):
    relation_dict = {}
    for cell in t['cells']:
        src = t['variables'][cell['src']]
        dest = t['variables'][cell['dest']]
        temp_list = cell['values'].keys()
        relation_dict[(src, dest)] = temp_list
        pass
    return relation_dict
    pass


'''
determining the data structure of dep diff

(filename1, filename2) -> {call: [(), (), ... ], 
                           use:  [(), (), ... ], 
                           return: []}
'''


def depends_diff(header, path1, path2, type_1_path, type_2_path, summary_path):
    t1 = relation_dict_generator(depends_json_parser(header, path1))
    t2 = relation_dict_generator(depends_json_parser(header, path2))
    # pprint(t1)
    # pprint('-----------------------------')
    # pprint(t2)
    # type I - diff analysis
    dict_1 = {'+': list(set(t2.keys())-set(t1.keys())),
              '-': list(set(t1.keys())-set(t2.keys()))}
    # type II - diff analysis
    dict_2 = {'+': [], '-': []}
    for i in set(t1.keys()) & set(t2.keys()):
        if len(set(t1[i])-set(t2[i])) > 0:
            dict_2['-'] += [(i, list(set(t1[i])-set(t2[i])))]
            pass
        if len(set(t2[i])-set(t1[i])) > 0:
            dict_2['+'] += [(i, list(set(t2[i])-set(t1[i])))]
            pass
        pass
    pprint(dict_1)
    pprint(dict_2)
    # write type1 dict with json format
    with open(type_1_path, 'w') as f1:
        json.dump(dict_1, f1, indent = 4)
    # write type3 dict with json format
    with open(type_2_path, 'w') as f2:
        json.dump(dict_2, f2, indent = 4)
    with open(summary_path, 'w') as f3:
        f3.writelines(['type1:' + str(len(dict_1['+'] + dict_1['-']) > 0) + '\n',
                       'type2:' + str(len(dict_2['+'] + dict_2['-']) > 0) + '\n'])
    pass


if __name__ == '__main__':
    path1 = sys.argv[1]
    path2 = os.path.join(path1, 'pre.json')
    path3 = os.path.join(path1, 'curr.json')
    path4 = os.path.join(path1, 'type1.json')
    path5 = os.path.join(path1, 'type2.json')
    path6 = os.path.join(path1, 'summary.json')
    depends_diff(path1, path2, path3, path4, path5, path6)
    # depends_diff('C:\\Users\\cuidi34\\Desktop\\test',
    #              'C:\\Users\\cuidi34\\Desktop\\test\\pre.json',
    #              'C:\\Users\\cuidi34\\Desktop\\test\\curr.json',
    #              'C:\\Users\\cuidi34\\Desktop\\test\\type1.json',
    #              'C:\\Users\\cuidi34\\Desktop\\test\\type2.json',
    #              'C:\\Users\\cuidi34\\Desktop\\test\\summary.json')
    print 'cuidi'
