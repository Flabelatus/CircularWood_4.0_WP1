__author__ = "Javid Jooshesh, j.jooshesh@hva.nl"
__version__ = "v1"


def find_closest_members(array1, array2):
    closest_members = []
    for value in array1:
        nearest_value = min(array2, key=lambda x: abs(x - value))
        closest_members.append(nearest_value)
    return closest_members
    

nearest_lengths = find_closest_members(design_lengths, database_lengths)