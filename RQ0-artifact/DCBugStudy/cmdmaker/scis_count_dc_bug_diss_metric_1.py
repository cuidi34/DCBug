import json
import os
from pprint import pprint
from issta_tool_dep_diff import depends_diff

'''
data collection
'''


def collect_all_bug_fix_metric():
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        project_path = header_path + '/' + pro_path
        # load bug fix data
        bug_fix_path = '/home//Dropbox/ArchBugFix/commit-fixing-log-fse20/'+project_name+'/bug-fix.txt'
        bug_fix_data = json_load_data(bug_fix_path)
        # load arch bug data
        cmd_list = []
        load_data = json_load_data(project_path)
        for item in load_data:
            bug_head = item[0][:item[0].index('-')]
            bug_id = item[0]
            print bug_id
            if item[1]:
                for fix_cmt in bug_fix_data[bug_id]:
                    print fix_cmt
                    cmt_path = '/home//arch-fix-commit/'+project_name+'/'+fix_cmt
                    if os.path.exists(cmt_path):
                        cmd_list.append('echo '+fix_cmt+'\n')
                        # convert pre
                        convert_pre_cmd = './dv8-console core:convert-matrix -dependPath '+cmt_path + '/depends' \
                                                                                                      '-dv8map.json ' \
                                                                                                      '-outputFile ' \
                                          + cmt_path + '/pre.dv8-dsm ' + cmt_path + '/pre.json '
                        print convert_pre_cmd
                        cmd_list.append(convert_pre_cmd+'\n')
                        # convert curr
                        convert_curr_cmd = './dv8-console core:convert-matrix -dependPath '+cmt_path + '/depends' \
                                                                                                       '-dv8map.json ' \
                                                                                                       '-outputFile '\
                                           + cmt_path + '/curr.dv8-dsm ' + cmt_path + '/curr.json '
                        print convert_curr_cmd
                        cmd_list.append(convert_curr_cmd+'\n')
                        # dl pre
                        dl_metric_pre_cmd = './dv8-console metrics:decoupling-level -outputFile '\
                                            + cmt_path+'/dl-pre.json '+cmt_path+'/pre.dv8-dsm'
                        print dl_metric_pre_cmd
                        cmd_list.append(dl_metric_pre_cmd+'\n')
                        # dl curr
                        dl_metric_curr_cmd = './dv8-console metrics:decoupling-level -outputFile ' \
                                             + cmt_path + '/dl-curr.json ' + cmt_path + '/curr.dv8-dsm'
                        print dl_metric_curr_cmd
                        cmd_list.append(dl_metric_curr_cmd+'\n')
                        # pc pre
                        pc_metric_pre_cmd = './dv8-console metrics:propagation-cost -outputFile '\
                                            + cmt_path+'/pc-pre.json '+cmt_path+'/pre.dv8-dsm'
                        print pc_metric_pre_cmd
                        cmd_list.append(pc_metric_pre_cmd+'\n')
                        # pc curr
                        pc_metric_curr_cmd = './dv8-console metrics:propagation-cost -outputFile ' \
                                             + cmt_path+'/pc-curr.json '+cmt_path+'/curr.dv8-dsm'
                        print pc_metric_curr_cmd
                        cmd_list.append(pc_metric_curr_cmd+'\n')
        with open('issta-cmd/'+project_name+'.sh', 'w') as f:
            f.writelines(cmd_list)
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    collect_all_bug_fix_metric()
    print ''