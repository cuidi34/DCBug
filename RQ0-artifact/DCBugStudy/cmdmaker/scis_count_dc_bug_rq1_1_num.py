import json
import os
from pprint import pprint
from issta_tool_dep_diff import depends_diff

'''
data collection
'''


def count_all_arch_fix():
    header_path = '/home/cuidi/Dropbox/ArchBugFix/arch-bug-issta'
    count = 0
    for pro_path in os.listdir(header_path):
        project_name = pro_path.replace('.json', '')
        project_path = header_path + '/' + pro_path
        # load bug fix data
        bug_fix_path = '/home/cuidi/Dropbox/ArchBugFix/commit-fixing-log-fse20/'+project_name+'/bug-fix.txt'
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
                    cmt_path = '/home/cuidi/arch-fix-commit/'+project_name+'/'+fix_cmt
                    if os.path.exists(cmt_path) and os.path.exists(cmt_path+'/summary.json'):
                        with open(cmt_path+'/summary.json', 'r') as f:
                            lines = f.readlines()
                            if 'True' in lines[0] or 'True' in lines[1]:
                                count += 1
                                print count
                        pass
    print count
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    count_all_arch_fix()
    print 'cuidi'
    pass
