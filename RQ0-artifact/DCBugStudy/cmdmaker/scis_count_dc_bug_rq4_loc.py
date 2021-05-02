import json
import os
from pprint import pprint

'''
studying the spent lines of code is enough!
'''


def iter_bug_fix():
    path = '/home//Dropbox/ArchBugFix/commit-fixing-log-fse20'
    for project_name in os.listdir(path):
        issue_index_list = iter_bug_fix_one_project(path, project_name)
        pprint(issue_index_list)
        with open('/home//Dropbox/ArchBugFix/bug-loc-issta/' + project_name + '.json', 'w') as f:
            json.dump(issue_index_list, f)


def iter_bug_fix_one_project(header, project):
    # load log data
    log_path = '/home//Dropbox/ArchBugFix/commit-log-fse20/' + project + '.log'
    log_data = json_load_bug_info(log_path)
    cmt_dict = {}
    for cmt_data in log_data:
        cmt_dict[cmt_data['commit']] = cmt_data
        pass
    issue_index_list = []
    with open(header + '/' + project + '/bug-fix.txt', 'r') as f:
        data = json.load(f)
        for issue_id, cmt_list in data.items():
            print issue_id
            issue_loc = 0
            for cmt in cmt_list:
                for change in cmt_dict[cmt]['changes']:
                    if change[2].endswith('.java') and isinstance(change[0], int) and isinstance(change[1], int):
                        print change
                        issue_loc += change[0]
                        issue_loc += change[1]
                        pass
            issue_index_list.append((issue_id, issue_loc))
    return issue_index_list
    pass


'''
count all bug fix
'''


def count_all_bug_fix_loc():
    arch_head = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    loc_head = '/home//Dropbox/ArchBugFix/bug-loc-issta'
    loc_list = []
    for pro_path in os.listdir(arch_head):
        loc_path = loc_head + '/' + pro_path
        arch_path = arch_head + '/' + pro_path
        # load loc data
        loc_data = json_load_data(loc_path)
        loc_dict = {i: j for i, j in loc_data}
        # load bug type data and store in global dict
        bug_type_data = json_load_data('/home//Dropbox/ArchBugFix/bug-type-issta/' + pro_path)
        bug_type_dict = {i[0]: i[1] for i in bug_type_data}
        # load arch data
        arch_data = json_load_data(arch_path)
        for item in arch_data:
            bug_id = item[0]
            print bug_id
            print loc_dict[bug_id]
            loc_list.append((bug_id, item[1], loc_dict[bug_id], bug_type_dict[bug_id]))
            pass
    # sort and count
    arch_loc_list = sorted(loc_list, key=lambda x: x[2], reverse=True)
    pprint(arch_loc_list)
    for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        print 'top: ' + str(i)
        count_top_percentage(arch_loc_list, i)
    # calculate average
    # use 0.2-1
    count_average_effort(arch_loc_list[int(float(len(arch_loc_list)) * 0.1):])
    pass


'''
add the interaction of each type
'''


def count_top_percentage(item_list, percentage):
    target_list = item_list[:int(float(len(item_list)) * percentage)]
    total_num = float(len(target_list))
    # arch
    arch_num = len(filter(lambda x: x[1], target_list))
    arch_total_num = len(filter(lambda x: x[1], item_list))
    print 'arch-P:' + str(float(arch_num) / float(arch_total_num)) + ',arch-R:' + str(
        float(arch_num) / float(total_num))
    # configuration-issue
    count_top_type('configuration-issue', target_list, item_list, total_num)
    # network-issue
    count_top_type('network-issue', target_list, item_list, total_num)
    # database
    count_top_type('database-issue', target_list, item_list, total_num)
    # gui
    count_top_type('gui-issue', target_list, item_list, total_num)
    # performance
    count_top_type('performance-issue', target_list, item_list, total_num)
    # permission
    count_top_type('permission-issue', target_list, item_list, total_num)
    # security
    count_top_type('security-issue', target_list, item_list, total_num)
    # functional
    count_top_type('functional-issue', target_list, item_list, total_num)
    # test
    count_top_type('test-issue', target_list, item_list, total_num)
    # not sure
    count_top_type('not sure', target_list, item_list, total_num)
    pass


def count_top_type(bug_type, target_list, item_list, total_num):
    config_num = len(filter(lambda x: x[3] == bug_type, target_list))
    config_total_num = len(filter(lambda x: x[3] == bug_type, item_list))
    print bug_type + '-P:' + str(float(config_num) / float(config_total_num)) + \
          ', ' + bug_type + '-R:' + str(float(config_num) / float(total_num))
    pass


'''
count average effort
'''


def count_average_effort(rank_list):
    # count arch
    print 'average value:'
    arch_list = filter(lambda x: x[1], rank_list)
    non_arch_list = filter(lambda x: not x[1], rank_list)
    print 'arch-average:' + str(float(sum(map(lambda x: x[2], arch_list))) / float(len(arch_list))) \
          + ', non-arch-average:' + str(float(sum(map(lambda x: x[2], non_arch_list))) / float(len(non_arch_list)))
    # configuration-issue
    count_average_type('configuration-issue', rank_list)
    # network-issue
    count_average_type('network-issue', rank_list)
    # database
    count_average_type('database-issue', rank_list)
    # gui
    count_average_type('gui-issue', rank_list)
    # performance
    count_average_type('performance-issue', rank_list)
    # permission
    count_average_type('permission-issue', rank_list)
    # security
    count_average_type('security-issue', rank_list)
    # functional
    count_average_type('functional-issue', rank_list)
    # test
    count_average_type('test-issue', rank_list)
    # not sure
    count_average_type('not sure', rank_list)
    pass


def count_average_type(bug_type, rank_list):
    arch_list = filter(lambda x: x[3] == bug_type, rank_list)
    non_arch_list = filter(lambda x: x[3] != bug_type, rank_list)
    print bug_type + '-average:' + str(float(sum(map(lambda x: x[2], arch_list))) / float(len(arch_list))) + ', non-' + \
          bug_type + '-average:' + str(float(sum(map(lambda x: x[2], non_arch_list))) / float(len(non_arch_list)))
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def json_load_bug_info(path):
    with open(path, 'r') as f:
        return json.loads(f.readline().decode("utf-8", "ignore"))
    pass


if __name__ == '__main__':
    count_all_bug_fix_loc()
    print ''
