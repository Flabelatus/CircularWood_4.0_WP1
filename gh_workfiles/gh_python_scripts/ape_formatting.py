"""__author__ = "Javid Jooshesh, j.jooshesh@hva.nl"
__version__ = "v1"
"""

import rhinoscriptsyntax as rs
import Grasshopper.DataTree as dt
import ghpythonlib.treehelpers as th

pairs = []

for i in range(len(database_elements)):
    for j in range(len(design_elements)):
        if database_elements[i] / (design_elements[j] + bit_diameter) >= 1:
            pairs.append(
                (i, j, float(
                    database_elements[i] / (design_elements[j] + bit_diameter)
                )
            )
        )
            
dic = {}

# Hashtable
for i in range(len(design_elements)):
    dic[i] = []
    
for i in range(len(pairs)):
    if pairs[i][1] in dic.keys():
        dic[pairs[i][1]].append(
            (pairs[i][0], pairs[i][2])
        ) if pairs[i][2] >= 1 else None

index_list = th.list_to_tree(
    [
        dic[i] for i in range(len(design_elements))
    ], source=[0]
)

msg = "Database Index: {0}, Design Element Index: {1}, Amounts per Element: {2}"
for i in range(len(pairs)):
    a = pairs[i][0]
    b = pairs[i][1]
    c = pairs[i][2]
    print(msg.format(a, b, c))