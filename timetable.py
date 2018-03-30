#coding=utf-8

from collections import namedtuple

import matplotlib as mpl
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams["text.latex.unicode"] = True


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
            item("Einarbeitung in Python", 0, 2, "th"),
            item("Erstellen der Simulation", 1, 4, "th"),
            item("Ergänzung der Simulation", 5, 2, "th"),
            item("Bau der Messvorrichtung", 0, 2, "ex"),
            item("Aufnahme der Messreihen", 2, 4, "ex"),
            item("Anpassung des Aufbaus", 6, 3, "ex"),
            item("Auswertung/Erstellung des Posters", 8, 3, "ev")
        ]

data_as_array = np.array(
                            [[  item.start,
                                item.duration ]
                            for item in items ]
                        )

y_values        = np.arange(len(items))
starting_points = data_as_array[:,0]
durations       = data_as_array[:,1]
y_labels        = [item.description for item in items]
colors          = [item.color for item in items]

kwargs = {
            "height" : .5, 
            "align" : "center"
         }


#################
#   plotting    #
#################

fig, ax = plt.subplots()
ax.barh(y_values, durations, left=starting_points, color=colors, **kwargs)

# adjust yaxis
ax.invert_yaxis()
ax.set_yticks(y_values)
ax.set_yticklabels(y_labels)
# hide yticks
ax.tick_params(axis='y', length=0)

# set xticks, label and grid
ax.set_xticks(np.arange(12))
ax.set_xlabel("Wochen (09.04.2018 - 22.06.2018)")
ax.set_xlim((0, 11))
# place grid below elements in plot
ax.set_axisbelow(True)
ax.grid(axis='x')

plt.title("Zeitplan")
# make and map proxy artists to legend
plt.legend(handles=[Patch(color=c, label=l)
                    for c, l in zip(color_mapping.values(), 
                                    ("Theorie", "Experiment", "Auswertung"))
                   ]
          )
