#################################################################
#                                                               #
#    Define any helper functions you need in this file only.    #
#    You will be handing in HyperSudoku.py, nothing else.       #
#                                                               #
#    A few test cases are provided in Test.py. You can test     #
#    Your code by running: (See the file for more details)      #
#               python Test.py                                  #
#    in the directory where the files are located.              #
#                                                               #
#    We're using Python 3.X this time.                          #
#                                                               #
#################################################################


class HyperSudoku:

    @staticmethod
    def solve(grid):
        """
        Input: An 9x9 hyper-sudoku grid with numbers [0-9].
                0 means the spot has no number assigned.
                grid is a 2-Dimensional array. Look at
                Test.py to see how it's initialized.

        Output: A solution to the game (if one exists),
                in the same format. None of the initial
                numbers in the grid can be changed.
                'None' otherwise.
        """
        (graph, boxes, head) = HyperSudoku.create_vertex(grid)
        
        HyperSudoku.create_edge(graph, boxes)
        
        boo = HyperSudoku.solvev(head)
        if not boo:
            return None
        else:
            cur = head
            while cur is not None:
                (i, j) = cur.xy
                value = cur.value
                grid[i][j] = value
                cur = cur.nextv
            return grid
        

    @staticmethod
    def printGrid(grid):
        """
        Prints out the grid in a nice format. Feel free
        to change this if you need to, it will NOT be 
        used in marking. It is just to help you debug.

        Use as:     HyperSudoku.printGrid(grid)
        """
        print("-"*25)
        for i in range(9):
            print("|", end=" ")
            for j in range(9):
                print(grid[i][j], end=" ")
                if (j % 3 == 2):
                    print("|", end=" ")
            print()
            if (i % 3 == 2):
                print("-"*25)

    @staticmethod
    def create_vertex(grid):
        """
        For each entry in the grid, we create a vertex for it and put them
        into a graph (a 2D matrix), and group them into 13 boxes and also link
        the vertices whoes values are unassigned.
        
        return (graph, boxes, head)
        """
        # initiate boxes
        boxes = []
        for box in range(13):
            boxes.append([])
    
        # initiate graph
        graph = []
        for a in range(9):
            graph.append([])
            for b in range(9):
                graph[a].append(None)

        # initiate a linked list
        head = None
        cur = None

        # read from grid then construct the graph and boxes
        for i in range(9):
            for j in range(9):
                # create a vertex
                value = grid[i][j]
                vertex = HyperSudoku.Vertex(value)
                vertex.xy = (i, j)
                graph[i][j] = vertex
                
                # link the unassigned vertex
                if value == 0:
                    if head is None:
                        head = vertex
                        cur = vertex
                    else:
                        cur.nextv = vertex
                        cur = vertex
                # put the vertex in one of the regular boxes
                box_num = -1
                if 0 <= i <= 2:
                    if 0 <= j <= 2:
                        box_num = 0
                    elif 3 <= j <= 5:
                        box_num = 1
                    else:
                        box_num = 2
                elif 3 <= i <= 5:
                    if 0 <= j <= 2:
                        box_num = 3
                    elif 3 <= j <= 5:
                        box_num = 4
                    else:
                        box_num = 5
                else:
                    if 0 <= j <= 2:
                        box_num = 6
                    elif 3 <= j <= 5:
                        box_num = 7
                    else:
                        box_num = 8
                boxes[box_num].append(vertex)
                vertex.box_nums.add(box_num)
                # put the vertex in an additional box if needed
                if 1 <= i <= 3 and 1 <= j <= 3:
                    box_num = 9
                elif 5 <= i <= 7 and 1 <= j <= 3:
                    box_num = 10
                elif 1 <= i <= 3 and 5 <= j <= 7:
                    box_num = 11
                elif 5 <= i <= 7 and 5 <= j <= 7:
                    box_num = 12
                # check whether the vertex need to be put in an addtional box
                if box_num >= 9:
                    boxes[box_num].append(vertex)
                    vertex.box_nums.add(box_num)                    
        return (graph, boxes, head)

    @staticmethod
    def create_edge(graph, boxes):
        """
        create edges for each vertex in the graph, such that a vertex will
        connect to all other vertices that within the same row, column and
        boxes as it.
        """
        for i in range(9):
            for j in range(9):
                vertex = graph[i][j]
                # connect in same row and column
                for c in range(j+1, 9):
                    vertex.connect(graph[i][c])
                for r in range(i+1, 9):
                    vertex.connect(graph[r][j])
                # connect in same box
                for bnum in vertex.box_nums:
                    box = boxes[bnum]
                    for v in box:
                        vertex.connect(v)

    @staticmethod
    def solvev(vertex):
        """
        Get the solution by DFS, try a option for a vertex A, then go to the
        next vertex B, if an error ocurr, BACK TRACE to A and try another
        option, otherwise go to the next vertex again to C till end.
        """
        # get possible options for vertex
        adjacent_value = set()
        for av in vertex.adjacent_vertices:
            adjacent_value.add(av.value)
        all_options = {1,2,3,4,5,6,7,8,9}
        options = all_options.difference(adjacent_value)
        # try for each option
        while len(options) > 0:
            value = options.pop()
            vertex.value = value
            # if got an answer, return true
            if (vertex.nextv is None) or (HyperSudoku.solvev(vertex.nextv)):
                return True
            # otherwise, try another solution
        # if all options don't work, recover the value to 0 and back track
        vertex.value = 0
        return False

    
    class Vertex():
        
        def __init__(self, value):
            self.value = value
            self.adjacent_vertices = set()
            self.box_nums = set()
            self.nextv = None
            self.xy = None
        
        def connect(self, vertex):
            self.adjacent_vertices.add(vertex)
            vertex.adjacent_vertices.add(self)


if __name__ == "__main__" :
    grid = [[0, 0, 6, 0, 9, 4, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 8, 9, 0],
            [1, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 9, 0, 5, 0, 2, 0],
            [3, 0, 0, 0, 2, 0, 0, 0, 7],
            [6, 0, 3, 0, 0, 0, 0, 7, 0],
            [0, 9, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0]]
    
    sln = HyperSudoku.solve(grid)
    HyperSudoku.printGrid(sln)