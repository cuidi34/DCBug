from jira.client import JIRA
from pprint import pprint
from pyquery import PyQuery as pq
import urllib2
import time


def jira_label_collector(bugID):
    options = {
        'server': 'https://issues.apache.org/jira/'
    }
    jira = JIRA(options)
    issue = jira.issue(bugID)
    return issue.fields.labels


if __name__ == '__main__':
    jira_label_collector('AMQ-6424')
    # test_jira_crawl_transition('AMQ-2659')
    print 'cuidi'