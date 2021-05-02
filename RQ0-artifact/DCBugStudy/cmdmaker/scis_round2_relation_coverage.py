import json
from pprint import pprint


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def extract_target_relation(name):
    relation_dict = {}
    relation_list = json_load_data('C:\\Users\\Administrator\\Dropbox\\ArchBugFix\\round2-arch-relation\\' + name + '.json')
    for relation in relation_list:
        relation_dict[(relation[0][0], relation[0][1])] = list(set(map(lambda x: x[1], relation[1])))
    return relation_dict.keys()
    pass


def extract_all_relation(name):
    all_relation_data = json_load_data('C:\\Users\\Administrator\\Dropbox\\ArchBugFix\\round2-all-relation\\'+name+'.json')
    file_list = map(lambda x: x.replace('C:\\Users\\Administrator\\Desktop\\cuidi\\'+name+'\\', '').replace('\\', '/'),
                    all_relation_data['variables'])
    relation_list = []
    for cell in all_relation_data['cells']:
        relation_list.append((file_list[cell['src']], file_list[cell['dest']]))
    return relation_list
    pass


def extract_bug_relation(name):
    all_list = extract_all_relation(name)
    buggy_file_list = json_load_data('C:\\Users\\Administrator\\Dropbox\\ArchBugFix\\round2-file-proneness\\'+name+'.json')
    buggy_file_list = set(map(lambda x: x[0], buggy_file_list))
    # pprint(buggy_file_list)
    bug_list = filter(lambda x: x[0] in buggy_file_list and x[1] in buggy_file_list, all_list)
    return bug_list
    pass


def calc_relation_coverage(name):
    all_list = extract_all_relation(name)
    target_list = extract_target_relation(name)
    bug_list = extract_bug_relation(name)
    t1 = float(len(set(target_list) & set(all_list)))/float(len(all_list))
    t2 = float(len(set(target_list) & set(bug_list)))/float(len(bug_list))
    print name+','+str(t1)+','+str(t2)
    pass


if __name__ == '__main__':
    # extract_bug_relation('camel')
    calc_relation_coverage('pig')
    calc_relation_coverage('hadoop')
    calc_relation_coverage('cassandra')
    calc_relation_coverage('camel')
    calc_relation_coverage('cxf')
    calc_relation_coverage('openjpa')
    calc_relation_coverage('hbase')
    calc_relation_coverage('pdfbox')
    print 'cuidi'