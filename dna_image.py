# Creates an image representing all the DNA code downloaded from 23andme.
#
# Run with 'python3 dna_image.py <name_of_23andme_text_file>'
#
# An image will pop up with the results, and it will be saved as 'dna.png' in
# the current working directory. Note that this image contains all the data in
# your DNA so it should be shared with care. All the DNA data could be
# extracted from the image for processing in other ways.
#
# If not already installed, you will need both 'numpy' and 'pillow' installed.
# Easiest way is with PIP, commands are 'pip3 install numpy' and
# 'pip3 install pillow'.

from PIL import Image
import numpy as np

import math
import sys

# Converts the DNA dump from 23andme in the file named `filename` to a Python
# array of arrays of genetic code.
#
# For example:
#
# # This is a comment
# 'rs548049170	1	69869	TT'
# 'rs9283150	1	565508	AA'
#
# turns into
#
# [['rs548049170', '1', '69869', 'TT'],
# ['rs9283150', '1', '565508', 'AA']]
def get_dna_data(filename):
    data = []
    with open(filename) as dna:
       for line in dna:
           if line.startswith('#'):
               continue
           data.append(line.rstrip('\n').split('\t'))
    return data

# Converts raw gene data into just the genetic letters (A, T, C, or G) in the
# left or right side of the chromosome.
#
# `data` is the array of arrays from get_dna_data()
# `name` is the name of the chromosome such as '1', '2', 'X', 'Y', or 'MT'
# `left` is a boolean on whether to retrieve the left or right chromosome
# ``
def get_chromosome_letters(data, name, left):
    chromosome = []
    for dna in data:
        if dna[1] == name:
            chromosome.append(dna)
    letters = []
    for dna in chromosome:
        # Some chromosomes have no match on the right side so have only one
        # letter in the raw data. Replace it with a '-' here to make further
        # processing simpler.
        if not left and len(dna[3]) == 1:
            letters.append('-')
        else:
            letters.append(dna[3][0 if left else 1])
    return letters

# Converts a genetic letter to a color for the image to be drawn in RGB format.
#
# A -> Red
# T -> Green
# C -> Blue
# G -> Yellow
# Missing or no match data -> Black
def letter_to_color(letter):
    if letter == 'A':
        return [255, 0, 0]
    elif letter == 'T':
        return [0, 255, 0]
    elif letter == 'C':
        return [0, 0, 255]
    elif letter == 'G':
        return [255, 255, 0]
    return [0, 0, 0]

# Converts all the genetic letters corresponding to a chromosome into square
# array colors for converting to an image later.
def letters_to_colors(letters):
    size = math.ceil(math.sqrt(len(letters)))
    colors = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(len(letters)):
        colors[(i // size), (i % size)] = letter_to_color(letters[i])
    return colors

# Combines the left and right sides of a chromosome into one image.
def combined_chromosome_colors(data, name):
    left = letters_to_colors(get_chromosome_letters(data, name, True))
    right = letters_to_colors(get_chromosome_letters(data, name, False))
    # Put a vertical line of black to differentiate the two sides in the image.
    split = np.zeros((left.shape[0], 1, 3), dtype=np.uint8)
    return np.concatenate((left, split, right), axis=1)

# Combines two images of possibly differing sizes by stacking one top of the
# other vertically and expanding with black to fill in the gaps.
#
# For example:
#
#             ABC
#  ABC   JK   DEF
#  DEF + LM = GHI
#  GHI        JK-
#             LM-
def combine_images(image_one, image_two):
    new_height = image_one.shape[0] + image_two.shape[0]
    new_width = max(image_one.shape[1], image_two.shape[1])
    combined = np.zeros((new_height, new_width, 3), dtype=np.uint8)
    # Fill in 0 -> image_one height and 0 -> image_one width for image one.
    combined[:image_one.shape[0], :image_one.shape[1]] = image_one
    # Fill in image_one height -> new height and 0 -> image_two width with
    # image_two.
    combined[image_one.shape[0]:new_height, :image_two.shape[1]] = image_two
    return combined


# Converts all the DNA data into one 3 dimensional array of colors organized by
# chromosomes (1, 2, ..., 22, X, Y, MT).
def chromosome_colors(data):
    print("Processing chromosome... 1")
    colors = combined_chromosome_colors(data, '1')
    chromosomes = [str(c) for c in range(2, 23)] + ['X', 'Y', 'MT']
    for chromosome in chromosomes:
        print("Processing chromosome... %s" % chromosome)
        colors = combine_images(colors,
                                combined_chromosome_colors(data, chromosome))
    return colors

# Hooks everything together.
#
# Get DNA from file -> convert to an image array -> draw it.
def main():
    image = Image.fromarray(chromosome_colors(get_dna_data(sys.argv[1])), 'RGB')
    image.save('dna.png')
    image.show()

if __name__ == '__main__':
    main()
