import json
import os
from pprint import pprint
from issta_tool_dep_diff import depends_diff


def collect_arch_commits_relation_unit(name):
    relation_dict = {}
    commit_list = json_load_data('/home/cuidi/Dropbox/ArchBugFix/round2-arch-commit/'+name+'.json')
    for commit_id in commit_list:
        print commit_id
        arch_cmt_path = '/home/cuidi/arch-fix-commit/' + name + '/' + commit_id
        if os.path.exists(arch_cmt_path) and os.path.exists(arch_cmt_path + '/summary.json'):
            # parse type1 data
            dict1, dict2 = depends_diff(arch_cmt_path, arch_cmt_path + '/pre.json', arch_cmt_path + '/curr.json')
            for add_relation in dict1['+']+dict2['+']:
                relation = add_relation[0]
                relation_type_list = add_relation[1]
                if relation not in relation_dict:
                    relation_dict[relation] = []
                # parse each relation type
                for relation_type in relation_type_list:
                    relation_dict[relation].append(('+', commit_id, relation_type))
                pass
            for del_relation in dict1['-']+dict2['-']:
                relation = del_relation[0]
                relation_type_list = del_relation[1]
                if relation not in relation_dict:
                    relation_dict[relation] = []
                # parse each relation type
                for relation_type in relation_type_list:
                    relation_dict[relation].append(('-', commit_id, relation_type))
                pass
    final_relation_dict = {}
    for k, v in relation_dict.items():
        print k
        temp = filter_relation(v)
        if len(temp) == 0:
            continue
        final_relation_dict[k] = temp
    pprint(final_relation_dict)
    with open('/home/cuidi/Dropbox/ArchBugFix/round2-arch-relation/'+name+'.json', 'w') as f:
        json.dump(final_relation_dict.items(), f, indent=4)
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def filter_relation(type_list):
    filter_type_list = []
    type_dict = {}
    for t in type_list:
        if t[2] not in type_dict:
            type_dict[t[2]] = []
        type_dict[t[2]].append(t)
        pass
    for k, v in type_dict.items():
        index = sum(map(lambda x: 1 if x[0] == '+' else -1, v))
        if index > 0:
            filter_type_list.append(v[-1])
    return filter_type_list
    pass


def collect_all_arch_commit_relations():
    project_list = ['pig', 'hadoop', 'cassandra', 'camel', 'cxf', 'openjpa', 'hbase', 'pdfbox']
    for project in project_list:
        collect_arch_commits_relation_unit(project)
    print 'cuidi'
    pass


if __name__ == '__main__':
    collect_all_arch_commit_relations()
    print 'cuidi'
    pass
