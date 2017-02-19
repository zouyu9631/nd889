from utils import *


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.
    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    assert len(grid) == 81
    return dict(zip(boxes, ['123456789' if v_in_g == '.' else v_in_g for v_in_g in grid]))


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # all boxes have 2 values, which cloud be one of naked-twins
    boxes_with_len_2 = [b for b in boxes if len(values[b]) == 2]
    for b in boxes_with_len_2:
        for u in units[b]:
            # find whether thers's another twin
            if len([same_value_box for same_value_box in u if values[b] == values[same_value_box]]) > 1:
                # if have, eliminate all other peers in the unit
                other_boxes = [other_box for other_box in u if values[b] != values[other_box]]
                for ob in other_boxes:
                    for d in values[b]:
                        values[ob] = values[ob].replace(d, '')

    return values


def eliminate(values):
    """Eliminate values from peers of each box with a single value.
    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.
    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    for box in boxes:
        if len(values[box]) == 1:
            d = values[box]
            for peer_box in peers[box]:
                values[peer_box] = values[peer_box].replace(d, '')

    """
    #this solution use cache for not changing initial state
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    """
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.
    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.
    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for d in '123456789':
            dboxes = [box for box in unit if d in values[box]]
            if len(dboxes) == 1: values[dboxes[0]] = d
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False: return values
    if all(len(values[box]) == 1 for box in boxes):
        return values  # solved

    # Choose one of the unfilled squares with the fewest possibilities
    _, shortest_box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    for d in values[shortest_box]:
        try_values = values.copy()
        try_values[shortest_box] = d
        try_values = search(try_values)
        if try_values:
            return try_values


if __name__ == '__main__':
    grid1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    # gv = grid_values(grid1)
    # display(gv)
    # print('\n')
    # display(eliminate(gv))
    # # display(eliminate(eliminate(eliminate(eliminate(eliminate(eliminate(eliminate(eliminate(gv)))))))))
    # print('\n')
    # display(only_choice(eliminate(gv)))
    # print('\n')
    # gv = grid_values(grid1)
    # display(reduce_puzzle(gv))
    # print('\n')
    #
    # gv = grid_values(grid1)
    # display(search(gv))

    # a harder puzzle
    grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    gv = grid_values(grid2)
    # display(reduce_puzzle(gv))
    # print('\n')
    display(search(gv))

    # hardest_grid = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    # gv = grid_values(hardest_grid)
    # display(search(gv))

    before_naked_twins_1 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                            'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                            'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                            'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
                            'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
                            'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                            'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
                            'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
                            'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
                            'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                            'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
    possible_solutions_1 = [
        {'G7': '6', 'G6': '3', 'G5': '2', 'G4': '9', 'G3': '1', 'G2': '8', 'G1': '7', 'G9': '5', 'G8': '4', 'C9': '1',
         'C8': '5', 'C3': '8', 'C2': '237', 'C1': '23', 'C7': '9', 'C6': '6', 'C5': '37', 'A4': '2357', 'A9': '8',
         'A8': '6', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'F6': '125', 'F7': '35', 'F8': '9',
         'F9': '7', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'C4': '4',
         'B8': '3', 'B9': '4', 'I9': '9', 'I8': '7', 'I1': '23', 'I3': '23', 'I2': '6', 'I5': '5', 'I4': '8', 'I7': '1',
         'I6': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'E8': '1', 'A7': '27', 'A6': '257', 'E5': '347',
         'E4': '6', 'E7': '345', 'E6': '579', 'E1': '8', 'E3': '79', 'E2': '37', 'H8': '2', 'H9': '3', 'H2': '9',
         'H3': '5', 'H1': '4', 'H6': '17', 'H7': '8', 'H4': '17', 'H5': '6', 'D8': '8', 'D9': '6', 'D6': '279',
         'D7': '34', 'D4': '237', 'D5': '347', 'D2': '1', 'D3': '79', 'D1': '5'},
        {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8', 'H5': '6', 'F9': '7',
         'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8', 'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23',
         'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5', 'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9',
         'A4': '2357', 'A7': '27', 'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
         'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2', 'F6': '125',
         'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '79', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235',
         'F5': '8', 'E2': '3', 'F7': '35', 'F8': '9', 'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17',
         'D3': '79', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6',
         'D6': '279', 'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
    ]

    before_naked_twins_2 = {'A1': '23', 'A2': '4', 'A3': '7', 'A4': '6', 'A5': '8', 'A6': '5', 'A7': '23', 'A8': '9',
                            'A9': '1', 'B1': '6', 'B2': '9', 'B3': '8', 'B4': '4', 'B5': '37', 'B6': '1', 'B7': '237',
                            'B8': '5', 'B9': '237', 'C1': '23', 'C2': '5', 'C3': '1', 'C4': '23', 'C5': '379',
                            'C6': '2379', 'C7': '8', 'C8': '6', 'C9': '4', 'D1': '8', 'D2': '17', 'D3': '9',
                            'D4': '1235', 'D5': '6', 'D6': '237', 'D7': '4', 'D8': '27', 'D9': '2357', 'E1': '5',
                            'E2': '6', 'E3': '2', 'E4': '8', 'E5': '347', 'E6': '347', 'E7': '37', 'E8': '1', 'E9': '9',
                            'F1': '4', 'F2': '17', 'F3': '3', 'F4': '125', 'F5': '579', 'F6': '279', 'F7': '6',
                            'F8': '8', 'F9': '257', 'G1': '1', 'G2': '8', 'G3': '6', 'G4': '35', 'G5': '345',
                            'G6': '34', 'G7': '9', 'G8': '27', 'G9': '27', 'H1': '7', 'H2': '2', 'H3': '4', 'H4': '9',
                            'H5': '1', 'H6': '8', 'H7': '5', 'H8': '3', 'H9': '6', 'I1': '9', 'I2': '3', 'I3': '5',
                            'I4': '7', 'I5': '2', 'I6': '6', 'I7': '1', 'I8': '4', 'I9': '8'}
    possible_solutions_2 = [
        {'A1': '23', 'A2': '4', 'A3': '7', 'A4': '6', 'A5': '8', 'A6': '5', 'A7': '23', 'A8': '9', 'A9': '1', 'B1': '6',
         'B2': '9', 'B3': '8', 'B4': '4', 'B5': '37', 'B6': '1', 'B7': '237', 'B8': '5', 'B9': '237', 'C1': '23',
         'C2': '5', 'C3': '1', 'C4': '23', 'C5': '79', 'C6': '79', 'C7': '8', 'C8': '6', 'C9': '4', 'D1': '8',
         'D2': '17', 'D3': '9', 'D4': '1235', 'D5': '6', 'D6': '237', 'D7': '4', 'D8': '27', 'D9': '2357', 'E1': '5',
         'E2': '6', 'E3': '2', 'E4': '8', 'E5': '347', 'E6': '347', 'E7': '37', 'E8': '1', 'E9': '9', 'F1': '4',
         'F2': '17', 'F3': '3', 'F4': '125', 'F5': '579', 'F6': '279', 'F7': '6', 'F8': '8', 'F9': '257', 'G1': '1',
         'G2': '8', 'G3': '6', 'G4': '35', 'G5': '345', 'G6': '34', 'G7': '9', 'G8': '27', 'G9': '27', 'H1': '7',
         'H2': '2', 'H3': '4', 'H4': '9', 'H5': '1', 'H6': '8', 'H7': '5', 'H8': '3', 'H9': '6', 'I1': '9', 'I2': '3',
         'I3': '5', 'I4': '7', 'I5': '2', 'I6': '6', 'I7': '1', 'I8': '4', 'I9': '8'},
        {'A1': '23', 'A2': '4', 'A3': '7', 'A4': '6', 'A5': '8', 'A6': '5', 'A7': '23', 'A8': '9', 'A9': '1', 'B1': '6',
         'B2': '9', 'B3': '8', 'B4': '4', 'B5': '3', 'B6': '1', 'B7': '237', 'B8': '5', 'B9': '237', 'C1': '23',
         'C2': '5', 'C3': '1', 'C4': '23', 'C5': '79', 'C6': '79', 'C7': '8', 'C8': '6', 'C9': '4', 'D1': '8',
         'D2': '17', 'D3': '9', 'D4': '1235', 'D5': '6', 'D6': '237', 'D7': '4', 'D8': '27', 'D9': '2357', 'E1': '5',
         'E2': '6', 'E3': '2', 'E4': '8', 'E5': '347', 'E6': '347', 'E7': '37', 'E8': '1', 'E9': '9', 'F1': '4',
         'F2': '17', 'F3': '3', 'F4': '125', 'F5': '579', 'F6': '279', 'F7': '6', 'F8': '8', 'F9': '257', 'G1': '1',
         'G2': '8', 'G3': '6', 'G4': '35', 'G5': '345', 'G6': '34', 'G7': '9', 'G8': '27', 'G9': '27', 'H1': '7',
         'H2': '2', 'H3': '4', 'H4': '9', 'H5': '1', 'H6': '8', 'H7': '5', 'H8': '3', 'H9': '6', 'I1': '9', 'I2': '3',
         'I3': '5', 'I4': '7', 'I5': '2', 'I6': '6', 'I7': '1', 'I8': '4', 'I9': '8'}]

    assert naked_twins(before_naked_twins_1) in possible_solutions_1
    assert naked_twins(before_naked_twins_2) in possible_solutions_2
