import json
import os
from pprint import pprint
import datetime

'''
extend to multiple label
'''


def count_all_bug_fix_time():
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    time_list = []
    for pro_path in os.listdir(header_path):
        project_path = header_path + '/' + pro_path
        load_data = json_load_data(project_path)
        # load bug type data and store in global dict
        bug_type_data = json_load_data('/home//Dropbox/ArchBugFix/bug-type-issta/' + pro_path)
        bug_type_dict = {i[0]: i[1] for i in bug_type_data}
        # iter item
        for item in load_data:
            bug_head = item[0][:item[0].index('-')]
            bug_id = item[0]
            bug_item_path = '/home//bugID-fse20/' + bug_head + '/' + bug_id + '.txt'
            t = json_load_data(bug_item_path)
            print bug_id
            print 'create time:'
            create_date = date_time_collector(t['create_date'])
            print create_date
            print 'resolution time:'
            resolution_date = date_time_collector(t['resolution_date'])
            print resolution_date
            interval = resolution_date - create_date
            print interval.days
            print interval.seconds
            print interval.total_seconds()
            print (bug_id, item[1], interval.total_seconds(), interval.days, interval.seconds)
            time_list.append(
                (bug_id, item[1], interval.total_seconds(), interval.days, interval.seconds, bug_type_dict[bug_id]))
    # sort and count
    bug_time_list = sorted(time_list, key=lambda x: x[2], reverse=True)
    pprint(bug_time_list)
    for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        print i
        count_top_percentage(bug_time_list, i)
    # calculate average
    count_average_effort(bug_time_list)
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
    config_num = len(filter(lambda x: x[5] == bug_type, target_list))
    config_total_num = len(filter(lambda x: x[5] == bug_type, item_list))
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
          + ',' + seconds_converter(int(float(sum(map(lambda x: x[2], arch_list))) / float(len(arch_list)))) \
          + ', non-arch-average:' + str(float(sum(map(lambda x: x[2], non_arch_list))) / float(len(non_arch_list))) \
          + ',' + seconds_converter(int(float(sum(map(lambda x: x[2], non_arch_list))) / float(len(non_arch_list))))
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
    arch_list = filter(lambda x: x[5] == bug_type, rank_list)
    non_arch_list = filter(lambda x: x[5] != bug_type, rank_list)
    print bug_type + '-average:' + str(float(sum(map(lambda x: x[2], arch_list))) / float(len(arch_list))) \
          + ',' + seconds_converter(int(float(sum(map(lambda x: x[2], arch_list))) / float(len(arch_list)))) \
          + ', non-' + bug_type + '-average:' + str(float(sum(map(lambda x: x[2], non_arch_list))) / float(len(non_arch_list))) \
          + ',' + seconds_converter(int(float(sum(map(lambda x: x[2], non_arch_list))) / float(len(non_arch_list))))
    pass


def date_time_collector(temp):
    print temp
    t_year = temp[:temp.index('-')]
    t_month = temp[temp.index('-') + 1:temp.rindex('-')]
    t_day = temp[temp.rindex('-') + 1:temp.index('T')]
    t_hour = temp[temp.index('T') + 1:temp.index(':')]
    t_minute = temp[temp.index(':') + 1:temp.rindex(':')]
    t_second = temp[temp.rindex(':') + 1:temp.index('.')]
    return datetime.datetime(int(t_year), int(t_month), int(t_day),
                             int(t_hour), int(t_minute), int(t_second))
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def seconds_converter(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return "%02d:%02d:%02d:%02d" % (d, h, m, s)
    pass


if __name__ == '__main__':
    count_all_bug_fix_time()
    print ''
