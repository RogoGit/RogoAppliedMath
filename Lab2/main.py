from queue import PriorityQueue


class Node:

    # A node with a symbol, frequency, probability and codes.
    # init node
    def __init__(self, symbol=None, frequency=None, probability=None, fano=None, huffman=None):
        self.symbol = symbol  # symbol itself
        self.frequency = frequency  # frequency
        self.probability = probability  # probability
        self.fano = fano  # shannon-fano code
        self.huffman = huffman  # huffman code

    def __str__(self):
        # string representation
        return "Node(" + self.symbol.__repr__() + ", " + str(self.probability) + ", " + self.fano + ", " \
               + self.huffman + ")"

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


def huffman(nodes):

    # recursion exit condition
    if len(nodes) == 2:
        return dict(zip(nodes.keys(), ["0", "1"]))

    # creating temp structure for huffman encoding
    huff_dict = nodes.copy()
    # sorting by probability ang getting 2 min
    sorted_huff_dict = sorted(nodes.items(), key=lambda node: node[1])
    min_node_one = sorted_huff_dict[0][0]
    min_node_two = sorted_huff_dict[1][0]
    prob_one = huff_dict.pop(min_node_one)
    prob_two = huff_dict.pop(min_node_two)

    huff_dict[min_node_one + min_node_two] = prob_one + prob_two
    # recursion + encoding
    huffman_code_dict = huffman(huff_dict)
    h_node = huffman_code_dict.pop(min_node_one + min_node_two)
    huffman_code_dict[min_node_one] = h_node + "0"
    huffman_code_dict[min_node_two] = h_node + "1"

    return huffman_code_dict


def main():

    ch_number = 0.0  # characters in text
    symb_dict = {}  # node instances
    symb_list = []  # symbols list
    h_dict = {}  # for huffman

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
                new_symb = Node(ch, 0.0, 0.0, "", "")
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

        # get huffman encoding
        for entry in symb_dict.keys():
            h_dict[entry] = symb_dict[entry].probability
        huffman_res = huffman(h_dict)
        print(huffman_res)

    except IOError:
        print("No such file found")


if __name__ == '__main__':
    main()
