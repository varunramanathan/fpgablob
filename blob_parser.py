import networkx as nx
import xml.etree.ElementTree as ET

def add_nodes_recursive(graph, xml_node):
    """
    Checks whether xml_node has 'mode' attribute as 'ble'. If yes, it creates a node in G
    for this element, with name of the node as 'name' attribute of the xml node's child and type attribute
    as the 'mode' attribute of the xml child.
    :param graph: DiGraph to which we will add ble elements of the circuit as nodes and connections as edges
    :param xml_node: the current node in the xml tree
    """
    if "mode" in xml_node.attrib and xml_node.attrib["mode"] == "ble":
        for child in xml_node:
            name_exists = "name" in child.attrib
            if name_exists:
                not_open = child.attrib["name"] != "open"
                is_ff = (child.attrib['instance'])[:2] == "ff"
                is_lut = (child.attrib['instance'])[:3] == "lut"
                if not_open and (is_ff or is_lut):
                    node_name = child.attrib["name"]
                    graph.add_node(node_name)
                    # print(child.attrib)
                    if is_ff:
                        graph.nodes[node_name]['type'] = "ff"
                    else:
                        graph.nodes[node_name]['type'] = "lut"
    else:
        for child_node in xml_node:
            add_nodes_recursive(graph, child_node)


G = nx.DiGraph()
net_tree = ET.parse('blob_merge_prepacked.net')
net_root = net_tree.getroot()
# for child in net_root:
#     print(child.tag, child.attrib)
add_nodes_recursive(G, net_root)
for node in G.nodes:
    print(str(node)+" "+G.nodes[node]['type'])
