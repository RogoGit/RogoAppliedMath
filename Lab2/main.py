class Node:

    # A node with a symbol, frequency, probability and code.
    # init node
    def __init__(self, symbol=None, frequency=None, probability=None, fano=None):
        self.symbol = symbol  # symbol itself
        self.frequency = frequency  # frequency
        self.probability = probability  # probability
        self.fano = fano  # shannon-fano code

    def __str__(self):
        # string representation
        return "Node(" + self.symbol.__repr__() + ", " + str(self.probability) + ", "  + self.fano + ") "
        # + str(self.left_ch) + ", " + str(self.right_ch) + ", "

    def __repr__(self):
        # representation of the Node
        return self.__str__()

    def __gt__(self, other):
        # nodes comparator (by probability)
        if self.probability is None:
            return False
        if other.probability is None:
            return True
        return self.probability > other.probability


def shannon_fano(nodes):
    length = len(nodes)
    # last nodes are here
    if length <= 1:
        return
    if length == 2:
        nodes[0].fano += "0"
        nodes[1].fano += "1"
        return

    # figuring out where to split the list.
    total = 0
    for i in range(length):
        total += nodes[i].probability
    second_half_total = 0
    index = length  # index - where we have to split

    while (index >= 0) and (second_half_total <= (total - second_half_total)):
        index -= 1
        second_half_total += nodes[index].probability

    diff1 = second_half_total - (total - second_half_total)
    diff2 = abs(diff1 - (2 * nodes[index].probability))
    if diff2 < diff1:
        index += 1

    # appending to code
    for j in range(index):
        nodes[j].fano += "0"

    k = index
    while k < length:
        nodes[k].fano += "1"
        k += 1

    # recursion - going to new tree branch
    if length > 0:
        shannon_fano(nodes[0:index])
        shannon_fano(nodes[index:])

    return


def main():

    ch_number = 0.0  # characters in text
    symb_dict = {}  # node instances
    symb_list = []  # symbols list

    print("Enter the filename")
    try:
        # opening file
        # - Cthulhu.txt - WhiteFang.txt - GreatExpectations.txt -
        filename = input()
        file = open(filename, 'r')

        # iterating through text
        for ch in file.read():
            # calculating symbols number
            ch_number += 1.0
            if ch in symb_dict:
                symb_dict[ch].frequency += 1.0
            else:
                new_symb = Node(ch, 0.0, 0.0, "")
                symb_dict[ch] = new_symb

        # calculating symbol probability
        for entry in symb_dict:
            symb_dict[entry].probability = symb_dict[entry].frequency / ch_number
            if symb_dict[entry].probability != 0.0:
                symb_list.append(symb_dict[entry])

        # sorting nodes list
        symb_list.sort()
        symb_list.reverse()

        # get shannon_fano encoding
        shannon_fano(symb_list)
        for i in symb_list:
            print(i)

    except IOError:
        print("No such file found")


if __name__ == '__main__':
    main()
