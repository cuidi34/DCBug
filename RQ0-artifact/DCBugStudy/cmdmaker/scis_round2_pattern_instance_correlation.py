import json
from pprint import pprint
import csv


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)
    pass


def file_pattern_agglomeration(name):
    l_pattern = json_load_data('C:\\Users\\Administrator\\Dropbox\\ArchBugFix\\round2-pattern-finder\\'+name+'-l.json')
    w_pattern = json_load_data('C:\\Users\\Administrator\\Dropbox\\ArchBugFix\\round2-pattern-finder\\'+name+'-w.json')
    d_pattern = json_load_data('C:\\Users\\Administrator\\Dropbox\\ArchBugFix\\round2-pattern-finder\\'+name+'-d.json')
    pattern_dict = {}
    # lambda pattern
    for k, v in l_pattern.items():
        for f in [k]+v[0]:
            # print f
            pattern_dict[f] = pattern_dict[f]+1 if f in pattern_dict else 1
    # wilson pattern
    for k, v in w_pattern.items():
        for f in [k]+v[0]:
            # print f
            pattern_dict[f] = pattern_dict[f]+1 if f in pattern_dict else 1
    # domino pattern
    for k, v in d_pattern:
        for f in v[0][0]:
            # print f
            pattern_dict[f] = pattern_dict[f] + 1 if f in pattern_dict else 1
    pprint(pattern_dict)
    error_file_list = json_load_data('C:\\Users\\Administrator\\Dropbox\\ArchBugFix\\round2-file-proneness\\'+name+'.json')
    for q in error_file_list:
        print q[0]
        print q[1]
        print q[2]
        if q[0] in pattern_dict:
            pattern_dict[q[0]] = [pattern_dict[q[0]], q[1], q[2]]
            pass
        else:
            pattern_dict[q[0]] = [0, q[1], q[2]]
            pass
    pprint(pattern_dict)
    write_list = []
    for k, v in pattern_dict.items():
        if type(v) == list:
            write_list.append([k]+v)
    with open('file-pattern/'+name+'.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, lineterminator='\n')
        csv_writer.writerows(write_list)
    pass


if __name__ == '__main__':
    file_pattern_agglomeration('pig')
    file_pattern_agglomeration('hadoop')
    file_pattern_agglomeration('cassandra')
    file_pattern_agglomeration('camel')
    file_pattern_agglomeration('cxf')
    file_pattern_agglomeration('openjpa')
    file_pattern_agglomeration('hbase')
    file_pattern_agglomeration('pdfbox')
    print 'cuidi'