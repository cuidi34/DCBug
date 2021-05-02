from pprint import pprint
from operator import add

'''
calculate the minimal space coverage
'''


def bug_space_coverage(sub_dsm_list, coverage_list):
    # subdsmlist = fast_subdsm.get_subdsm(dsmpath, clxpath).items()
    target_list = set(coverage_list)
    final_space = []
    while len(target_list) > 0 and len(sub_dsm_list) > 0:
        mini_index = -1
        mini_value = 0
        mini_index_list = []
        for index, sub_dsm in enumerate(sub_dsm_list):
            coverage_metric = float(len(set(sub_dsm[1]) & target_list))/float(len(target_list))
            if coverage_metric > mini_value:
                mini_index = index
                mini_value = coverage_metric
                mini_index_list = [index]
                pass
            if coverage_metric == mini_value:
                mini_index_list.append(index)
            pass
        if len(mini_index_list) > 1:
            mini_temp_index = -1
            mini_temp_value = 1000000
            for temp_index in mini_index_list:
                if len(sub_dsm_list[temp_index][1]) < mini_temp_value:
                    mini_temp_index = temp_index
                    mini_temp_value = len(sub_dsm_list[temp_index][1])
                    pass
                pass
            mini_index = mini_temp_index
            pass
        # print subdsmlist
        # print mini_index
        final_result = sub_dsm_list.pop(mini_index)
        final_space.append(final_result)
        target_list = target_list-set(final_result[1])
        pass
    # pprint(len(final_space))
    contain_list = set(reduce(add, map(lambda x: x[1], final_space)))
    # print len(set(contain_list))
    # print float(len(coverage_list)) / float(len(contain_list))
    return float(len(final_space)) / float(len(coverage_list))
    pass


if __name__ == '__main__':
    print ''
