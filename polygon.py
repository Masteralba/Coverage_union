class Node():

    def __init__(self):

        self.x = None
        self.y = None
        self.next = None
        self.prev = None
        self.intersection = False

    def __init__(self, coords, next, prev):

        self.x = coords[0]
        self.y = coords[1]
        self.next = next
        self.prev = prev

    def __str__(self):
        return f"Coords x: {self.x} y: {self.y}"

    
class Outline():

    def __init__(self):
        
        self.root = None

    def __init__(self, polygon):

        self.root = Node(polygon[0], None, None)

        current = self.root

        for i in range(1, len(polygon)):

            current.next = Node(polygon[i], None, current)

            current = current.next

        current.next = self.root
        self.root.prev = current