import sys
from node import Node
from domain import Domain
from tin import TIN
from point import Point

import math
import numpy as np
import matplotlib.pyplot as plt

class Tree(object):
    '''Creates Class tree'''
    def __init__(self,c):
        self.__root = Node()
        self.__capacity = c

    def get_root(self):
        return self.__root

    def get_leaf_threshold(self):
        return self.__capacity

    def build_tree(self,tin):
        # first we insert the vertices of the TIN
        for i in range(tin.get_vertices_num()):
            print ("INSERT POINT %s"%tin.get_vertex(i))  ## you can use this line to check the vertex input. Can comment it out if you don't need it.
            self.insert_vertex(self.__root,0,tin.get_domain(),i,tin)
        # ADD THE CODE for inserting its triangles
        for i in range(tin.get_triangles_num()):
            triangle = tin.get_triangle(i)
            print("INSERT TRIANGLE %i - %s" % (i, triangle))
            for v_index in triangle.vertices():
                node = self.point_query(self.__root, 0, tin.get_domain(), tin.get_vertex(v_index), tin)
                if i not in node.get_triangles():
                    node.add_triangle(i)
        self.preorder()
        #  End of the build_tree() function

    def insert_vertex(self,node,node_label,node_domain,v_index,tin):
        if node_domain.contains_point(tin.get_vertex(v_index),tin.get_domain().get_max_point()):
            if node.is_leaf():
                if node.is_duplicate(v_index,tin): # if the inserting vertex is the same as one vertex in the tree.
                    return                          # do not insert it
                node.add_vertex(v_index) #update append list
                if node.overflow(self.__capacity):
                    # WE HAVE TO PERFORM A SPLIT OPERATION WHEN THE NUMBER OF VERTICES EXCEED CAPACITY
                    # current node become internal, and we initialize its children
                    node.init_children()
                    for i in node.get_vertices():
                        self.insert_vertex(node,node_label,node_domain,i,tin)
                    node.reset_vertices() # empty the list of the current node

            else: # otherwise we are visiting an INTERNAL node
                mid_point = node_domain.get_centroid()
                for i in range(4):
                    s_label,s_domain = node.compute_child_label_and_domain(i,node_label,node_domain,mid_point)
                    self.insert_vertex(node.get_child(i),s_label,s_domain,v_index,tin)

    def point_query(self, node, node_label, node_domain, search_point, tin):
        # node: Node object; node_label: int; node_domain: Domain object;search_point: Vertex object, the vertex you want to search
        # when point_query used in other functions for searching point:
        # node is the root of the tree,node_label is the node label of the root node(0), node_domain is the domain of the TIN(tin.get_domain()).
        # You will use this for identifying nodes containing the extreme vertices of a triangle
        #
        # This function will return the node that contains the input search_point.
        if node_domain.contains_point(search_point, tin.get_domain().get_max_point()):
            if node.is_leaf():
                isfound = False
                x = None  # x is the point id
                for i in node.get_vertices():  # for each point index in each node, if that point is equal to the query point, then it is found. Otherwise, it is not found.
                    if tin.get_vertex(i) == search_point: # here tin.get_vertex(i) and search_point are Vertex objects
                        isfound = True
                        x = i  # x is the point index that is equal to the search point.
                        print("Vertex "+str(x)+" is in Node "+str(node_label))
                        break
                if isfound:
                    return node
                else:
                    return None
            else:  # Internal node
                ### we visit the children in the following order: NW -> NE -> SW -> SE
                mid_point = node_domain.get_centroid()
                s_label, s_domain = node.compute_child_label_and_domain(0, node_label, node_domain, mid_point)
                ret_node = self.point_query(node.get_child(0), s_label, s_domain, search_point, tin)
                if ret_node is not None:
                    return ret_node
                else:
                    s_label, s_domain = node.compute_child_label_and_domain(1, node_label, node_domain, mid_point)
                    ret_node = self.point_query(node.get_child(1), s_label, s_domain, search_point, tin)
                    if ret_node is not None:
                        return ret_node
                    else:
                        s_label, s_domain = node.compute_child_label_and_domain(2, node_label, node_domain, mid_point)
                        ret_node = self.point_query(node.get_child(2), s_label, s_domain, search_point, tin)
                        if ret_node is not None:
                            return ret_node
                        else:
                            s_label, s_domain = node.compute_child_label_and_domain(3, node_label, node_domain, mid_point)
                            ret_node = self.point_query(node.get_child(3), s_label, s_domain, search_point, tin)
                            return ret_node



    def get_points(self, tin, pts):
        """return xs,ys"""
        xs = list()
        ys = list()
        for v in pts:
            xs.append(tin.get_vertex(v).get_x())
            ys.append(tin.get_vertex(v).get_y())
        return xs,ys

    def get_pts_feature_values(self,tin, fid):
        vals=list()
        for v in range(tin.get_vertices_num()):
            ver = tin.get_vertex(v)
            #print(ver, fid,ver.get_fields_num() )
            #ver.print_fields()
            if fid >= ver.get_fields_num():
                sys.exit()
            else:
                vals.append(ver.get_field(fid))
        return vals

    def preorder(self, node = None, node_label=0):
        if node is None:
            node = self.__root
        print("\nSTART TRIANGLE PR")
        if node.is_leaf():
            if node.get_vertices_num() == 0:
                print(node_label, "EMPTY LEAF")
            elif node.get_vertices_num() == self.__capacity:
                print(node_label, "FULL LEAF")
                print("V", node.get_vertices_num(), node.get_vertices())
                print("T", len(node.get_triangles()), node.get_triangles())
            else:
                print(node_label, "FULL LEAF")
                print("V", node.get_vertices_num(), node.get_vertices())
                print("T", len(node.get_triangles()), node.get_triangles())
        else:
            print(node_label, "INTERNAL")
            for i in range(4):
                self.preorder(node.get_child(i), node_label*4+i+1)
        print("END TRIANGLE PR")

 
    def calculate_roughness(self, tin, node):
        for v_index in node.get_vertices():
            vertex = tin.get_vertex(v_index)
            vertices = [tin.get_vertex(i) for i in node.get_vertex_neighborhood(v_index, tin)]
            k = len(vertices)
            elevation_avg = sum([v.get_z() for v in vertices]) / k
            squared_elevation_diff_sum = sum([(v.get_z() - elevation_avg)**2 for v in vertices])
            roughness = np.round((squared_elevation_diff_sum / k) ** 0.5, 2)
            vertex.add_field(roughness)

    def traverse_tree(self, tin, node=None):
        if node is None:
            node = self.__root

        if node.is_leaf():
            self.calculate_roughness(tin, node)
        else:
            for i in range(4):
                self.traverse_tree(tin, node.get_child(i))

    def calculate_curvature(self, tin, node):
        for v_index in node.get_vertices():
            vertex = tin.get_vertex(v_index)
            neighbor_triangles = node.get_vertex_triangle_neighborhood(v_index, tin)
            angle_sum = 0
            boundary_vertices = set()
            for t_index in neighbor_triangles:
                triangle = tin.get_triangle(t_index)
                vertices = list(triangle.vertices())
                vertices.remove(v_index)
                v1 = tin.get_vertex(vertices[0])
                v2 = tin.get_vertex(vertices[1])
                angle_sum += self.angle(v1, vertex, v2)

                for v in vertices:
                    if v in boundary_vertices:
                        boundary_vertices.remove(v)
                    else:
                        boundary_vertices.add(v)

            k = len(boundary_vertices)
            if k == 0:
                curvature = np.round(np.pi - angle_sum, 2)
            else:
                curvature = np.round(2 * np.pi - angle_sum, 2)
            vertex.add_field(curvature)

    def traverse_tree_for_curvature(self, tin, node=None):
        if node is None:
            node = self.__root

        if node.is_leaf():
            self.calculate_curvature(tin, node)
        else:
            for i in range(4):
                self.traverse_tree_for_curvature(tin, node.get_child(i))

    def angle(self, v1, v2, v3):
        V_21 = [v1.get_c(0)-v2.get_c(0),v1.get_c(1)-v2.get_c(1),v1.get_z()-v2.get_z()]
        V_23 = [v3.get_c(0)-v2.get_c(0),v3.get_c(1)-v2.get_c(1),v3.get_z()-v2.get_z()]
        cos_angle = np.dot(V_21, V_23) / (np.sqrt(np.dot(V_21, V_21)) * np.sqrt(np.dot(V_23, V_23)))
        angle = np.arccos(cos_angle)
        return angle

    def find_local_maximas(self, tin, node):
        maxima_vertices = []

        for v_index in node.get_vertices():
            vertex = tin.get_vertex(v_index)
            neighborhood_vertices = node.get_vertex_neighborhood(v_index, tin)
            neighborhood_vertices.remove(v_index)
            is_maximum = True
            for neighbor_v_index in neighborhood_vertices:
                neighbor_vertex = tin.get_vertex(neighbor_v_index)
                if neighbor_vertex.get_z() >= vertex.get_z():
                    is_maximum = False
                    break
            if is_maximum:
                maxima_vertices.append(v_index)

        return maxima_vertices

    def traverse_tree_for_maximas(self, tin, node=None):
        if node is None:
            node = self.__root

        maxima_vertices = []

        if node.is_leaf():
            maxima_vertices.extend(self.find_local_maximas(tin, node))
        else:
            for i in range(4):
                maxima_vertices.extend(self.traverse_tree_for_maximas(tin, node.get_child(i)))

        return maxima_vertices





       
