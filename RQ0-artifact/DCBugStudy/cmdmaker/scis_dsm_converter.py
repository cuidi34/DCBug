import json
from pprint import pprint


def relation_converter(name):
    relation_list = json_load_data('/home//Dropbox/ArchBugFix/round2-arch-relation/'+name+'.json')
    variable_list, header_list = header_and_variable_generator(relation_list)
    pprint(relation_list)
    pprint(header_list)
    matrix_list = matrix_generator(relation_list, variable_list, header_list)
    node = map(lambda x: x + '\n', variable_list)
    write_list = [head_to_str(header_list), str(len(variable_list))+'\n']+matrix_list+node
    write_path = '/home//Dropbox/ArchBugFix/round2-arch-dsm/'+name+'.dsm'
    with open(write_path, 'w') as f:
        f.writelines(write_list)
    pass


def header_and_variable_generator(relation_list):
    variable_list, header_list = [], []
    for relation in relation_list:
        variable_list.append(relation[0][0])
        variable_list.append(relation[0][1])
        for type_list in relation[1]:
            header_list.append(type_list[2])
    return list(set(variable_list)), list(set(header_list))
    pass


def matrix_generator(relation_list, variable_list, header_list):
    cell_dict = {}
    matrix_list = []
    for relation in relation_list:
        cell_dict[(variable_list.index(relation[0][0]),
                   variable_list.index(relation[0][1]))] = label_generator(relation[1], header_list)
    # generate matrix list
    for i in range(0, len(variable_list)):
        print i
        temp = ''
        for j in range(0, len(variable_list)):
            temp += cell_dict[(i, j)]+' ' if (i, j) in cell_dict else '0 '
        temp += '\n'
        matrix_list.append(temp)
    return matrix_list
    pass


def label_generator(target_list, header_list):
    target_list = map(lambda x: x[2], target_list)
    icon = ''
    for header in header_list:
        if header in target_list:
            icon += '1'
        else:
            icon += '0'
        pass
    return icon
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def head_to_str(header):
    if len(header) == 0:
        return ''
    else:
        temp = ''
        for h in header:
            temp += h+','
        return '['+temp.strip(',')+']'+'\n'
    pass


def collect_all_arch_dsm():
    project_list = ['pig', 'hadoop', 'cassandra', 'camel', 'cxf', 'openjpa', 'hbase', 'pdfbox']
    for project in project_list:
        relation_converter(project)
    print ''
    pass


if __name__ == '__main__':
    collect_all_arch_dsm()
    print ''
    pass
