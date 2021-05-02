import os
from pprint import pprint


def cmd_tag_converter(name):
    tag_list = []
    with open('tag/'+name+'-tag.txt') as f:
        lines = f.readlines()
        for line in lines:
            tag_line = line.strip()
            temp_tag = tag_line[:tag_line.index(',')]
            tag_list.append(temp_tag)
            # print temp_tag
            tag_path = '/home/cuidi/security-result/'+name+'/'+temp_tag
            if not os.path.exists(tag_path):
                os.mkdir(tag_path)
            print 'cd /home/cuidi/security-repo/'+name
            print 'git checkout '+temp_tag
            print '/home/cuidi/und/./undxml.sh /home/cuidi/security-repo/'+name+' /home/cuidi/security-result/'+name+'/' + temp_tag+' '+name

    pass


if __name__ == '__main__':
    cmd_tag_converter('curl')
    # print 'cuidi'