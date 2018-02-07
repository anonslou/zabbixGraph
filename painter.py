#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num
import numpy as np
from datetime import datetime
import matplotlib.cm as cm

class Plot:
    
    def __init__(self, title):
        self.lines = {}
        self.fig, self.ax = plt.subplots()
        self.ax.set_title(title)
        self.fig.autofmt_xdate()
        plt.autoscale(enable=True, axis='x', tight=True)
        self.fig.set_size_inches(16, 9)
        self.ax.grid(True)
        plt.ylabel('Mb/s')

    def add_line(self, data, legend):
        dt = np.array([])
        clocks = []
        for clock, value in data:
            dt = np.append(dt, value/1024/1024)
            clocks.append(datetime.fromtimestamp(clock))
        self.lines[legend] = (clocks, dt)
   
    _summer = 0
    _spring = 0
    def _get_color(self, legend):
        if 'IN' in legend:
            self._summer+=80
            return cm.summer(self._summer)
        if 'OUT' in legend:
            self._spring+=80
            return cm.winter(self._spring)

    def paint_graph(self):
        for legend, (clock, data) in self.lines.items():
            pl = self.ax.plot(date2num(clock), data, linewidth=1.5, label=legend, color=self._get_color(legend))
            self.ax.xaxis.set_major_formatter(DateFormatter('%d.%m.%Y %H:%M:%S'))
        plt.legend()

    def show(self):
        plt.show()

    def save(self, filename):
        plt.savefig(filename, format='png', dpi=150)
