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


if __name__ == '__main__':
    gv = grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
    display(gv)
    print('\n')
    display(eliminate(gv))
    # display(eliminate(eliminate(eliminate(eliminate(eliminate(eliminate(eliminate(eliminate(gv)))))))))
    print('\n')
    display(only_choice(eliminate(gv)))
