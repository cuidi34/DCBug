"""
Create on july 9,2017

@function: fast get the sub dsm of the drh
"""

import xml.etree.ElementTree as ET
from collections import OrderedDict
from pprint import pprint
from operator import add
import numpy as np
import re
import zlib


'''
fast get all the drspace of the design rule

'''


def get_drh_sub_dsm(drh_path):
    tree = ET.parse(drh_path)
    root = tree.getroot()
    '''
    store the drh with sim-hash-table
    '''
    counter = 0
    drh_dict = OrderedDict()
    for index, neighbor in enumerate(root.iter('group')):
        '''
        segment the layer
        '''
        if neighbor.attrib['name'] == 'L'+str(counter):
            counter += 1
            pass
        '''
        segment the cluster
        '''
        if neighbor[0].tag == 'item':
            cluster_list = [child.attrib['name'] for child in neighbor]
            cluster_item = {'value': cluster_list,
                            'layer': counter,
                            'type': neighbor.attrib['name']}
            for item in cluster_list:
                drh_dict[item] = cluster_item
    return drh_dict
    pass


'''
core step: get subdsm from drh and dsm
'''


def get_sub_dsm(dsm_path, drh_path):
    drh_dict = get_drh_sub_dsm(drh_path)
    with open(dsm_path, 'r') as f:
        lines = f.readlines()
        length = int(lines[1].strip())
        design_relations = lines[2:length+2]
        design_entities = lines[length+2:]
    design_relations = np.array(map(lambda x: map(lambda y: 0 if len(y) == 1 else 1, x.strip().split(' ')),
                                    design_relations))
    design_entities = map(lambda x: x.strip(), design_entities)
    # iterate each entity and find their sub dsm group
    sub_dsm_dict={}
    for index, entity in enumerate(design_entities):
        temp_list = np.where(design_relations[:, index] == 1)[0]
        neighbor_list = [design_entities[temp] for temp in temp_list]
        # print neighbor_list
        # reduce(,,the last) the last is the initial value
        sub_dsm_list = reduce(add, map(lambda x: drh_dict[x]['value'] if drh_dict[x]['type'] == 'M0' else [x],
                                       neighbor_list+[entity]), [])
        # remove the replicated element
        sub_dsm_list = {}.fromkeys(sub_dsm_list).keys()
        # supplying the sub_dsm into the dict
        sub_dsm_dict[entity] = sub_dsm_list
    return sub_dsm_dict
    pass


if __name__ == '__main__':
    t = get_sub_dsm('/home//Dropbox/BugGraph/dsm-minos-icpc/cxf.dsm',
                    '/home//Dropbox/BugGraph/dsm-minos-icpc/cxf.clsx')
    pprint(t)
    pprint(t.values())
    print 'testing '
    pass
