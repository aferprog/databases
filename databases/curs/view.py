import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable

class View:
    @staticmethod
    def show_categories(categories):
        print('----------------------------\n')
        i = 1
        for x in categories:
            print('%d. %s (%d)  --  %d' % (i, x[0], x[1], x[2]))
            i = i+1
        print('\n----------------------------')

    @staticmethod
    def show_channels(channels):
        print('----------------------------\n')
        i = 1
        for x in channels:
            print('%d. %s  --  %d' % (i, x[0], x[1]))
            i = i+1
        print('\n----------------------------')

    @staticmethod
    def show_ranges(ranges):
        print('----------------------------\n')
        i = 1
        for x in ranges:
            print('%d. %s  --  %d' % (i, x[0], x[1]))
            i = i+1
        print('\n----------------------------')

    @staticmethod
    def draw_cat(categories):
        value = [x[2] for x in categories]
        labels = ["%s\n(%d)" % (x[0], x[1]) for x in categories]
        position = np.arange(len(categories))
        fig, ax = plt.subplots()
        ax.barh(position, value)
        ax.set_yticks(position)
        ax.set_yticklabels(labels,
                           fontsize=10)
        plt.show()

    @staticmethod
    def draw_chan(channels):
        def get_lable(str):
            t = str.split()
            res = ''
            for x in t[:int(len(t)/2)]:
                res += x+' '
            res += '\n'
            for x in t[int(len(t)/2):]:
                res += x+' '
            return res
        value = [x[1] for x in channels]
        labels = [get_lable(x[0]) for x in channels]
        position = np.arange(len(channels))
        fig, ax = plt.subplots()
        ax.barh(position, value)
        ax.set_yticks(position)
        ax.set_yticklabels(labels,
                           fontsize=10)
        plt.show()

    @staticmethod
    def draw_range(channels):
        def get_lable(d):
            m = int(d/30.4167)
            d1 = d-int(m*30.4167)
            y = m / 12
            m = m % 12
            res = ''
            if y != 0:
                res += "%d Years\n" % y
            if y != 0 or m != 0:
                res += "%d Month " % m
            if y != 0 or m != 0 or d1 != 0:
                res += "%d Days " % d1
            return res

        value = [x[1] for x in channels]
        labels = [get_lable(x[0]) for x in channels]
        position = np.arange(len(channels))
        fig, ax = plt.subplots()
        ax.barh(position, value)
        ax.set_yticks(position)
        ax.set_yticklabels(labels,
                           fontsize=10)
        plt.show()

    @staticmethod
    def print_table(head, tab):
        columns = len(head)
        table = PrettyTable(head)
        for x in tab:
            table.add_row(x)
        print(table)
