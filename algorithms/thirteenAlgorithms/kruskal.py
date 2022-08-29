# https://www.youtube.com/watch?v=Yo7sddEVONg&t=78s:

# 1. Sort edges such that smaller weights are prioritised. Pick the lowest-cost edge; if there are multiple such edges,
# then it might be a good idea to choose between them
# randomly, but using a probability distribution in which edges connecting to nodes with higher degrees (more
# neighbours) are more likely to be chosen, since in many real-world solutions such nodes tend to receive more new
# neighbours than less connected ones, meaning you would want the minimum spanning tree to connect high-degree nodes
# two-way rather than leaving them as leaves, for example.

# 2. Make sure the edge picked doesn't create any cycles in MST.
# According to https://www.programiz.com/dsa/kruskal-algorithm, the most common way of avoiding cycles is using Union
# Find. This divides vertices into clusters and lets us check if the two vertices in the edge we are considering belong
# to the same cluster, in which case adding the edge would create a cycle in the MST.
# The Union-Find method here works like this:
# -> See C:\Users\james\postgradPycharm\dataStructures\unionFind\williamFiset.py
# -> Right off the bat, make a set for each vertex in the graph, where the set contains this vertex.
# -> When considering an edge connects u and v, then if u and v belong to the same set, don't add this edge to the MST;
# otherwise, add this edge to the MST and perform the union of the sets that u and v are currently in, so that you
# get a new set containing both the original sets.
# -> Do the above for every edge in the graph.

# 3. Keep selecting the remaining lowest-weight edges that don't violate the MST until the MST contains all the nodes
# from the graph. The number of edges to be selected in total must be V-1, as necessary for a MST.

# Can run at O(Elog(V)) with binary heaps.

# May run a little vaster with Fibonacci heap O(E + Vlog(V)) if V is much smaller than E--this is because Vlog(V) has
# a higher order of growth than E, so if E is similar to V, this tends to O(E + Vlog(V)) instead of being closer to
# O(E), which would be expected to be worse than O(Elog(V)), especially since E and V are similar.

# IN CODE BELOW:

# Sorting takes O(Elog(E)) time. Afterwards, iterate through all edges (of which there are E) and apply the find-union
# algorithm, whose find and union operations can take at most O(log(V)) time (so Elog(V)) in total, so sorting and then
# iterating through the edges takes O(Elog(E) + Elog(V)) time; E can be at most V**2, so O(logV) and O(logE) are the
# same--therefore, overall time complexity can be said to be either O(ElogE) or O(ElogV).

# Auxiliary space: O(V + E), which can be simplified to O(E) for similar reasoning to above.


class Graph:
    """https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/

    Time complexity: O(ElogE) == O(ElogV)
    Auxiliary complexity: O(V + E) == O(V) == O(E)
    """

    def __init__(self, vertices):
        self.v = vertices   # Number of vertices
        self.graph = [] # Default dictionary to store graph

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    # Utility function to find set of an element i (uses path compression technique)
    # See https://www.youtube.com/watch?v=VHRhJWacxis for path compression
    def find(self, parent, i):
        """I think that parent could be like the array in 6:40 of https://www.youtube.com/watch?v=0jNmHPfA_yE: an array
        in which the index of each position is mapped to by the label of a node in a graph, and the element at this
        index position is simply the index number of the node's parent. So, in recursion, you keep passing in "parent"
        because you want to get to the position in the array where the element is equal to the index, as this means the
        parent of the node represented by the index is itself--therefore, we have the root.
        """
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        """When comparing two nodes mapped to index numbers x and y, this function finds the roots of their groups and
        makes one the parent of the other, based on the rank of each. Rank is a mapping of each root to a "rank"; here,
        the root with the higher rank becomes the parent of that with the lower rank. See 'find' function description
        for what 'parent' is.
        """
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot

        # If the ranks are the same, then make one of the roots (arbitrarily choosing xroot here) the root of the union
        # and increment this node's rank by 1.
        else:
            parent[yroot] = xroot
            # todo: find out if you really need to do the rank incrementation shown below
            rank[xroot] += 1

    def kruskalMST(self):
        """Finds a minimum spanning tree in this graph using Kruskal's algorithm."""

        mst = []

        # Step 1: sort all edges in ascending order (i.e. smallest one first) of weight. Creating a new graph in case
        # not allowed to modify the given graph. Creation is O(V + E).
        self.graph = sorted(self.graph,
                            # Remember, graph contains lists items of format [u, v, w], by virtue of add_edge, where
                            # item[2] would be w (weight)
                            key=lambda item: item[2])

        parent = []
        rank = []

        # Create v number of subsets with single elements
        for node in range(self.v):
            parent.append(node) # Remember, this is just an integer in the range [0, v)
            rank.append(0)

        i = 0   # Index variable used for sorted edges
        e = 0   # Index variable used for mst[]
        # Number of edges in MST will necessarily be equal to V-1
        while e < self.v - 1:

            # Step 2: pick the smallest edge and increment the index for the next iteration
            u, v, w = self.graph[i]
            i += 1

            # If including this edge doesn't cause a cycle (i.e. if u and v belong to different groups), include it in
            # result, increment 'e' for the next edge, and unify u's and v's groups.
            x = self.find(parent, u)
            y = self.find(parent, v)
            if not x == y:
                e += 1
                mst.append([u, v, w])
                self.union(parent, rank, x, y)

        minimum_cost = 0
        print('Edges in the constructed MST:')
        for u, v, weight in mst:
            minimum_cost += weight
            print('%d -- %d: weight == %d' % (u, v, weight))
        print(f"Minimum spanning tree's total weight: {minimum_cost}")

if __name__ == '__main__':
    g = Graph(4)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 6)
    g.add_edge(0, 3, 5)
    g.add_edge(1, 3, 15)
    g.add_edge(2, 3, 4)

    g.kruskalMST()