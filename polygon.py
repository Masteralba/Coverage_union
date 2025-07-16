class Node:

    def __init__(self):

        self.x = None
        self.y = None
        self.next = None
        self.prev = None
        self.intersection = False
        self.dist = None
        self.neighbor = None
        self.isEntry = None
        self.processed = False

    def __init__(self, coords, next, prev, intersection=False, 
                 dist=None, neighbor=None, isEntry = None, processed=False):

        self.x = coords[0]
        self.y = coords[1]
        self.next = next
        self.prev = prev
        self.intersection = intersection
        self.dist = dist
        self.neighbor = neighbor
        self.isEntry = isEntry
        self.processed = processed
        

    def str(self):
        if self.isEntry != None:
            return f"Coords x: {self.x} y: {self.y}, Intersection: {self.intersection}, isEntry: {self.isEntry}"
        else:
            return f"Coords x: {self.x} y: {self.y}, Intersection: {self.intersection}"

    
class Outline:

    def __init__(self, polygon):

        self.root = Node(polygon[0], None, None)

        current = self.root

        for i in range(1, len(polygon)):

            current.next = Node(polygon[i], None, current)

            current = current.next

        current.next = self.root
        self.root.prev = current

    def str(self):

        current = self.root
        res = str(current)
        current = current.next

        while(current != self.root):
            res += '\n' + str(current)
            current = current.next

        return res