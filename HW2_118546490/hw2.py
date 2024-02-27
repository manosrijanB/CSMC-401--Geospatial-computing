
import numpy as np
import copy

class Node:
    def __init__(self):
        self.NodeType = None
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None
        
    def init_children(self):
        self.NW = Node()
        self.NE = Node()
        self.SW = Node()
        self.SE = Node()


def BuildTree(r, image, cur_col, cur_row, L, label = 0):
    # when there is only one pixel left in the block
    if L == 1:
        # set the NodeType based on the pixel value
        r.NodeType = image[cur_col][cur_row]
        return
    else:
        color = image[cur_col][cur_row]
        # visit other pixels in the current block in sequence
        cur_block = image[cur_col:cur_col+L, cur_row:cur_row+L]
        for pixel in cur_block.flatten():
            if pixel != color:  # the current block needs to be split
                # add four children to the current node corresponding to four sub-blocks                
                print("FIND a pixel with different value at", cur_col, cur_row,
                      "Split block", label)
                r.NW = Node()
                r.NE = Node()
                r.SW = Node()
                r.SE = Node()
                r.NodeType = 2
                j = 1
                # for each child of root, call BuildTree function
                for i, child in zip(['NW', 'NE', 'SW', 'SE'], [r.NW, r.NE, r.SW, r.SE]):
                    # corner_col and corner_row are the coordinates of the upper-left corner of the sub-block
                    if i == 'NW':
                        corner_col, corner_row = cur_col, cur_row
                    elif i == 'NE':
                        corner_col, corner_row = cur_col, cur_row+L//2
                    elif i == 'SW':
                        corner_col, corner_row = cur_col+L//2, cur_row
                    else:
                        corner_col, corner_row = cur_col+L//2, cur_row+L//2
                    BuildTree(child, image, corner_col, corner_row, L//2, 4*label + j)
                    j += 1
                return
        r.NodeType = color

chr = ['White', 'Black', 'Gray']

def Preorder(n, index  = 0):
    if n is None or n.NodeType is None:
        return
    else:
        print(f"{index} {chr[n.NodeType]}")
        Preorder(n.NW, index * 4 + 1)
        Preorder(n.NE, index * 4 + 2)
        Preorder(n.SW, index * 4 + 3)
        Preorder(n.SE, index * 4 + 4)


def Intersection(s, t, label = 0):
    if s is None or t is None:
        return Node()
    q = Node()
    if s.NodeType == 0 or t.NodeType == 0:
        q.NodeType = 0
        print(label, chr[s.NodeType], chr[t.NodeType], chr[q.NodeType])
    elif s.NodeType == 1:
        q = copy.deepcopy(t)
        print(label, chr[s.NodeType], chr[t.NodeType], chr[q.NodeType])
    elif t.NodeType == 1:
        q = copy.deepcopy(s)
        print(label, chr[s.NodeType], chr[t.NodeType], chr[q.NodeType])
    else:
        q.NodeType = 2
        print(label, chr[s.NodeType], chr[t.NodeType], chr[q.NodeType])
        q.NW = Intersection(s.NW, t.NW, 4*label + 1)
        q.NE = Intersection(s.NE, t.NE, 4*label + 2)
        q.SW = Intersection(s.SW, t.SW, 4*label + 3)
        q.SE = Intersection(s.SE, t.SE, 4*label + 4)
        if q.NW.NodeType == 0 and q.NE.NodeType == 0 and q.SW.NodeType == 0 and q.SE.NodeType == 0:
            q.NodeType = 0
            print(label, chr[s.NodeType], chr[t.NodeType], chr[q.NodeType])
            q.init_children()
    return q



# Define a function to create a binary image from a window and the size of the original image
def create_window_image(window, size):
    image = [[0 for j in range(size)] for i in range(size)]
    for i in range(window[0][0], window[1][0] + 1):
        for j in range(window[0][1], window[1][1] + 1):
            if i >= 0 and i < size and j >= 0 and j < size:
                image[i][j] = 1
    return image



def readImage(filename):
    image = []
    with open(filename) as f:
        content = f.readlines()
        for line in content[1:]:
            image.append([int(x) for x in line.strip().split() if x])
    return np.array(image)


image1 = input("Enter the name of the first image file: ")
image1 = readImage(image1)
image2 = input("Enter the name of the second image file: ")
image2 = readImage(image2)

# Build the tree
print("START INPUT")
L1 = len(image1)
A = Node()
BuildTree(A, image1, 0, 0, L1)
print('SPLIT COMPLETED')

# Print the tree
print("START RQ")
Preorder(A, 0)
print("END RQ")

# bulid tree for image2

L2 = len(image2)
B = Node()
BuildTree(B, image2, 0, 0, L2)

# test intersection
print("START INTERSECTION")
Q = Intersection(A, B)
print("END INTERSECTION")

im2 = create_window_image([[0, 0], [2, 2]], L1)
B = Node()
BuildTree(B, np.array(im2), 0, 0, L1)


# Print the tree
print("START RQ")
Preorder(Q, 0)
print("END RQ")

