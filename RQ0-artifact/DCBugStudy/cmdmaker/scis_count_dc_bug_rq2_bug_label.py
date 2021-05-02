import os
import json
from pprint import pprint
from jira.client import JIRA


def collect_all_bug_fix_label():
    # build connection
    header_path = '/home/cuidi/Dropbox/ArchBugFix/arch-bug-issta'
    options = {
        'server': 'https://issues.apache.org/jira/'
    }
    jira = JIRA(options)
    # iter each report
    for pro_path in os.listdir(header_path):
        if os.path.exists('/home/cuidi/Dropbox/ArchBugFix/arch-label-issta/'+pro_path):
            continue
        label_list = []
        project_path = header_path + '/' + pro_path
        load_data = json_load_data(project_path)
        for item in load_data:
            bug_id = item[0]
            print bug_id
            issue = jira.issue(bug_id)
            label_list.append((bug_id, issue.fields.labels))
        with open('/home/cuidi/Dropbox/ArchBugFix/arch-label-issta/'+pro_path, 'w') as f:
            json.dump(label_list, f)
            pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    collect_all_bug_fix_label()
    print 'cuidi'