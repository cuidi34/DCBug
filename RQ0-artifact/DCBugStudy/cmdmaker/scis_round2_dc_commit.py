import json
import os


def collect_arch_commits_unit(name):
    header_path = '/home//Dropbox/ArchBugFix/arch-bug-issta'
    project_path = header_path + '/' + name + '.json'
    # load bug fix data
    bug_fix_path = '/home//Dropbox/ArchBugFix/commit-fixing-log-fse20/' + name + '/bug-fix.txt'
    bug_fix_data = json_load_data(bug_fix_path)
    # load arch bug data
    load_data = json_load_data(project_path)
    commit_list = []
    for item in load_data:
        bug_id = item[0]
        print bug_id
        if item[1]:
            for fix_cmt in bug_fix_data[bug_id]:
                print fix_cmt
                cmt_path = '/home//arch-fix-commit/' + name + '/' + fix_cmt
                if os.path.exists(cmt_path) and os.path.exists(cmt_path + '/summary.json'):
                    with open(cmt_path + '/summary.json', 'r') as f:
                        lines = f.readlines()
                        if 'True' in lines[0] or 'True' in lines[1]:
                            commit_list.append(fix_cmt)
                    pass
    arch_cmt_path = '/home//Dropbox/ArchBugFix/round2-arch-commit/'+name+'.json'
    with open(arch_cmt_path, 'w') as f:
        json.dump(commit_list, f, indent=4)
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


def collect_all_arch_commits():
    project_list = ['pig', 'hadoop', 'cassandra', 'camel', 'cxf', 'openjpa', 'hbase', 'pdfbox']
    for project in project_list:
        collect_arch_commits_unit(project)
    print ''
    pass


if __name__ == '__main__':
    collect_all_arch_commits()
    print ''
    pass
