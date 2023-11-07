import pygame
from scripts.objects import Block, Decoration
from scripts.enemies import Enemies
from scripts.trees import Tree


blocks = []
enemies = []
lands = []
tree = []
back_tree= []
decorations = []
block_size = 127

def create_map(cell, x, y):
    # NULL
    if cell == '.':
        blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[740,0], "Back"))

    # BLOCKS
    if cell == 'A': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[740,80], "Block"))
    if cell == 'Q': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[0,0], "Block"))
    if cell == 'W': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[74,0], "Grass"))
    if cell == 'E': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[148,0], "Block"))
    if cell == 'R': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[222,0], "Block"))

    if cell == 't': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[296,0], "Block"))
    if cell == 'y': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[370,0], "Block"))
    if cell == 'u': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[444,0], "Block"))
    if cell == 'i': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[518,0], "Block"))
    if cell == 'o': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[592,0], "Block"))
    if cell == 'p': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[666,0], "Block"))

    if cell == 'X': blocks.append(Block(x* block_size, y* block_size, block_size/2, block_size,[814,0], "Block"))
    if cell == 'x': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[856,0], "Block"))
    if cell == 'a': blocks.append(Block(x* block_size, y* block_size, block_size/2, block_size,[930,0], "Block"))
    if cell == '+': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[972,0], "Block"))
    if cell == '"': blocks.append(Block(x* block_size, y* block_size, block_size/2, block_size,[666,00], "Block"))


    if cell == 'T': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[0,80], "Block"))
    if cell == 'Y': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[74,80], "Block"))
    if cell == 'U': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[148,80], "Block"))
    if cell == 'I': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[222,80], "Block"))
    if cell == 'O': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[296,80], "Block"))
    if cell == 'P': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[370,80], "Block"))
    if cell == 'w': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[444,80], "Block"))
    if cell == 'q': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[518,80], "Block"))
    if cell == 'e': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[592,80], "Block"))
    if cell == 'r': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[666,80], "Block"))

    if cell == '_': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[971,80], "Block"))
    if cell == '=': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[921,161], "Block"))
    if cell == '_': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[971,80], "Block"))
    if cell == '-': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[971,161], "Block"))
    

    if cell == 'S': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[0,161], "Block"))
    if cell == 'D': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[74,161], "Block"))
    if cell == 'F': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[148,161], "Block"))
    if cell == 'G': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[222,161], "Block"))
    if cell == 'H': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[296,161], "Block"))
    if cell == 's': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[1045,161], "Block"))
    if cell == 'd': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[370,161], "Block"))
    if cell == 'f': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[1119,161], "Block"))
    if cell == 'g': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[444,161], "Block"))
    if cell == 'h': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[518,161], "Block"))
    if cell == 'j': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[1055,0], "Block"))
    if cell == 'k': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[1045,80], "Block"))
    if cell == 'l': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[592,161], "Block"))
    if cell == 'J': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[666,161], "Block"))
    if cell == 'K': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[740,161], "Block"))
    if cell == 'L': blocks.append(Block(x* block_size, y* block_size, block_size, block_size,[921,161], "Block"))
    

    # WATER AND LAV
    if cell == '@': lands.append(Block(x* block_size, y* block_size, block_size, block_size,[814,80], "Water"))
    if cell == '$': lands.append(Block(x* block_size, y* block_size, block_size, block_size,[888,80], "Lava"))


    # ENEMIES
    if cell == '1':
        enemies.append(Enemies(x*block_size, y*block_size+61, 70, 35, "Crabby",200, 0))

    if cell == '2':
        enemies.append(Enemies(x*block_size, y*block_size+61, 50, 35, "FierceTooth", 150, 70, False))

    if cell == '3':
        enemies.append(Enemies(x*block_size, y*block_size+61, 50, 35, "PinkStar", 220, 0, True, False))

    if cell == '4':
        enemies.append(Enemies(x*block_size-30, y*block_size+62, 50, 35, "Seashell", 500, 0, False, True, 2000, 3))


    # TREES
    if cell == "b":
        back_tree.append(Tree(x* block_size, y* block_size, 50, 64, "BackTree"))
    if cell == "v":
        tree.append(Tree(x* block_size, y* block_size -20, 50, 95, "FrontTree"))


    # OBJECTS
    if cell == "#":
        decorations.append(Decoration(x* block_size+30, y* block_size+105, 21, 22, "Barrel"))
    if cell == "N":
        decorations.append(Decoration(x* block_size+30, y* block_size+110, 7, 17, "Botle"))
    if cell == ",":
        decorations.append(Decoration(x* block_size+30, y* block_size+95, 32, 32, "Spike"))
    
    if cell == "<":
        decorations.append(Decoration(x* block_size +30, y* block_size+105 , 64, 25, "Chestc"))
    if cell == ">":
        decorations.append(Decoration(x* block_size+30, y* block_size +105, 64, 25, "Chesto"))

    if cell == "z":
        decorations.append(Decoration(x* block_size+30, y* block_size +100 , 24, 24, "Key"))
    