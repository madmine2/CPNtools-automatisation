import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from collections import Counter

class PetriNet:
    def __init__(self):
        self.places = set()
        self.transitions = set()
        self.arcs = set()

    def add_place(self, name):
        self.places.add(name)

    def add_transition(self, name):
        self.transitions.add(name)

    def add_arc(self, source, target):
        self.arcs.add((source, target))

# Exemple d'utilisation avec les traces extraites du fichier mxml
file_path = "new_data_mxml.mxml"

def parse_mxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    traces = []
    for process_instance in root.findall(".//ProcessInstance"):
        trace = []
        for entry in process_instance.findall(".//AuditTrailEntry"):
            workflow_element = entry.find("WorkflowModelElement").text
            trace.append(workflow_element)
        traces.append(trace)

    return traces

traces = parse_mxml(file_path)

# Compter le nombre de fois où chaque WorkflowModelElement apparaît
element_counts = Counter(element for trace in traces for element in trace)

# Créer le réseau de Petri avec networkx
G = nx.DiGraph()

# Ajouter des nœuds (places et transitions) avec les occurrences dans le nom
for element, count in element_counts.items():
    node_name = f"{element} (x{count})"
    G.add_node(node_name)

# Ajouter des arcs (les transitions ne sont pas nécessaires ici)
for trace in traces:
    for i in range(len(trace) - 1):
        source = f"{trace[i]} (x{element_counts[trace[i]]})"
        target = f"{trace[i + 1]} (x{element_counts[trace[i + 1]]})"
        G.add_edge(source, target)

# Définir une disposition linéaire pour les nœuds
pos = nx.shell_layout(G)

# Visualiser le réseau avec matplotlib
nx.draw(G, pos, with_labels=True, font_size=8, font_color='black', font_weight='bold', arrowsize=10, edge_color='gray', width=0.5)

plt.show()