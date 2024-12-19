"""
Demo.
Authors:
Xin Xu: xinxu629@umd.edu
Yunting Song: ytsong@terpmail.umd.edu 
Mar-04-2022
"""
import sys
import os

from reader import Reader

from tin import TIN
from tree import Tree
from point import Point

# generate TIN
from scipy.spatial import Delaunay 

# plot
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib.ticker import LinearLocator, FormatStrFormatter


def generate_TIN(pts_file):
    '''
    Generate TIN from input point file.
    Return
    tin_file: name of TIN .off file
    points1: updated 2D points (x,y). each pair of (x,y) is unique
    zs1: updated z values of points, in the same order of points1
    tris: triangles of TIN. each triangle is saved as [vid1, vid2, vid3]. vid is point index based on points1
    '''
    points = np.empty(shape=[0, 2])
    with open(pts_file) as infile:
        lines_num= infile.readline().strip()
        lines_num=int(lines_num)
        zs = list()
        for l in range(lines_num):
            line = (infile.readline()).split()
            v1 = float(line[0])
            v2 = float(line[1])
            zs.append(float(line[2])) 
            points = np.append(points, [[v1,v2]], axis=0)
    
    triangles = Delaunay(points) 
    
    tris = np.empty(shape=[0, 3])
    used_pts = set()
    for tri in triangles.simplices:
        used_pts.add(tri[0])
        used_pts.add(tri[1])
        used_pts.add(tri[2])
    o2n = dict()
    zs1 = list()
    points1= np.empty(shape=[0, 2])
    for pid in used_pts:
        points1 = np.append(points1,[[points[pid][0], points[pid][1]]],axis=0)
        o2n[pid] = len(points1)-1
        zs1.append(zs[pid])

    for tri in triangles.simplices:
        v1 = tri[0]
        v2 = tri[1]
        v3 = tri[2]
        nv1 = o2n[v1]
        nv2 = o2n[v2]
        nv3 = o2n[v3]
        tris = np.append(tris,[[nv1, nv2, nv3]],axis=0)
   
   # output TIN file, Note:  you can rename the file name
    tin_file = "pts-dt.off"
    with open(tin_file,'w') as ofs:
        ofs.write("OFF\n")
        ofs.write("{} {} 0\n".format(len(points1), len(tris)))
        for pid in range(len(points1)):
            ofs.write("{} {} {}\n".format(points1[pid][0], points1[pid][1],zs1[pid]))
        for tri in tris:
            ofs.write("3 {} {} {}\n".format(int(tri[0]), int(tri[1]), int(tri[2])))
    return tin_file, points1, zs1, tris


def plot_tin_with_marks(xs,ys,zs,tris,vals,mxs,mys,mzs,filename="test"):
    """
    Plot TIN 3D with markers. TIN is colored  based on values of each triangle. The triangle value is the  average value of 3 extreme points.
    Inputs:
    xs,ys,zs: lists of the same size. Point i
    (xs[i],ys[i], zs[i]) represents a point
    tris: np.array. triangles. each triangle is represented as [vid1, vid2, vid3]. vid is point index.
    vals: list. values of points with the same order as points.
    mxs,mys,mzs: lists. Marker i
    (mxs[i],mys[i], mzs[i]) represents a marker
    filename: output figure name.
    """
    tri_avg = []
    for tri in tris:
        v1 = vals[int(tri[0])]
        v2 =  vals[int(tri[1])]
        v3 =  vals[int(tri[2])]
        v  = (v1+ v2 + v3) / 3
        tri_avg.append(v)
    vals_np = np.array(vals)
    zs_np = np.array(zs)
    triang = mtri.Triangulation(xs, ys, tris)
    maskedTris = triang.get_masked_triangles()
    xt = triang.x[maskedTris]
    yt = triang.y[maskedTris]
    zt = zs_np[maskedTris]
    verts = np.stack((xt, yt,zt), axis=-1)
    norm = cm.colors.Normalize(vmin=min(tri_avg), vmax=max(tri_avg))
    nm = norm(tri_avg)
    
    my_col = cm.jet(nm)
    newcmp = cm.colors.ListedColormap(my_col)
    
    collection = Poly3DCollection(verts)
    collection.set_facecolor(my_col)

    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(projection='3d')
    
    ax.add_collection(collection)
    # add markers
    
    ax.scatter(mxs, mys, mzs, c='r', marker='^', s = 40)
    
    ax.set_title(filename)
    ax.set_xlim3d(min(xs), max(xs))
    ax.set_xlabel('X')
    ax.set_ylim3d(min(ys), max(ys))
    ax.set_ylabel('Y')
    ax.set_zlim3d(min(zs), max(zs))
    ax.set_zlabel('Z')
    ax.autoscale_view()
    
    m = cm.ScalarMappable(cmap=cm.jet, norm=norm)
    m.set_array([])
    fig.colorbar(m, ax=ax, location = 'left')
    
    # output tin figure
    plt.savefig(filename+".png", dpi=96)
    plt.show()


    
def read_tin_and_generate_tree(reader, tin_file, capacity):
        tin = reader.read_tin_file(tin_file)
        tree = Tree(int(capacity))
        tree.build_tree(tin)
        return tin, tree

def calculate_and_save_roughness(tin, tree):
    tree.traverse_tree(tin)
    roughness = []
    with open("roughness.txt", 'w') as ofs:
        for i in range(tin.get_vertices_num()):
            vertex = tin.get_vertex(i)
            ofs.write("{} {}\n".format(i, vertex.get_field(1)))
            roughness.append(vertex.get_field(1))
    return roughness

def calculate_and_save_curvature(tin, tree):
    tree.traverse_tree_for_curvature(tin)
    curvature = []
    with open("curvature.txt", 'w') as ofs:
        for i in range(tin.get_vertices_num()):
            vertex = tin.get_vertex(i)
            ofs.write("{} {}\n".format(i, vertex.get_field(2)))
            curvature.append(vertex.get_field(2))
    return curvature

def find_and_save_maximas(tin, tree):
    maximas = tree.traverse_tree_for_maximas(tin)
    with open("maximas.txt", 'w') as ofs:
        ofs.write("{}\n".format(len(maximas)))
        for i in range(len(maximas)):
            ofs.write("{}\n".format(maximas[i]))
    return maximas

def main():
    tin_file, pts, zs, tris = generate_TIN(sys.argv[1])
    plot_tin_with_marks(pts[:,0], pts[:,1], zs, tris, zs, [], [], [], "tin-og")

    reader = Reader()
    tin, tree = read_tin_and_generate_tree(reader, tin_file, sys.argv[2])
    tree.preorder()

    roughness = calculate_and_save_roughness(tin, tree)
    plot_tin_with_marks(pts[:,0], pts[:,1], zs, tris, roughness, [], [], [], "roughness")

    curvature = calculate_and_save_curvature(tin, tree)
    plot_tin_with_marks(pts[:,0], pts[:,1], zs, tris, curvature, [], [], [], "curvature")

    maximas = find_and_save_maximas(tin, tree)
    mxs, mys, mzs = [], [], []
    for i in range(len(maximas)):
        vertex = tin.get_vertex(maximas[i])
        mxs.append(vertex.get_c(0))
        mys.append(vertex.get_c(1))
        mzs.append(vertex.get_z())

    plot_tin_with_marks(pts[:,0], pts[:,1], zs, tris, zs, mxs, mys, mzs, "maximas")

if __name__ == "__main__":
    main()


