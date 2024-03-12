import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import random
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

class GraphVisualizer:
    def __init__(self):
        self.G = nx.Graph()
        self.fig, self.ax = plt.subplots()
        self.pos = None
        self.visited_nodes = []
        self.edge_highlight = []
        self.dfs_order = []
        self.bfs_order = []
        self.canvas = None

    def generate_random_graph(self, num_nodes, probability):
        self.G = nx.erdos_renyi_graph(num_nodes, probability)

    def visualize_graph(self):
        self.pos = nx.spring_layout(self.G)
        nx.draw(self.G, self.pos, with_labels=True, font_weight='bold')

    def update_graph(self):
        plt.clf()
        nx.draw(self.G, self.pos, with_labels=True, font_weight='bold')
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=self.visited_nodes, node_color='g', node_size=500)
        if self.edge_highlight:
            nx.draw_networkx_edges(self.G, self.pos, edgelist=self.edge_highlight, edge_color='r', width=2)

    def animate_dfs(self, i):
        if i < len(self.dfs_order):
            self.visited_nodes.append(self.dfs_order[i])
            self.update_graph()

    def animate_bfs(self, i):
        if i < len(self.bfs_order):
            node, edge = self.bfs_order[i]
            self.visited_nodes.append(node)
            self.edge_highlight.extend(edge)
            self.update_graph()

    def dfs(self, start):
        visited = set()

        def dfs_recursive(node):
            visited.add(node)
            self.dfs_order.append(node)
            for neighbor in self.G.neighbors(node):
                if neighbor not in visited:
                    dfs_recursive(neighbor)

        dfs_recursive(start)
        print("DFS Traversal Order:", self.dfs_order)

    def bfs(self, start):
        visited = set()
        queue = deque([start])

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                self.bfs_order.append((node, [(node, neighbor) for neighbor in self.G.neighbors(node)]))
                queue.extend(neighbor for neighbor in self.G.neighbors(node) if neighbor not in visited)

        print("BFS Traversal Order:", [node for node, _ in self.bfs_order])

# GUI for the visualizer
class GraphVisualizerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Visualizer")
        self.visualizer = GraphVisualizer()

        # Generate a random graph with 10 nodes and a probability of edge creation
        self.visualizer.generate_random_graph(10, 0.3)

        # Visualize the random graph
        self.visualizer.visualize_graph()

        # Create Tkinter canvas to embed matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.visualizer.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create buttons for DFS and BFS
        self.dfs_button = tk.Button(self.master, text="Step DFS", command=self.step_dfs)
        self.dfs_button.pack(side=tk.LEFT)
        self.bfs_button = tk.Button(self.master, text="Step BFS", command=self.step_bfs)
        self.bfs_button.pack(side=tk.LEFT)

        # Perform DFS starting from a random node
        start_node = random.choice(list(self.visualizer.G.nodes()))
        self.visualizer.dfs(start_node)

        # Perform BFS starting from a random node
        start_node = random.choice(list(self.visualizer.G.nodes()))
        self.visualizer.bfs(start_node)

        self.dfs_i = 0
        self.bfs_i = 0

    def step_dfs(self):
        self.visualizer.animate_dfs(self.dfs_i)
        self.dfs_i += 1
        self.canvas.draw()

    def step_bfs(self):
        self.visualizer.animate_bfs(self.bfs_i)
        self.bfs_i += 1
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizerGUI(root)
    root.mainloop()
