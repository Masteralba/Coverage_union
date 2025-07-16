from polygon import Outline, Node


def find_lines_intersection(n1, n2, q1, q2):
    
    a1 = [n1.x, n1.y]
    a2 = [n2.x, n2.y]
    b1 = [q1.x, q1.y]
    b2 = [q2.x, q2.y]

    adx = a2[0] - a1[0]
    ady = a2[1] - a1[1]
    bdx = b2[0] - b1[0]
    bdy = b2[1] - b1[1]

    axb = adx*bdy - ady*bdx

    inf = float("inf")

    ret = [axb, inf, inf, [inf, inf]]
    #cross, alongA, alongB, Point:x, y

    if (axb == 0):
        return ret

    dx = a1[0] - b1[0]
    dy = a1[1] - b1[1]

    ret[1] = (bdx*dy - bdy*dx) / axb  #Along A
    ret[2] = (adx*dy - ady*dx) / axb  #Along B

    ret[3][0] = a1[0] + ret[1]*adx
    ret[3][1] = a1[1] + ret[1]*ady

    return ret


def next_non_intersection(node):

    while(True):
        node = node.next
        if not node.intersection:
            break

    return node


#Ray-casting algorithm
def point_in_polygon(x, y, root):

    odd = False
    current = root

    #do while
    while(True):

        next = current.next

        hx = current.x
        hy = current.y
        nx = next.x
        ny = next.y

        if ((hy < y and ny >=y) or (hy >= y and ny <y) ) and (hx <=x or nx <= x) and (hx + (y-hy) / (ny-hy)*(nx-hx) < x):
            odd = not odd

        current = next
        
        if current == root:
            continue
        else:
            break

    return odd


def calculate_entry_exit(root, isEntry):

    current = root

    while(True):
        if current.intersection:
            current.isEntry = isEntry
            isEntry = not isEntry
        current = current.next
        if current != root:
            continue
        else:
            break

def find_and_insert_inter(root1, root2):

    current1 = root1    
    current2 = root2

    # Цикл по всем ребрам двух полигонов
    while(True):
        while(True):

            next1 = next_non_intersection(current1)
            next2 = next_non_intersection(current2)

            intersection = find_lines_intersection(current1, next1, current2, next2)

            #check intersection
            if (intersection[1] > 0 and intersection[1] < 1
            and intersection[2] > 0 and intersection[2] < 1):
                #intersection found
                node1 = Node(intersection[3], None, None,
                            True, intersection[1], None)
                node2 = Node(intersection[3], None, None,
                            True, intersection[2], None)
                
                node1.neighbor = node2
                node2.neighbor = node1

                #insert nodes between current and next

                inext = current1.next
                
                while(inext != next1 and inext.dist < node1.dist ):
                    inext = inext.next

                iprev = inext.prev

                inext.prev = node1
                node1.next = inext
                node1.prev = iprev
                iprev.next = node1

                inext = current2.next

                while( inext != next2 and inext.dist < node2.dist ):
                    inext = inext.next

                iprev = inext.prev

                inext.prev = node2
                node2.next = inext
                node2.prev = iprev
                iprev.next = node2

            current2 = next_non_intersection(current2)

            if current2 != root2:
                continue
            else:
                break

        current1 = next_non_intersection(current1)

        if current1 != root1:
            continue
        else:
            break


def clipping(o1, o2, into_p1=False, into_p2=False):

    root1 = o1.root
    root2 = o2.root

    # True if point in Polygon ( it is exit)
    is1in2 = point_in_polygon(root1.x, root1.y, root2)
    is2in1 = point_in_polygon(root2.x, root2.y, root1)

    find_and_insert_inter(root1, root2)

    calculate_entry_exit(root1, not is1in2)
    calculate_entry_exit(root2, not is2in1)

    result = []
    isect = root1
    into = [into_p1, into_p2]

    while(True):

        while(True):
            if isect.intersection and not isect.processed: #Возможно можно убрать проверку processed
                break
            isect = isect.next
            if isect != root1:
                continue
            else:
                break
        if isect == root1:
            break

        curpoly = 0
        clipped  = []

        current = isect

        while(True):
            #mark intersection as processed
            current.processed = True
            current.neighbor.processed = True
            moveForward = current.isEntry
            if current.isEntry == into[curpoly]:
                moveForward = True
            else:
                moveForward = False
            while(True):
                clipped.append([current.x, current.y])
                if moveForward:
                    current = current.next
                else:
                    current = current.prev
                if not current.intersection:
                    continue
                else:
                    break

            current = current.neighbor
            curpoly = 1 - curpoly
            
            if not current.processed:
                continue
            else:
                break

            

        result.append(clipped)

    return clipped


if __name__ == "__main__":

    polygon1 = [[0, 0], [0, 2], [2, 2], [2, 0]]
    polygon2 = [[1, 1], [1, 3], [3, 3], [3, 1]]

    o1 = Outline(polygon1)
    o2 = Outline(polygon2)

    print(clipping(o1, o2))

