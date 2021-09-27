
import copy
import argparse
from multiprocessing import Pool
from functools import partial

nextCells = []
mrow = list()
mcolumn = list()


def main():
    # allows me to user argparse as inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-t", "--threads", type=int, default=1)
    args = parser.parse_args()

    # prints my r number onto the console
    print("Project :: R11487176\n\n\n")

    # opens whatever the args.input was as read
    with open(args.input, 'r') as file:
        # calls global nextCells to read the input matrix and make them in to lists of lists
        global nextCells
        nextCells = [list(line.strip()) for line in file]

        # using enumerate, assigns indices of elements in the matrix into row and column
        for x, ele1 in enumerate(nextCells):
            for y, ele2 in enumerate(ele1):
                global mrow
                global mcolumn
                mrow.append(x)
                mcolumn.append(y)

    # creates number of processes based on args.threads(input)
    MAX_PROCESS = args.threads
    processPool = Pool(processes=args.threads)

    currentCells = []

    # opens user input outputfile to write
    with open(args.output, 'w') as output_file:

        # loops 100 times to iterate through the matrix using pool.map
        for x in range(0, 100):
            # creates a deep copy of the nextCell which holds the immediate matrix from the input
            # then using pool.map and partial, iterate through the matrix with multiprocessing
            currentCells = [copy.deepcopy(nextCells)]
            neighborx = partial(neighbor, row=mrow, column=mcolumn, ncell=nextCells)
            nextCells = processPool.map(neighborx, currentCells)
            nextCells = nextCells[0]

        # flattens the list of list into a string with new line character wherever it needs
        cellflat3 = list(map(''.join, nextCells))
        cellflat4 = '\n'.join(str(ele) for ele in cellflat3)
        output_file.write(str(cellflat4))
        output_file.write("\n\n")


# my version of the solver
# takes in the currentCells which is a deepcopy of the nextCell and row, column and ncell(nextCells)
# iterates through the coordinates in row and column to check it's neighboring characters in currentCells
def neighbor(currentCells, row, column, ncell):
    count_neighbor = 0
    for x in range(0, len(row)):
        if (currentCells[(row[x] - 1) % len(currentCells)][column[x] % len(currentCells)]) == 'O':  # above
            count_neighbor += 1
        if (currentCells[row[x] % len(currentCells)][(column[x] + 1) % len(currentCells)]) == 'O':  # right
            count_neighbor += 1
        if (currentCells[(row[x] + 1) % len(currentCells)][column[x] % len(currentCells)]) == 'O':  # bottom
            count_neighbor += 1
        if (currentCells[row[x] % len(currentCells)][(column[x] - 1) % len(currentCells)]) == 'O':  # left
            count_neighbor += 1
        if (currentCells[(row[x] - 1) % len(currentCells)][(column[x] + 1) % len(currentCells)]) == 'O':  # top_right
            count_neighbor += 1
        if (currentCells[(row[x] + 1) % len(currentCells)][(column[x] + 1) % len(currentCells)]) == 'O':  # bot_right
            count_neighbor += 1
        if (currentCells[(row[x] + 1) % len(currentCells)][(column[x] - 1) % len(currentCells)]) == 'O':  # bot_left
            count_neighbor += 1
        if (currentCells[(row[x] - 1) % len(currentCells)][(column[x] - 1) % len(currentCells)]) == 'O':  # top_left
            count_neighbor += 1

        if (currentCells[row[x]][column[x]]) == '.':
            if count_neighbor == 2 or count_neighbor == 4 or count_neighbor == 6 or count_neighbor == 8:
                ncell[row[x]][column[x]] = 'O'
            else:
                ncell[row[x]][column[x]] = '.'

        if (currentCells[row[x]][column[x]]) == 'O':
            if count_neighbor == 2 or count_neighbor == 3 or count_neighbor == 4:
                ncell[row[x]][column[x]] = 'O'
            else:
                ncell[row[x]][column[x]] = '.'
        count_neighbor = 0

    return ncell


if __name__ == '__main__':
    main()
