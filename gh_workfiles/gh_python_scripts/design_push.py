"""
__Matching Algorithm__
__author__ = "Javid Jooshesh, j.jooshesh@hva.nl"
__version__ = "v1"
"""

        
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        
        
class Queue:
    """_A class representing the Queue data structure based on the FIFO 
        (first in first out) principle_"""
            
    def __init__(self, value):
        """_Init method of the class_"""
                
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1
        
    def print_queue(self):
        """_A method to print the nodes of the queue_"""
                
        current = self.first
        while current:
            print(current.value)
            current = current.next
        
    def enqueue(self, value):
        """_Add a node to the queue_"""
                
        new_node = Node(value)
        if self.length == 0:
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node
        self.length += 1
        
    def dequeue(self):
        """_Remove a node from the queue_"""
                
        if self.length == 0:
            return None
        current = self.first
        if self.length == 1:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next
            current.next = None
        self.length -= 1
        return current
        
        
def update_length(subtracting_length, index):
    """ Update the length of part in the database via subtracting its length
    from the length of the design part
    """
    
    global remained_lengths
    try:
        remained_lengths[index] -= subtracting_length
        return remained_lengths[index]
    except:
        msg = "### -----> Index is not in the list <----- ###"
        print(msg)
        return -1
        
def organize(param_1, param_2, param_3):
    """ Organize the given data as parameters. This function is used to
        organize the elements with the criteria of length and the factor of 
        APE (Amount Per Element). 
        
        param_1: A set from the list of APE as inputs
        param_2: List of indecies of usable elements from the database
        param_3: Remained length of the usable elements in the database at the
            index of `param_2`
        
        returns: Dictionary of the data organized in the following way:
                   {
                param_1: {
                    'index_list': [param_2],
                    'remained_lengths': [param_3]
                }
            }
    """
    hashtable = dict()
    FIRST_ARG = 0
    SECOND_ARG = 1
    data = zip(param_1, param_2, param_3)
            
    for i in range(len(param_1)):
        hashtable[param_1[i]] = {'index_list': [], 'remained_lengths': []}
                
    for i in range(len(data)):
        if data[i][FIRST_ARG] in hashtable.keys():
            hashtable[data[i][FIRST_ARG]]['index_list'].append(data[i][SECOND_ARG])
            hashtable[data[i][FIRST_ARG]]['remained_lengths'].append(param_3[i])
                    
    return hashtable
        

def main():
    global ape
    global db_index
    global remained_lengths
    global lengths
    global design_elements_index
    global db_index_to_update
    global des_index
    global filtered_widths_indecies
    global selection_index
    
    LAST_INDEX = -1
    FIRST_INDEX = 0
    
    data = organize(ape, db_index, remained_lengths)
    filtered_lengths_indecies = [data[key]['index_list'] for key in data]
    
    for key in data:
        # See whats in the data
        print("{0}: {1}".format(key, data[key]))
    print("----------------------------")
    
    queue = Queue(None)
    ape_as_key_list = sorted(set(ape))
    print(ape_as_key_list)
    if queue.first.value is not None:
        queue.print_queue()
    
    node = []
    
    for key, value in data.items():
        if key == ape_as_key_list[LAST_INDEX]:
            for index, item in enumerate(value['index_list']):
                if index == FIRST_INDEX:
                    # Add the item and remained_lengths at the same index
                    # to the node as a tuple
                    node.append((item, value['remained_lengths'][index]))
                    
                    if queue.first.value is None:
                        queue.dequeue()
                    queue.enqueue(node[FIRST_INDEX])

    updated_length = 0
    print(node)
    # Design Element Index
    dei = []
    # For now just working with one element. Later can be a list of lengths 
    for i in range(len(lengths)):
        for index, item in enumerate(db_index):
            if item == node[FIRST_INDEX][0]:
                # Update the length by subtracting the design element length 
                # from the database element length
                updated_length = update_length(lengths[i], index)
                dei.append(index)

        lengths.remove(lengths[i])
    queue.print_queue()
    db_index_to_update = node[FIRST_INDEX][0]
    
    design_elements_index = dei 
    return updated_length
    
    
if __name__ == "__main__":
    remaining_length = main()

