import sys, os, random
from os import path

def get_jump_routes_peg_holes(lines,jump_routes, peg_holes):
    for line in lines:
        temp_j_route = []
        temp_jump_route = line.replace("\n", "").split()
        for route in temp_jump_route:
            temp_j_route.append(int(route))
        jump_routes.append(temp_j_route)
    for route in jump_routes:
        for potential_holes in route:
            if potential_holes not in peg_holes:
                peg_holes.append(potential_holes)
    return jump_routes, peg_holes

def get_proposition_encoding(index, jump_routes, number_holes):
    # Atoms
    print("Propositional Encoding Key: \n")
    # Atom Jump(A,B,C,I)
    # Jump(A,B,C,I) means that at time I, the peg in A is jumped to C over B.
    print("Propositional Encoding: Jump(A,B,C,I): \n")
    for row_a_b_c_i in jump_routes:
        new_index = index

        for time_pt in range(number_holes - 2):
            text = ""
            for triple_holes in row_a_b_c_i:
                text += ","+(str(triple_holes))

            new_index = new_index + 1
            actual_time = time_pt + 1
            print(str(new_index)+" Jump("+str(text)+","+str(actual_time)+")\n")

        index = new_index

        new_index = index

        for time_pt in range(number_holes - 2):
            text = ""
            for triple_holes in row_a_b_c_i:
                text += ","+(str(triple_holes))
            new_index = new_index + 1

            text = text[::-1]
            actual_time = time_pt + 1
            print(str(new_index)+" Jump("+str(text)+","+str(actual_time)+")\n")

        index = new_index

    # Atom Peg(H,I)
    # Peg(H,I) means that hole H has a peg in it at time I.
    print("Propositional Encoding: Peg(H,I): \n")
    new_index = index
    for peg in range(number_holes):
        for time_pt in range(number_holes - 1):
            new_index = new_index + 1
            actual_time = time_pt + 1
            peg_offset = peg + 1
            print(str(new_index)+" Peg("+str(peg_offset)+","+str(actual_time)+")\n")


def get_precondition_axioms(time_points, index, jump_routes, number_holes):
    # Precondition Axiom
    # f, at time I, you jump a peg from A to C over B, then A and B must have pegs at
    # time I and C must not have a peg at time I.
    print("Precondition Axiom: \n")
    for row_a_b_c_i in jump_routes:
        new_index = index
        for time_pt in range(number_holes - 2):
            new_index = new_index + 1
            peg_time_i = 0
            a = 1
            for peg in row_a_b_c_i:
                if peg_time_i > 1:
                    a = -1
                actual_time = time_pt + 1
                create_unique_id = a * (time_points + (peg - 1) * (number_holes - 1) + actual_time)
                print(str(-new_index) + " " + str(create_unique_id) + "\n")
                peg_time_i = peg_time_i + 1
        index = new_index

        row_a_b_c_i.reverse()

        new_index = index
        for time_pt in range(number_holes - 2):
            new_index = new_index + 1
            peg_time_i = 0
            a = 1
            for peg in row_a_b_c_i:
                if peg_time_i > 1:
                    a = -1
                actual_time = time_pt + 1
                create_unique_id = a * (time_points + (peg - 1) * (number_holes - 1) + actual_time)
                print(str(-new_index) + " " + str(create_unique_id) + "\n")
                peg_time_i = peg_time_i + 1
        index = new_index

def get_causal_axioms(time_points, index, jump_routes, number_holes):
    # Causal Axioms
    # If you jump from A to C over B at time I, then, at time I+1, A and B are empty
    # and C has a peg.
    print("Causal Axiom: \n")
    for row_a_b_c_i in jump_routes:
        row_a_b_c_i.reverse()

        new_index = index
        for time_pt in range(number_holes - 2):
            new_index = new_index + 1
            peg_time_i = 0
            a = -1
            for peg in row_a_b_c_i:
                if peg_time_i > 1:
                    a = 1
                actual_time = time_pt + 2
                create_unique_id = a * (time_points + (peg - 1) * (number_holes - 1) + actual_time)
                print(str(-new_index) + " " + str(create_unique_id) + "\n")
                peg_time_i = peg_time_i + 1
        index = new_index
        row_a_b_c_i.reverse()

        new_index = index
        for time_pt in range(number_holes - 2):
            new_index = new_index + 1
            peg_time_i = 0
            a = -1
            for peg in row_a_b_c_i:
                if peg_time_i > 1:
                    a = 1
                actual_time = time_pt + 2
                create_unique_id = a * (time_points + (peg - 1) * (number_holes - 1) + actual_time)
                print(str(-new_index) + " " + str(create_unique_id) + "\n")
                peg_time_i = peg_time_i + 1
        index = new_index
    return index

def get_frame_axioms(time_points, use_index, jump_routes, number_holes):
    # Frame Axioms
    # Frame axioms assert that state can change only if a relevant action occurs.
    print("Frame Axiom A: \n")
    new_index = use_index + 1
    for row_a_b_c_i in jump_routes:
        row_a_b_c_i.reverse()
    for peg in range(number_holes):
        for time_pt in range(number_holes - 2):
            action_array = []
            jump_time = 0
            for row in jump_routes:
                if row[0] == peg + 1 or row[1] == peg + 1:
                    action_array.append(jump_time * (number_holes - 2) * 2 + time_pt + 1)
                if row[2] == peg + 1 or row[1] == peg + 1:
                    action_array.append((jump_time * 2 + 1) * (number_holes - 2) + time_pt + 1)
                jump_time = jump_time + 1
            text_row = ""
            for action in action_array:
                text_row += ","+(str(action))
            print(str(-new_index) + " "+str(new_index+1)+" "+str(text_row)+"\n")
            new_index = new_index + 1
        new_index = new_index + 1

    #index = new_index

    print("Frame Axiom B: \n")
    new_index = use_index + 1
    for peg in range(number_holes):
        for time_pt in range(number_holes - 2):
            action_array = []
            jump_time = 0
            current_peg = peg+1
            current_time = time_pt +1
            for row in jump_routes:
                if row[0] == current_peg:
                    action_array.append((jump_time * 2 + 1) * (number_holes - 2) + current_time)
                if row[2] == current_peg:
                    action_array.append(jump_time * 2 * (number_holes - 2) + current_time)
                jump_time = jump_time + 1
            text_row = ""
            for action in action_array:
                text_row += (str(action)) + ","
            print(str(new_index) + " "+str(-new_index-1)+" "+str(text_row)+"\n")
            new_index = new_index + 1
        new_index = new_index + 1

    #index = new_index

    print("Frame Axiom B: \n")
    for jump_time in range(time_points):
        jump_timeTmp = jump_time + number_holes - 2
        while True:
            if jump_timeTmp >= time_points:
                break
            print(str(-jump_time-1)+" "+str(-jump_timeTmp-1)+"\n")
            jump_timeTmp = jump_timeTmp + number_holes - 2

def get_states(step_level, time_points, empty_starting_hole, number_holes):
    while step_level < 4:
        if step_level == 1:
            print("Starting State: \n")
            # Starting State
            # Specify the truth value of Peg(H,1) for each hole H.
            for peg_time_i in range(number_holes):
                a = 1
                if peg_time_i == empty_starting_hole - 1:
                    a = -1
                index_offset = a * (time_points + 1 + (number_holes - 1) * peg_time_i)
                print(str(index_offset)+"\n")
        # Ending State
        # Exactly one peg remains. This involves two kinds of axioms.
        elif step_level == 2:
            print("Ending State A: \n")
            # A
            # At least one peg remains at time N-1.
            for peg_time_i in range(number_holes):
                index_offset = time_points + (number_holes - 1) * (peg_time_i + 1)
                print(str(index_offset)+" ")
            print("\n")

        elif step_level == 3:
            print("Ending State B: \n")
            # B
            # No two holes have a peg.
            for peg_time_i in range(number_holes):
                holes_h = time_points + (number_holes - 1) * (peg_time_i + 1)
                peg_time_i_Tmp = peg_time_i + 1
                while True:
                    if peg_time_i_Tmp > number_holes - 1:
                        break
                    holes_j = time_points + (number_holes - 1) * (peg_time_i_Tmp + 1)
                    peg_time_i_Tmp = peg_time_i_Tmp + 1
                    new_holes_h = -holes_h
                    new_holes_j = -holes_j
                    print(str(new_holes_h) + " " + str(new_holes_j) + "\n")

        step_level += 1

def create_cnf(number_holes, empty_starting_hole, jump_routes, index):

    # Atoms

    # Atom Jump(A,B,C,I)
    # Jump(A,B,C,I) means that at time I, the peg in A is jumped to C over B.
    # Atom Peg(H,I)
    # Peg(H,I) means that hole H has a peg in it at time I.
    # Propositional Encoding
    get_proposition_encoding(index, jump_routes, number_holes)

    time_points = len(jump_routes) * (number_holes - 2) * 2
    index = 0
    # Precondition Axiom
    # f, at time I, you jump a peg from A to C over B, then A and B must have pegs at
    # time I and C must not have a peg at time I.
    # Precondition Axioms
    get_precondition_axioms(time_points, index, jump_routes, number_holes)

    index = 0
    # Causal Axioms
    # If you jump from A to C over B at time I, then, at time I+1, A and B are empty
    # and C has a peg.
    # Causal Axioms
    index = get_causal_axioms(time_points, index, jump_routes, number_holes)

    use_index = index
    # Frame Axioms
    # Frame axioms assert that state can change only if a relevant action occurs.
    # Frame Axioms
    get_frame_axioms(time_points, use_index, jump_routes, number_holes)

    step_level = 1
    # Starting State
    # Specify the truth value of Peg(H,1) for each hole H.
    # Ending State
    # Exactly one peg remains. This involves two kinds of axioms.
    # A
    # At least one peg remains at time N-1.
    # B
    # No two holes have a peg.
    # States
    get_states(step_level, time_points, empty_starting_hole, number_holes)


def main(argv):
    input_file = str(sys.argv[1])
    f = open(input_file, "r")
    first_line = f.readline()
    first_line_values = first_line.split()
    number_holes = int(first_line_values[0])
    empty_starting_hole = int(first_line_values[1])
    peg_holes = []
    jump_routes = []

    # Number of Time Points is Equal to Number of Holes Minus One
    # Let N be Number of Holes
    # For Each Hole H and I = 1...N-1
    # There Should be Atom Peg(h,I)
    # and For Each Triple of Holes in a Row A,B,C
    # and I = 1...N-2
    # There should be Atom Jump(A,B,C,I)
    # Atoms
    # Peg(H,I)
    # Jump(A,B,C,I)

    # Atoms

    # Atom Jump(A,B,C,I)
    # Jump(A,B,C,I) means that at time I, the peg in A is jumped to C over B.
    # Atom Peg(H,I)
    # Peg(H,I) means that hole H has a peg in it at time I.
    jump_routes, peg_holes = get_jump_routes_peg_holes(f.readlines(), jump_routes, peg_holes)
    index = 0
    create_cnf(number_holes, empty_starting_hole, jump_routes, index)

    f.close()

if __name__ == "__main__":
    main(sys.argv)