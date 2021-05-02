from nong_transition_crawler_new import transition_collector
import os
import json
import sys
from pprint import pprint


def crawl_framework_from_file(file_path):
    header_path = '/home/cuidi/Dropbox/ArchBugFix/arch-bug-issta'
    pro_path_list = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            pro_path_list.append(line.strip())
    for pro_path in pro_path_list:
        transition_dict = {}
        # get project name
        project_path = header_path + '/' + pro_path
        print project_path
        load_data = json_load_data(project_path)
        for bug_id, arch_index in load_data:
            print bug_id
            transition_dict[bug_id] = crawl_transition_unit(bug_id)
        with open('/home/cuidi/Dropbox/ArchBugFix/bug-transition-issta/' + pro_path, 'w') as f:
            json.dump(transition_dict, f, indent=4)
        pass
    pass


def crawl_framework():
    header_path = '/home/cuidi/Dropbox/ArchBugFix/arch-bug-issta'
    for pro_path in os.listdir(header_path):
        transition_dict = {}
        # get project name
        project_path = header_path + '\\' + pro_path
        print project_path
        load_data = json_load_data(project_path)
        for bug_id, arch_index in load_data:
            print bug_id
            transition_dict[bug_id] = crawl_transition_unit(bug_id)
        with open('/home/cuidi/Dropbox/ArchBugFix/bug-transition-issta/'+pro_path, 'w') as f:
            json.dump(transition_dict, f, indent= 4)
        pass
    pass


def crawl_transition_unit(bug_id):
    left_url = 'https://issues.apache.org/jira/browse/'
    right_url = '?page=com.googlecode.jira-suite-utilities%3Atransitions-summary-tabpanel'
    url = left_url + bug_id + right_url
    return transition_collector(url)
    pass


def json_load_data(path):
    with open(path, 'r') as f:
        return json.load(f)
    pass


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    crawl_framework_from_file('trans/project2.txt')
    print 'cuidi'