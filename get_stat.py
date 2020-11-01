from download import DataDownloader
from matplotlib import pyplot as plt
import os

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

    rects = axs[0].bar(keys1, values1)
    axs[0].set_title('2016')
    add_order_to_axs(axs[0], rects)

    rects = axs[1].bar(keys2, values2)
    axs[1].set_title('2017')
    add_order_to_axs(axs[1], rects)

    rects = axs[2].bar(keys3, values3)
    axs[2].set_title('2018')
    add_order_to_axs(axs[2], rects)

    rects = axs[3].bar(keys4, values4)
    axs[3].set_title('2019')
    add_order_to_axs(axs[3], rects)

    rects = axs[4].bar(keys5, values5)
    axs[4].set_title('2020')
    add_order_to_axs(axs[4], rects)

    if fig_location:
        if not os.path.exists(fig_location):
            os.makedirs(fig_location)
        plt.savefig(f'{fig_location}/graph.png')
    if show_figure:
        plt.show()

data_source = DataDownloader().get_list()
plot_stat(data_source, fig_location='graphs', show_figure=True)


