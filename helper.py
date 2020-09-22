import pathlib


def sud_txt_to_dimacs(example_path='top95.sdk.txt'):
    '''This function reads .txt (txtfile one line of 81 characters per puzzle, '.' for free space)
    Translate txtfile to DIMACS. Puts Dimacs file in folder sud_examples
    top95.sdk.txt is a set of 95 "hard" puzzles, favoured benchmark set of a web forum for sudokus'''

    all_sudokus = open(example_path, 'r').read()
    all_sudokus = all_sudokus.split("\n")
    sudnr = 1

    for sudoku in all_sudokus:

        sud_file = open(r'../sud_examples/sudoku_%d'%sudnr, 'w+')
        row = 1
        column = 1

        for place in sudoku:
            if place.isdigit():
                sud_file.write(str(row) + str(column) + str(place) + ' 0\n')

            column += 1

            if column == 10:
                column = 1
                row += 1

        sudnr += 1

    return all_sudokus