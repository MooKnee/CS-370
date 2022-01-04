import sys, getopt, argparse
from queue import *

'''
Name: Caitlin Mooney
Class: CS 370
Assignment: Assignment 1
'''

class Process_Nodes:
    def __init__(self, state):
        self.state = state
        self.temporary_top = ""
        self.temporary_bottom = ""
    def translate_node_top(self):
        for t in self.state:
            self.temporary_top += domino_set[t][0]
        return self.temporary_top
    def translate_node_bottom(self):
        for b in self.state:
            self.temporary_bottom += domino_set[b][1]
        return self.temporary_bottom


class Process_Children():
    def __init__(self, state, max_depth):
        self.original_state = state
        self.original_maximum_state = max_depth
        self.kid_list = []
    def create_children(self):
        for i in range(len(domino_set)):
            self.kid_list.append(self.original_state + str(i+1))
        return self.kid_list

class Sequence_backsides():
    def __init__(self, top, bottom):
        self.state_status = self
        self.top_status = top
        self.bottom_status = bottom
        self.top_length = len(self.top_status)
        self.bottom_length = len(self.bottom_status)
        self.backsides = ''
    def get_prefix_length(self):
        if self.top_length == self.bottom_length:
            if self.top_status == self.bottom_status:
                return True, self.backsides
        elif self.top_length > self.bottom_length:
            topping = self.top_status[:self.bottom_length]
            if topping == self.bottom_status:
                self.backsides = "+" + self.top_status[self.bottom_length:]
                return True, self.backsides
            return False, self.backsides
        elif self.top_length < self.bottom_length:
            bottoming = self.bottom_length[:self.top_length]
            if bottoming == self.bottom_status:
                self.backsides = "-" + self.bottom_status[self.bottom_length:]
                return True, self.backsides
        else:
            return False, self.backsides


def dls_recursion(state, depth, max_depth):
    described_flag = 0
    if state.translate_node_top() == state.translate_node_bottom():
        described_flag = 1
        return state, described_flag
    elif depth == 0:
        return False
    else:
        hit_max_depth = False
        state_kid = state.create_children(max_depth)
        for kid in state_kid:
            described_flag, backside = kid.get_prefix_length()
            if described_flag == True:
                updated_depth = depth-1
                dls_output = dls_recursion(kid, updated_depth)
                if dls_output == False:
                    hit_max_depth = True
                elif described_flag == 1:
                    return dls_output
        if hit_max_depth == True:
            return False
        else:
            return False, described_flag

def end_ids(dls_output, depth):
    expected_output = dls_output[0]
    length_expected = len(expected_output)
    print('End of Iterative Depth')
    print('Solution sequence:' + expected_output)
    print('Top sequence: ' + expected_output.translate_node_top())
    print('Bottom sequence: ' + expected_output.translate_node_bottom())
    print('Current size:' + str(length_expected))
    print('IDS depth:' + str(depth))


def ids_algorithm(max_depth, queue):
    queueList = []
    while not queue.empty():
        queueList.append(queue.get())
    print('IDS')

    # Loop for the levels of depth
    for depth in range(max_depth):
        print('DFS Depth: ' + str(depth))
        for state in queueList:
            described_flag, backside = state.get_prefix_length()
            print('Start State: ' + backside)
            dls_output = dls_recursion(state, depth, max_depth)
            print('stack pop occurs here: ' + backside)

            if dls_output[1] == 1:
                end_ids(dls_output, depth)
                return dls_output
    return 'This depth is so full of dominoes it makes me sick.'


def load_queue(output_flag, domino_set, queue):
    if output_flag:
        print('Load Queue:')
    for node in domino_set:
        described_flag, backside = node.get_prefix_length()
        if described_flag:
            queue.put(node)
            if output_flag:
                print("Add Queue State: " + backside)
    return queue


def end_bfs(kid):

    print('Final Sequence of Dominoes: ' + str(kid))
    print('top sequence:' + str(kid.translate_node_top()))
    print('bottom sequence:' + str(kid.translate_node_bottom()))
    print('Number of Dominoes: ' + str(len(kid)))
    print('top sequence:' + str(kid.translate_node_top()))
    print('bottom sequence:' + str(kid.translate_node_bottom()))


def node_translation(kid, output_flag, backside, queue):
    if kid.translate_node_top() == kid.translate_node_bottom():
        end_bfs(kid)
        return kid.translate_node_top(), kid.translate_node_bottom()
    if output_flag:
        print("All the great queues leave their states: " + backside)
    queue.put(kid)
    return queue


def set_queue(frontier):
    queue = Queue(maxsize=0)
    checked = list()
    return queue, checked


def breadth_first_search(domino_set, frontier, max_depth, output_flag):
    queue, checked = set_queue(frontier)

    queue = load_queue(output_flag, domino_set, queue)

    while True:
        if frontier <= queue.qsize():
            print('Max Queue Size')
            ids_output = ids_algorithm(max_depth, queue)
            if ids_output[1] == 1:
                return ids_output[0]
        if queue.empty() == True:
            print('We know that queue is in there and that queue is all alone')
            return False
        updated_n = queue.get()
        described_flag, backside = updated_n.get_prefix_length()
        if output_flag:
            print("Keep the queue state, ya filthy animal: " + backside)
        checked.append(updated_n)
        state_kid = updated_n.create_children(max_depth)
        for kid in state_kid:
            described_flag, backside = kid.get_prefix_length()
            if described_flag == True:
                node_translation(kid, output_flag, backside, queue)


def main(frontier, max_depth, output_flag, set_length, init_dominoes):

    for dice in range(len(init_dominoes)):
        for decks in range(len(init_dominoes)):
            queue_string = init_dominoes[dice].split()
            domino_set[queue_string[0]] = [str(queue_string[1]), str(queue_string[2])]
    breadth_first_search(domino_set, frontier, max_depth, output_flag)


domino_set = {}


f = open(sys.argv[1], "r")
read = f.readlines()
domino_list = []
f.close()

for i in range(len(read)):
    domino_list.append(read[i].strip())
# frontier: maximum size of the queue
frontier = int(domino_list[0])
# maximum depth:  value of some kind of parameter that will to prevent the program from going
# into an infinite loop.
max_depth = int(domino_list[1])
# A flag indicating the type of output, as described in the next section
output_flag = int(domino_list[2])
# Fourth line: the number of Dominoes
set_length = domino_list[3]
# The set of dominos.
init_dominoes = domino_list[4:]

main(frontier, max_depth, output_flag, set_length, init_dominoes)