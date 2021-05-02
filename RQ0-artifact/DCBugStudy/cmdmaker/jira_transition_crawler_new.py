#-*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
import sys


def transition_collector(url):
	transition_list_all = []
	p = pq(url=url)
	scripts = p('script').items()
	for script in scripts:
		script_text = script.text()
		if 'issuePanelContainer' in script_text:
			start=script_text.find('\\\\/span&gt;\\\\\\\"\u003e')
			flag=0
			transition_list = []
			while start != -1:
				start_time=script_text.find('\u003ctd width=\\\\\\\"20%\\\\\\\"\u003e\\\\n\\\\t\\\\t\\\\t',start)
				end = script_text.find('\u003c\\\\/span', start)
				end_time = script_text.find('\\\\n', start_time+44)
				transition_list.append(script_text[start+21:end])
				# print(script_text[start+21:end])
				flag += 1
				if flag % 2 == 0:
					transition_list.append(script_text[start_time+44:end_time].strip())
					# print(script_text[start_time+44:end_time])
					transition_list_all.append(transition_list)
					transition_list = []
				start = script_text.find('\\\\/span&gt;\\\\\\\"\u003e',start+1)
				start_time = script_text.find('\u003ctd width=\\\\\\\"20%\\\\\\\"\u003e\\\\n\\\\t\\\\t\\\\t',start_time+1)
	return transition_list_all


if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	left_url = 'https://issues.apache.org/jira/browse/'
	right_url = '?page=com.googlecode.jira-suite-utilities%3Atransitions-summary-tabpanel'
	url = left_url+'AMQ-2659'+right_url
	print transition_collector(url)
	url = left_url+'ACCUMULO-3217'+right_url
	print transition_collector(url)
	pass

