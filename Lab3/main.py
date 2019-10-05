class Segment:
    # segment borders for encoding
    left = 0.0  # left border
    right = 0.0  # right border


def create_segments(letters, probability):
    # defining segments
    border = 0.0
    # create segment for each letter
    segments = {}
    for letter in letters:
        segments[letter] = Segment()
    # create segment border for each letter
    for i in range(len(letters)):
        segments[letters[i]].left = border
        segments[letters[i]].right = border + probability[i]
        border = segments[letters[i]].right
    return segments


def arith_encoding(letters, probability, str_to_code):
    #  creating segments for encoding
    code_segments = create_segments(letters, probability)
    left = 0.0
    right = 1.0
    # loop for encoding symbols in interval
    for i in range(len(str_to_code)):
        symbol = str_to_code[i]  # get symbols
        # new borders
        new_right = left + (right - left) * code_segments[symbol].right
        new_left = left + (right - left) * code_segments[symbol].left
        left = new_left
        right = new_right
    #  returning some number in final interval
    return (left + right) / 2


def main():
    print("Enter the filename")
    try:

        # reading phrase from file
        filename = input()
        file = open(filename, 'r')

        phrase_to_code = file.read()  # string from file
        str_length = len(phrase_to_code)  # phrase length
        letters_set = set(list(phrase_to_code))  # get letters of phrase
        probability = [phrase_to_code.count(i) / str_length for i in letters_set]  # list of letter probabilities

        # encoding
        encoded = arith_encoding(letters=list(letters_set), probability=probability, str_to_code=phrase_to_code)
        print("Arithmetic encoding: " + str(encoded) + "\n")

    except IOError:
        print("No such file found")


main()
