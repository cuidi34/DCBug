from pprint import pprint


def figure_count():
    with open('issta-figure/arch-rate.txt', 'r') as f:
        count_list = []
        lines = f.readlines()
        for line in lines:
            count_list.append(float(line.strip().replace('%', '')))
        print max(count_list)
        print min(count_list)
        print '<10%:' + str(len(filter(lambda x: x < 10, count_list)))
        print '<20% and >10%:' + str(len(filter(lambda x: 20 > x >= 10, count_list)))
        print '<30% and >20%:' + str(len(filter(lambda x: 30 > x >= 20, count_list)))
        print '<40% and >30%:' + str(len(filter(lambda x: 40 > x >= 30, count_list)))
        print '<50% and >40%:' + str(len(filter(lambda x: 50 > x >= 40, count_list)))
        print '<60% and >50%:' + str(len(filter(lambda x: 60 > x >= 50, count_list)))
        print '<70% and >60%:' + str(len(filter(lambda x: 70 > x >= 60, count_list)))
        print '<100% and >70%:' + str(len(filter(lambda x: 100 > x >= 70, count_list)))
    pass


if __name__ == '__main__':
    figure_count()
    pass
