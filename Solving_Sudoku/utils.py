rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [x + y for x in a for y in b]


boxes = cross(rows, cols)

row_units = [cross(x, cols) for x in rows]
column_units = [cross(rows, y) for y in cols]
square_units = [cross(xs, ys) for xs in ['ABC', 'DEF', 'GHI'] for ys in ['123', '456', '789']]
unitlist = row_units + column_units + square_units
units = dict((box, [u for u in unitlist if box in u]) for box in boxes)
peers = dict((box, set(sum(units[box], [])) - set([box])) for box in boxes)


def display(values):
    """Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None"""
    width = 1 + max(len(values[box]) for box in boxes)  # should be 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return


if __name__ == '__main__':
    print(boxes)
    print(row_units)
    print(column_units)
    print(square_units)
    print(units)
    print(peers)
    display(dict((box, box[1:]) for box in boxes))
