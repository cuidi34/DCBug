import os
from pprint import pprint
from core_fast_subdsm import get_sub_dsm
import json


def clustering_cmd_generator():
    header = '/home/cuidi/Dropbox/ArchBugFix/round2-arch-dsm'
    for project in os.listdir(header):
        print 'java -jar archdrh-fast-jdk1.6.jar -c -inDsm '+header+'/'+project+' -outClsx '+header+'/'+project.replace('.dsm', '.clsx')
    pass


def pattern_finder(name):
    minos_header = '/home/cuidi/Dropbox/ArchBugFix/round2-arch-dsm'
    minos_dsm_path = minos_header + '/' + name + '.dsm'
    minos_drh_path = minos_header + '/' + name + '.clsx'
    # store relation dict
    relation_dict = {}
    relation_list = json_load_data('/home/cuidi/Dropbox/ArchBugFix/round2-arch-relation/'+name+'.json')
    for relation in relation_list:
        relation_dict[(relation[0][0], relation[0][1])] = list(set(map(lambda x: x[1], relation[1])))
    # get sub dsm and find pattern
    sub_dsm_dict = get_sub_dsm(minos_dsm_path, minos_drh_path)
    lambda_pattern, wilson_pattern, domino_pattern = {}, {}, {}
    reversed_dict = {}
    # collect lambda pattern
    for lead_file, sub_file_list in sub_dsm_dict.items():
        sub_file_list.remove(lead_file)
        # prepare lambda
        if len(sub_file_list) > 1:
            commit_list, sub_list = [], []
            for sub_file in sub_file_list:
                if (sub_file, lead_file) in relation_dict:
                    commit_list += relation_dict[(sub_file, lead_file)]
                    sub_list.append(sub_file)
                pass
            commit_list = list(set(commit_list))
            # write lambda pattern
            if len(commit_list) > 1:
                print commit_list
                print sub_list
                lambda_pattern[lead_file] = [sub_list, commit_list]
        # prepare reverse dict
        for sf in sub_file_list:
            if (sf, lead_file) in relation_dict:
                if sf not in reversed_dict:
                    reversed_dict[sf] = []
                reversed_dict[sf].append(lead_file)
    # collect wilson pattern
    for lead_file, sub_file_list in reversed_dict.items():
        print lead_file
        print sub_file_list
        if len(sub_file_list) > 1:
            commit_list = []
            for sub_file in sub_file_list:
                commit_list += relation_dict[(lead_file, sub_file)]
            commit_list = list(set(commit_list))
            if len(commit_list) > 1:
                wilson_pattern[lead_file] = [sub_file_list, commit_list]
    # collect domino pattern: we have removed lead file in subspaces
    for begin_file, middle_file_list in sub_dsm_dict.items():
        for middle_file in middle_file_list:
            if (middle_file, begin_file) in relation_dict:
                print middle_file
                for end_file in sub_dsm_dict[middle_file]:
                    if (end_file, middle_file) in relation_dict:
                        commit_list = list(set(relation_dict[(middle_file, begin_file)] +
                                               relation_dict[(end_file, middle_file)]))
                        if len(commit_list) > 1:
                            domino_pattern[(begin_file, middle_file, end_file)] = commit_list
                        pass
    # re-organize domino pattern with middle file
    domino_pattern_dict = {}
    for dp in domino_pattern.keys():
        print dp
        if dp[1] not in domino_pattern_dict:
            domino_pattern_dict[dp[1]] = []
        domino_pattern_dict[dp[1]].append((dp, domino_pattern[dp]))
        pass
    domino_pattern = domino_pattern_dict.items()
    pprint(domino_pattern)
    pprint(len(domino_pattern))
    # write three types of pattern
    with open('/home/cuidi/Dropbox/ArchBugFix/round2-pattern-finder/'+name+'-l.json', 'w') as f1:
        json.dump(lambda_pattern, f1, indent=4)
    with open('/home/cuidi/Dropbox/ArchBugFix/round2-pattern-finder/'+name+'-w.json', 'w') as f2:
        json.dump(wilson_pattern, f2, indent=4)
    with open('/home/cuidi/Dropbox/ArchBugFix/round2-pattern-finder/'+name+'-d.json', 'w') as f3:
        json.dump(domino_pattern, f3, indent=4)
    pass


def merge_two_element(a, b):
    print a
    print b
    if a[0][0] == b[0][-2] and a[0][1] == b[0][-1]:
        file_seq = tuple(list(b[0])+list(a[0])[2:])
        commit_list = list(set(a[1]+b[1]))
        print (file_seq, commit_list)
        return file_seq, commit_list
        pass
    if a[0][-2] == b[0][0] and a[0][-1] == b[0][1]:
        file_seq = tuple(list(a[0]) + list(b[0])[2:])
        commit_list = list(set(a[1] + b[1]))
        print (file_seq, commit_list)
        return file_seq, commit_list
        pass
    return None
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)
    pass


def collect_all_pattern_data():
    project_list = ['pig', 'hadoop', 'cassandra', 'camel', 'cxf', 'openjpa', 'hbase', 'pdfbox']
    for project in project_list:
        print project
        pattern_finder(project)
    pass


if __name__ == '__main__':
    # collect_all_pattern_data()
    pattern_finder('pig')
    print 'cuidi'
    pass
