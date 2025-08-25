import numpy as np

# Define basic blocks
AIR   = 0
GRASS = 1
DIRT  = 2
WOOD  = 3
LEAF  = 4

BLOCKS = {
    AIR:   {"name":"air",   "solid":False, "color":(0.0,0.0,0.0), "drop":None},
    GRASS: {"name":"grass", "solid":True,  "color":(0.40,0.70,0.35), "drop":"dirt"},
    DIRT:  {"name":"dirt",  "solid":True,  "color":(0.45,0.30,0.18), "drop":"dirt"},
    WOOD:  {"name":"wood",  "solid":True,  "color":(0.55,0.42,0.25), "drop":"wood"},
    LEAF:  {"name":"leaf",  "solid":True,  "color":(0.35,0.60,0.35), "drop":None},
}

# Face normals and corners (for meshing exposed faces)
FACE_INFO = [
    (( 1, 0, 0), [(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),  # +X
    ((-1, 0, 0), [(0,0,1),(0,1,1),(0,1,0),(0,0,0)]),  # -X
    (( 0, 1, 0), [(0,1,1),(1,1,1),(1,1,0),(0,1,0)]),  # +Y
    (( 0,-1, 0), [(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),  # -Y
    (( 0, 0, 1), [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]),  # +Z
    (( 0, 0,-1), [(0,1,0),(1,1,0),(1,0,0),(0,0,0)]),  # -Z
]

def tri_indices():
    return [(0,1,2),(0,2,3)]


class Block:
    def __init__(self, block_type="dirt"):
        self.type = block_type

    @property
    def hardness(self):
        if self.type in ("dirt", "grass", "leaves"):
            return 1
        elif self.type == "wood":
            return 2
        elif self.type == "stone":
            return 3
        return 1