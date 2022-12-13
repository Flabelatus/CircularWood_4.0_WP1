__author__ = "Javid Jooshesh, j.jooshesh@hva.nl"
__version__ = "v1"


def find_nearest(array, value):
    return array[min(range(len(array)), key = lambda i: abs(array[i] - value))]


def search(base_array, array_to_search_from):
    found_closest_values = []
    hashset = set()

    # Copy the search array to not lose the original data from the array
    new_search_target_array = []
    for i in array_to_search_from:
        new_search_target_array.append(i)

    if base_array and array_to_search_from:
        while len(new_search_target_array) > len(array_to_search_from) / 1.2:
            print(len(array_to_search_from))
            for item in base_array:
                closest = find_nearest(new_search_target_array, item)
                if closest in hashset:
                    continue
                else:
                    hashset.add(closest)
                    new_search_target_array.remove(closest)
                    
                    if len(found_closest_values) < len(base_array):
                        print(len(found_closest_values))
                        found_closest_values.append(closest)

    return found_closest_values


x = [1, 2, 4, 4, 4, 6, 7, 7]
y = [2, 2, 2, 2, 2.02, 2.01, 7, 8]

a = search(x, y)
print(a)