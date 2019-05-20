import networkx as nx
import xml.etree.ElementTree as ET

LUT_SET = set()
FF_SET = set()


def all_devices_io(xml_node, iodict, current_clb, current_kernel, current_ble, current_lut_or_ff):
    if "mode" in xml_node.attrib:
        if xml_node.attrib["mode"] == "clb":
            iodict[xml_node.attrib["mode"]]["input"] = (xml_node[0][0].text).split()
            for child in xml_node:
                all_devices_io()


def add_nodes_recursive(graph, xml_node, placement_dict, current_clb):
    """
    Checks whether xml_node has 'mode' attribute as 'ble'. If yes, it creates a node in G
    for this element, with name of the node as 'name' attribute of the xml node's child and type attribute
    as the 'mode' attribute of the xml child.
    :param current_clb: the clb for the current element
    :param placement_dict: dict which has the placement of the elements on the FPGA
    :param graph: DiGraph to which we will add ble elements of the circuit as nodes and connections as edges
    :param xml_node: the current node in the xml tree
    """
    if "mode" in xml_node.attrib and xml_node.attrib["mode"] == "ble":
        for child in xml_node:
            name_exists = "name" in child.attrib and current_clb in place_dict
            if name_exists:
                not_open = child.attrib["name"] != "open"
                is_ff = (child.attrib['instance'])[:2] == "ff"
                is_lut = (child.attrib['instance'])[:3] == "lut"
                if not_open and (is_ff or is_lut):
                    node_name = child.attrib["name"]
                    graph.add_node(node_name)
                    # print(child.attrib)
                    if is_ff:
                        global FF_SET
                        graph.nodes[node_name]['type'] = "ff"
                        FF_SET.add(node_name)
                    else:
                        global LUT_SET
                        graph.nodes[node_name]['type'] = "lut"
                        LUT_SET.add(node_name)
                    graph.nodes[node_name]['x'] = int(place_dict[current_clb][0])
                    graph.nodes[node_name]['y'] = int(place_dict[current_clb][1])
                    graph.nodes[node_name]['subblk'] = int(place_dict[current_clb][2])
                    graph.nodes[node_name]['block number'] = int(place_dict[current_clb][3][1:])
    else:
        if 'mode' in xml_node.attrib and xml_node.attrib['mode'] == "clb":
            current_clb = xml_node.attrib['name']
        for child_node in xml_node:
            add_nodes_recursive(graph, child_node, placement_dict, current_clb)


G = nx.DiGraph()
net_tree = ET.parse('blob_merge_prepacked.net')
net_root = net_tree.getroot()
# for child in net_root:
#     print(child.tag, child.attrib)
place = open(r'blob_merge_prepacked.place', 'r')
place_dict = dict()
start_dict = False
while True:
    new_line = place.readline()
    if len(new_line) == 0:
        break
    # print(new_line)
    if new_line[:2] == "#-":  # this string is the beginning of the line which separates unwanted content from wanted
        # content
        start_dict = True
        break
while start_dict:
    new_line = place.readline()
    if len(new_line) == 0:
        break
    new_line = new_line.split()
    place_dict[new_line[0]] = tuple(new_line[1:])
add_nodes_recursive(G, net_root, place_dict, 0)
print("")
print("Graph G size is "+str(len(G.nodes)))
for node in G.nodes:
    print(str(node)+" "+str(G.nodes[node]))

# Adding edges:

for edge in G.edges:
    edge['weight'] = 8.5
    print(str(edge) + " " + str(G.edges[edge]))

