
class Triangle(object):
    """ A Triangle is encoded as the triple of the indexes of its vertices in the Vertex array"""


    def __init__(self, v1, v2, v3):
        self.__vertices = [v1, v2, v3]

    def vertices(self):
        return self.__vertices
    
    def __str__(self):
        return "Triangle(%s,%s,%s)"%(self.__vertices[0],self.__vertices[1],self.__vertices[2])
    