import networkx as nx
import xml.etree.ElementTree as ET

G = nx.DiGraph()
net_tree = ET.parse('blob_merge_prepacked.net')
place_tree = ET.parse('blob_merge_prepackaged.place')
net_root = net_tree.getroot()
place_root = place_tree.getroot()

