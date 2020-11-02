from download import DataDownloader
from matplotlib import pyplot as plt
import os
import argparse

def create_ax(axs, i, keys, values, year):
    rects = axs[i].bar(keys, values)
    axs[i].set_title(year)
    add_order_to_axs(axs[i], rects)

def add_order_to_axs(axs, rects):
    i = 1
    for rect in rects:
        height = rect.get_height()
        axs.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                i,#'%d' % int(height),
                ha='center', va='bottom')
        i += 1

def plot_stat(data_source, fig_location = None, show_figure = False):
    data_source = data_source[1]
    data2016 = {}
    data2017 = {}
    data2018 = {}
    data2019 = {}
    data2020 = {}

    for i in range(len(data_source[0])):
        if data_source[3][i][:4] == '2016':
            if data_source[64][i] in data2016.keys():
                data2016[data_source[64][i]] += 1
            else:
                data2016[data_source[64][i]] = 1

        elif data_source[3][i][:4] == '2017':
            if data_source[64][i] in data2017.keys():
                data2017[data_source[64][i]] += 1
            else:
                data2017[data_source[64][i]] = 1

        elif data_source[3][i][:4] == '2018':
            if data_source[64][i] in data2018.keys():
                data2018[data_source[64][i]] += 1
            else:
                data2018[data_source[64][i]] = 1

        elif data_source[3][i][:4] == '2019':
            if data_source[64][i] in data2019.keys():
                data2019[data_source[64][i]] += 1
            else:
                data2019[data_source[64][i]] = 1

        elif data_source[3][i][:4] == '2020':
            if data_source[64][i] in data2020.keys():
                data2020[data_source[64][i]] += 1
            else:
                data2020[data_source[64][i]] = 1

    data2016 = {k: v for k, v in sorted(data2016.items(), key=lambda item: item[1], reverse=True)}
    keys1 = data2016.keys()
    values1 = data2016.values()

    data2017 = {k: v for k, v in sorted(data2017.items(), key=lambda item: item[1], reverse=True)}
    keys2 = data2017.keys()
    values2 = data2017.values()

    data2018 = {k: v for k, v in sorted(data2018.items(), key=lambda item: item[1], reverse=True)}
    keys3 = data2018.keys()
    values3 = data2018.values()

    data2019 = {k: v for k, v in sorted(data2019.items(), key=lambda item: item[1], reverse=True)}
    keys4 = data2019.keys()
    values4 = data2019.values()

    data2020 = {k: v for k, v in sorted(data2020.items(), key=lambda item: item[1], reverse=True)}
    keys5 = data2020.keys()
    values5 = data2020.values()

    fig, axs = plt.subplots(5)
    fig.suptitle('Pocet nehod vo vybranych krajoch')
    plt.setp(axs, yticks=[0, 10000, 20000], ylabel='Pocet nehod')
    fig.tight_layout()
    fig.set_size_inches(6.5, 9.5)

    create_ax(axs, 0, keys1, values1, '2016')
    create_ax(axs, 1, keys2, values2, '2017')
    create_ax(axs, 2, keys3, values3, '2018')
    create_ax(axs, 3, keys4, values4, '2019')
    create_ax(axs, 4, keys5, values5, '2020')

    if fig_location:
        if not os.path.exists(fig_location):
            os.makedirs(fig_location)
        plt.savefig(f'{fig_location}/graph.png')
    if show_figure:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='get_stat.py')

    parser.add_argument('--fig_location', default = None, type=str, help='Path, where graph.png will be saved')
    parser.add_argument('--show_figure', default = False, type=bool, help='Boolean value, which indicates if graph should be opened after execution or not')

    args = parser.parse_args()

    data_source = DataDownloader().get_list()
    plot_stat(data_source, args.fig_location, args.show_figure)
