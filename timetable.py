#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable = C, R

from collections import namedtuple

import matplotlib as mpl
from matplotlib.patches import Patch
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams["font.size"] = 12


# colors
cmap = plt.get_cmap("Set1")
color_mapping = {
    "th" : cmap(0),     # theory
    "ex" : cmap(1),     # experiment
    "ev" : cmap(2)      # evaluation
    }


class item(namedtuple("item",
                      ["description", "start", "duration", "domain"])):
    """
    item in the timetable containing startpoint (starting with 0), duration,
    domain (theory, experiment, evaluation) and description (as it appears in
    the plot)
    """
    __slots__ = ()
    @property
    def color(self):
        return color_mapping[self.domain]


#############
#   data    #
#############

items = [
    # item: description, start, duration, domain
    item("Einarbeitung\n in Python", 0, 2, "th"),
    item("Erstellen der\n Simulation", 1, 4, "th"),
    #  item("Ergänzung der\n Simulation", 5, 2, "th"),
    item("Bau der Mess-\n vorrichtung", 0, 2, "ex"),
    item("Aufnahme der\n Messreihen", 2, 4, "ex"),
    item("Anpassung des\n Aufbaus", 6, 3, "ex"),
    item("Auswertung der\nDaten", 7, 3, "ev"),
    item("Erstellung des\nPosters", 8, 11, "ev")
    ]

data_as_array = np.array([[item.start, item.duration] for item in items])

y_values        = np.arange(len(items))
starting_points = data_as_array[:,0]
durations       = data_as_array[:,1]
y_labels        = [item.description for item in items]
colors          = [item.color for item in items]

kwargs = {
    "height"    :   .4,
    "align"     :   "center"
    }


#################
#   plotting    #
#################

fig = plt.figure(figsize=(8, 6))
# make two subplots - actual plot and legend
gs = GridSpec(2, 1, height_ratios=[11, 1])

# make timetable
ax = plt.subplot(gs[0])
ax.barh(y_values, durations, left=starting_points, color=colors, **kwargs)

# adjust yaxis
ax.invert_yaxis()
ax.set_yticks(y_values)
ax.set_yticklabels(y_labels)
# hide yticks
ax.tick_params(axis='y', length=0)

# xaxis: set ticks, label and limits
ax.set_xticks(np.arange(12))
ax.set_xlabel("Wochen (09.04.2018 - 22.06.2018)")
ax.set_xlim((0, 11))
# turn grid off to avoid conflicts with local settings
ax.grid(False)
# place grid below elements in plot
ax.set_axisbelow(True)
ax.grid(axis='x')

# make legend in second subplot
legend_ax = plt.subplot(gs[1])
# remove ticks and boundary box
legend_ax.set(xticks=[], yticks=[])
legend_ax.set_axis_off()
# make and map proxy artists to legend
plt.legend(handles=[Patch(color=c, label=l)
                    for c, l in zip(color_mapping.values(),
                                    ("Theorie", "Experiment", "Auswertung"))],
           loc="lower center", ncol=3)

# allign subplots
plt.tight_layout()

plt.savefig("timetable.png", format="png", dpi=300)
plt.savefig("timetable.eps", format="eps", dpi=1000)
