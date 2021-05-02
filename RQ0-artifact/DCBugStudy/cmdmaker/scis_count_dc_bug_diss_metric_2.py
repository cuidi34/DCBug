import json
import os
from pprint import pprint


def collect_all_bug_fix_metric_2():
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        project_path = header_path + '/' + pro_path
        # load bug fix data
        bug_fix_path = '/home//Dropbox/ArchBugFix/commit-fixing-log-fse20/' + project_name + '/bug-fix.txt'
        bug_fix_data = json_load_data(bug_fix_path)
        # load arch bug data
        load_data = json_load_data(project_path)
        metric_list = []
        for item in load_data:
            bug_head = item[0][:item[0].index('-')]
            bug_id = item[0]
            print bug_id
            dl_value, pc_value = 0, 0
            if item[1]:
                for fix_cmt in bug_fix_data[bug_id]:
                    print fix_cmt
                    m1, m2 = calc_metric('/home//arch-fix-commit/' + project_name + '/' + fix_cmt)
                    dl_value += m1
                    pc_value += m2
            metric_list.append((bug_id, [dl_value, pc_value]))
        # write results
        with open('/home//Dropbox/ArchBugFix/arch-metric-issta/' + project_name + '.json', 'w') as f:
            json.dump(metric_list, f)
    pass


def count_all_bug_fix_metric_2():
    arch_head = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    metric_head = '/home//Dropbox/ArchBugFix/arch-metric-issta'
    issue_link_keyword = ['blocks', 'is depended upon by', 'requires', 'breaks', 'causes', 'blocked',
                          'contains', 'incorporates', 'is a parent of']
    metric_list = []
    for pro_path in os.listdir(arch_head):
        metric_path = metric_head + '/' + pro_path
        arch_path = arch_head + '/' + pro_path
        # load metric data
        metric_data = json_load_data(metric_path)
        metric_dict = {i: j for i, j in metric_data}
        # load transition data
        trans_path = '/home//Dropbox/ArchBugFix/bug-transition-issta/' + pro_path
        trans_data = json_load_data(trans_path)
        trans_dict = {}
        for bug_id, trans_list in trans_data.items():
            trans_dict[bug_id] = calc_reopen_times(trans_list)
        # load arch data
        arch_data = json_load_data(arch_path)
        for item in arch_data:
            bug_head = item[0][:item[0].index('-')]
            bug_id = item[0]
            print bug_id
            print metric_dict[bug_id]
            bug_item_path = '/home//bugID-fse20/' + bug_head + '/' + bug_id + '.txt'
            t = json_load_data(bug_item_path)
            print bug_id
            print item[1]
            is_induce = False
            for link_item in t['issue_link']:
                if link_item[1] in issue_link_keyword:
                    is_induce = True
                    break
            # 2 for reopen, 3 for induce
            metric_list.append((bug_id, metric_dict[bug_id], True if trans_dict[bug_id] > 1 else False, is_induce, item[1]))
            pass
    arch_dl_list = sorted(metric_list, key=lambda x: abs(x[1][0]), reverse=True)
    arch_pc_list = sorted(metric_list, key=lambda x: abs(x[1][1]), reverse=True)
    pprint(arch_dl_list)
    print 'dl list ... '
    for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        print 'top: ' + str(i)
        count_top_percentage(arch_dl_list, i)
    print 'pc list ... '
    for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        print 'top: ' + str(i)
        count_top_percentage(arch_pc_list, i)
    pass


def calc_reopen_times(trans_list):
    word_list = []
    for t in trans_list:
        word_list.append(t[0])
        word_list.append(t[1])
    return int(float(word_list.count('Reopened'))/2)
    pass


def count_top_percentage(item_list, percentage):
    target_list = item_list[:int(float(len(item_list)) * percentage)]
    total_num = float(len(target_list))
    # reopen
    reopen_num = len(filter(lambda x: x[2] and x[4], target_list))
    reopen_total_num = len(filter(lambda x: x[2], item_list))
    print 'reopen-R:' + str(float(reopen_num) / float(reopen_total_num)) + ',reopen-P:' + str(
        float(reopen_num) / float(total_num))
    # induce
    induce_num = len(filter(lambda x: x[3] and x[4], target_list))
    induce_total_num = len(filter(lambda x: x[3], item_list))
    print 'induce-R:' + str(float(induce_num) / float(induce_total_num)) + ',induce-P:' + str(
        float(induce_num) / float(total_num))
    pass


def calc_metric(path):
    if os.path.exists(path + '/pc-pre.json') and \
            os.path.exists(path + '/pc-curr.json') and \
            os.path.exists(path + '/dl-pre.json') and \
            os.path.exists(path + '/dl-curr.json'):
        dl_pre = json_load_data(path + '/dl-pre.json')['decouplingLevel']
        dl_curr = json_load_data(path + '/dl-curr.json')['decouplingLevel']
        pc_pre = json_load_data(path + '/pc-pre.json')['propagationCost']
        pc_curr = json_load_data(path + '/pc-curr.json')['propagationCost']
        dl_pre, dl_curr, pc_pre, pc_curr = format_transformer(dl_pre), format_transformer(dl_curr), \
                                           format_transformer(pc_pre), format_transformer(pc_curr)
        return dl_curr - dl_pre, pc_curr - pc_pre
    return 0, 0
    pass


def format_transformer(t):
    return float(t.replace('%', '')) / 100


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    # collect_all_bug_fix_metric_2()
    count_all_bug_fix_metric_2()
    print ''
