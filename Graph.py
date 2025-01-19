import random

class Graph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]

    # adding edges manually
    def add_edge(self, v, w):
        self.adj[v].append(w)

    # creating random edges of the graph (initialize the number of `vertices` and `edges` before)
    def create_random_edges(self, num_edges):
        edges = set()  # To keep track of unique edges
        while len(edges) < num_edges:
            v = random.randint(0, self.V - 1)
            w = random.randint(0, self.V - 1)
            if v != w:  # Avoid self-loops
                edge = (v, w)
                if edge not in edges:  # Ensure no duplicate edges
                    edges.add(edge)
                    self.add_edge(v, w) # to store it in the `adj` attribute
 
    # visualizing the graph:
    def print_graph(self):
        for i in range(self.V):
            print(f"{i}: {self.adj[i]}")
    
    # applying depth-first search algorithm
    def dfs_util(self, v, visited):
        visited[v] = True
        for i in self.adj[v]:
            if not visited[i]:
                self.dfs_util(i, visited)

    # sets the state to `False` before running DFS
    def fill_order(self, v, stack):
        visited = [False] * self.V
        self.dfs_util(v, visited)
        stack.append(v)

    # turning the graph into a transposed one
    def get_transpose(self):
        g = Graph(self.V)
        for v in range(self.V):
            for i in self.adj[v]:
                g.adj[i].append(v)
        return g

    # checking if the graph is strongly connected
    def is_strongly_connected(self):
        stack = []

        for i in range(self.V):
            if len(self.adj[i]) > 0:
                self.fill_order(i, stack)

        transposed = self.get_transpose()

        visited = [False] * self.V
        count = 0

        while stack:
            v = stack.pop()
            if not visited[v]:
                transposed.dfs_util(v, visited)
                count += 1

        return count == 1

    # this function to check whether the `vertices` are indistinguishable or not
    def is_indistinguishable(self, u, w):
        # Check if there exists a path from u to w and from w to u
        visited_from_u = [False] * self.V
        visited_from_w = [False] * self.V

        self.dfs_util(u, visited_from_u)
        self.dfs_util(w, visited_from_w)

        return visited_from_u[w] and visited_from_w[u]

    # now implementing all above here to check whether it's "Twinless Strongly Connected"
    def is_twinless_strongly_connected(self):
        if not self.is_strongly_connected():
            return False

        # Check for indistinguishable vertices
        for v in range(self.V):
            visited = [False] * self.V
            self.dfs_util(v, visited)

            # Check for indistinguishable vertices
            reachable = [i for i in range(self.V) if visited[i]]

            # If more than one vertex is reachable, check indistinguishability
            if len(reachable) > 1:
                for u in reachable:
                    for w in reachable:
                        if u != w:
                            # Check if u and w are indistinguishable
                            if self.is_indistinguishable(u, w):
                                return False
        return True


# running the class file
if __name__ == "__main__":
    vertices = 5 # changeable
    num_edges = 10 # changeable
    g = Graph(vertices)
    g.create_random_edges(num_edges)
    g.print_graph()
    print(g.is_twinless_strongly_connected())