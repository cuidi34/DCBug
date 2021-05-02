import json
from pprint import pprint


def collect_file_error_proneness(name):
    file_dict = {}
    # load commit list
    commit_list = json_load_data('/home/cuidi/Dropbox/ArchBugFix/commit-fixing-log-fse20/'+name+'/commit-fix.txt')
    commit_list = commit_list.keys()
    # load commit log
    commit_log_dict = json_load_data('/home/cuidi/Dropbox/ArchBugFix/commit-log-fse20/'+name+'.log')
    commit_log_dict = {i['commit']: i['changes'] for i in commit_log_dict}
    # generate file list
    for commit in commit_list:
        print commit
        for change in commit_log_dict[commit]:
            file_name = change[2]
            if file_name.endswith('.java') and '=>' not in file_name:
                churn = int(change[0])+int(change[1])
                if file_name not in file_dict:
                    file_dict[file_name] = [0, 0]
                file_dict[file_name] = [file_dict[file_name][0]+1, file_dict[file_name][1]+churn]
    pprint(file_dict)
    write_list = [(str(i), j[0], j[1]) for i, j in file_dict.items()]
    pprint(write_list)
    with open('/home/cuidi/Dropbox/ArchBugFix/round2-file-proneness/'+name+'.json', 'w') as f:
        json.dump(write_list, f, indent=4)
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


'''
determine projects: hadoop, cassandra, camel, cxf, openjpa, hbase, pdfbox, pig 
'''


def collect_all():
    project_list = ['pig', 'hadoop', 'cassandra', 'camel', 'cxf', 'openjpa', 'hbase', 'pdfbox']
    for project in project_list:
        collect_file_error_proneness(project)
    print 'cuidi'
    pass


if __name__ == '__main__':
    collect_all()
    pass
