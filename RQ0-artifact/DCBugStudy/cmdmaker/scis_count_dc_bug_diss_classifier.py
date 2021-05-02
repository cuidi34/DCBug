from issta_count_arch_bug_rq2_bug_type import bug_type_classifier
from nltk.stem.porter import PorterStemmer
from pprint import pprint
import json
import sys


def load_ground_truth():
    data_set = []
    with open('issta-compare/issta-groundtruth.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            t = line.strip()
            label = t[:t.index(',')]
            description = t[t.index(',') + 1:] \
                .replace('"', '') \
                .replace('.', '') \
                .replace(':', '') \
                .replace('[', '') \
                .replace(']', '')
            data_set.append((label, description.split(' ')))
    return data_set


def calc_metric(data_set):
    # init stemmer
    porter_stemmer = PorterStemmer()
    type_dict = json_load_data('type/type.json')
    # iter each item
    target_list = []
    check_list = []
    for k, v in data_set:
        print k
        print v
        label = bug_type_classifier(porter_stemmer, v, type_dict)
        print label
        if k == 'not sure':
            continue
        target_list.append((k, label))
        check_list.append((k, v, label))
    with open('issta-compare/verify.txt', 'w') as f:
        for c in check_list:
            f.writelines(str(c[0] == c[2]) + ',' + c[0] + ',' + c[2] + '\n')
            f.writelines(str(c[1]) + '\n')
    calc_sub_set_metric('network-issue', target_list)
    calc_sub_set_metric('gui-issue', target_list)
    calc_sub_set_metric('database-issue', target_list)
    calc_sub_set_metric('permission-issue', target_list)
    calc_sub_set_metric('functional-issue', target_list)
    calc_sub_set_metric('configuration-issue', target_list)
    calc_sub_set_metric('test-issue', target_list)
    calc_sub_set_metric('performance-issue', target_list)
    calc_sub_set_metric('security-issue', target_list)
    calc_overall_metric(target_list)
    print len(target_list)
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def calc_sub_set_metric(bug_type, target_list):
    a_list = filter(lambda x: x[0] == bug_type, target_list)
    b_list = filter(lambda x: x[1] == bug_type, target_list)
    a_b_list = filter(lambda x: (x[0] == x[1]) and (x[0] == bug_type), target_list)
    precision = float(len(a_b_list)) / float(len(b_list))
    recall = float(len(a_b_list)) / float(len(a_list))
    f_measure = (2 * precision * recall) / (precision + recall)
    print bug_type + ': precision, ' + str(precision) + ', recall, ' + str(recall) + ', f1, ' + str(f_measure)
    pass


def calc_overall_metric(target_list):
    a_list = target_list
    b_list = target_list
    a_b_list = filter(lambda x: x[0] == x[1], target_list)
    precision = float(len(a_b_list)) / float(len(b_list))
    recall = float(len(a_b_list)) / float(len(a_list))
    f_measure = (2 * precision * recall) / (precision + recall)
    print 'overall: precision, ' + str(precision) + ', recall, ' + str(recall) + ', f1, ' + str(f_measure)
    pass


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    calc_metric(load_ground_truth())
    print ''
    pass
