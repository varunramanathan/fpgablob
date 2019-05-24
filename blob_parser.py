import networkx as nx
import xml.etree.ElementTree as ET

LUT_SET = set()
FF_SET = set()


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


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
            name_exists = "name" in child.attrib and current_clb in placement_dict
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
                    graph.nodes[node_name]['x'] = int(placement_dict[current_clb][0])
                    graph.nodes[node_name]['y'] = int(placement_dict[current_clb][1])
                    graph.nodes[node_name]['subblk'] = int(placement_dict[current_clb][2])
                    graph.nodes[node_name]['block number'] = int(placement_dict[current_clb][3][1:])
    else:
        if 'mode' in xml_node.attrib and xml_node.attrib['mode'] == "clb":
            current_clb = xml_node.attrib['name']
        for child_node in xml_node:
            add_nodes_recursive(graph, child_node, placement_dict, current_clb)


def distance_in_graph(graph, u, v):
    x1 = graph.nodes[u]['x']
    y1 = graph.nodes[u]['y']
    x2 = graph.nodes[v]['x']
    y2 = graph.nodes[v]['y']
    return abs(x1 - x2) + abs(y1 - y2) + 8


def return_out_end(xml_node, edge_from):
    if xml_node.attrib["instance"][:4] == "lut[" or xml_node.attrib["instance"][:3] == "ff[":
        return xml_node.attrib["name"]
    else:
        for sub_xml_block in range(len(xml_node)):  # get into component
            if "instance" in xml_node[sub_xml_block].attrib and xml_node[sub_xml_block].attrib["instance"] == edge_from[
                0]:  # are we in, say, kernel[3]?
                edge_from_in_component = xml_node[sub_xml_block][1][0].text.split()[
                    int(edge_from[1][edge_from[1].find("[") + 1:edge_from[1].find("]")])].split("->")[0].split(".")
                return return_out_end(xml_node[sub_xml_block], edge_from_in_component)


def edge_construction(xml_node, in_edge_list, graph):
    # print(str(xml_node))
    if "mode" in xml_node.attrib:
        # print("mode exists")
        current_mode = xml_node.attrib["mode"]
        if current_mode == "lut" or current_mode == "ff":
            node_element_in_graph = graph.nodes[xml_node.attrib["name"]]
            current_coordinates = (node_element_in_graph["x"], node_element_in_graph["y"])
            # print("At lut or ff "+str(xml_node.attrib["name"]))
            if current_coordinates not in in_edge_list: in_edge_list[current_coordinates] = dict()
            if xml_node.attrib["name"] not in in_edge_list[current_coordinates]: in_edge_list[current_coordinates][
                xml_node.attrib["name"]] = list()
            for element in xml_node[0][0].text.split(" "):
                if element != "open":
                    in_edge_list[current_coordinates][xml_node.attrib["name"]].append(element.split("->")[0])
            # print(str(xml_node.attrib["name"]) +" " + str(in_edge_list[current_coordinates][xml_node.attrib["name"]]) + " is the lut/ff we are exiting")
            # print("Out of lut or ff")

        elif current_mode == "ble":
            if xml_node.attrib["name"] == "open":
                return in_edge_list
            node_element_in_graph = graph.nodes[xml_node.attrib["name"]]
            current_coordinates = (node_element_in_graph["x"], node_element_in_graph["y"])
            # print("At ble " + str(xml_node.attrib["name"]))
            for child in xml_node:
                edge_construction(child, in_edge_list, graph)
            for u in in_edge_list[current_coordinates]:
                in_edges_u = in_edge_list[current_coordinates][u]
                # print(str(u) + " : " + str(in_edges_u))
                for v in range(len(in_edges_u)):
                    if in_edges_u[v] == "open":
                        continue
                    if in_edges_u[v].find(".") != -1:
                        edge_from = in_edges_u[v].split(".")
                        if edge_from[0] == "ble":
                            in_edge_list[current_coordinates][u][v] = xml_node[0][0].text.split()[
                                int(edge_from[1][edge_from[1].find("[") + 1:edge_from[1].find("]")])].split("->")[0]
                        elif edge_from[0][:6] != "kernel" and edge_from[0][:3] != "clb" and edge_from[0][:4] != "ble[":
                            in_edge_list[current_coordinates][u][v] = return_out_end(xml_node, edge_from)
            # print("Out of ble")

        elif current_mode == "kernel":
            if xml_node.attrib["name"] in graph.nodes:
                node_element_in_graph = graph.nodes[xml_node.attrib["name"]]
                current_coordinates = (node_element_in_graph["x"], node_element_in_graph["y"])
                # print("At kernel " + str(xml_node.attrib["name"]))
                for child in xml_node:
                    edge_construction(child, in_edge_list, graph)
                for u in in_edge_list[current_coordinates]:
                    in_edges_u = in_edge_list[current_coordinates][u]
                    # print(str(u) + " : " + str(in_edges_u))
                    for v in range(len(in_edges_u)):
                        if in_edges_u[v] == "open":
                            continue
                        if in_edges_u[v].find(".") != -1:
                            edge_from = in_edges_u[v].split(".")
                            if edge_from[0] == "kernel":
                                in_edge_list[current_coordinates][u][v] = xml_node[0][0].text.split()[
                                    int(edge_from[1][edge_from[1].find("[") + 1:edge_from[1].find("]")])].split("->")[0]
                            elif edge_from[0][:3] != "clb" and edge_from[0][:7] != "kernel[":
                                in_edge_list[current_coordinates][u][v] = return_out_end(xml_node, edge_from)
                # print("Out of kernel")

        elif current_mode == "clb":
            node_element_in_graph = graph.nodes[xml_node.attrib["name"]]
            current_coordinates = (node_element_in_graph["x"], node_element_in_graph["y"])
            # print("At clb" + str(xml_node.attrib["name"]))
            for child in xml_node:
                edge_construction(child, in_edge_list, graph)  # updated dict
            for u in in_edge_list[current_coordinates]:
                in_edges_u = in_edge_list[current_coordinates][u]
                # print(str(u)+" : "+str(in_edges_u))
                for v in range(len(in_edges_u)):
                    if in_edges_u[v] == "open":
                        continue
                    if in_edges_u[v].find(".") == -1:
                        continue
                    edge_from = in_edges_u[v].split(".")
                    if edge_from[0] == "clb":
                        assert edge_from[1][:2] == "I["
                        in_edge_list[current_coordinates][u][v] = xml_node[0][0].text.split()[
                            int(edge_from[1][edge_from[1].find("[") + 1:edge_from[1].find("]")])]
                    elif edge_from[0][:7] == "kernel[":
                        in_edge_list[current_coordinates][u][v] = return_out_end(xml_node, edge_from)
            # print("Done with clb")
            # print("Printing IN_EDGE_LIST: ")
        return in_edge_list
    else:
        # print("mode doesn't exist, bro do you even deep")
        for child in xml_node:
            in_edge_list = edge_construction(child, in_edge_list, graph)
        # print("In edge list: " + str(in_edge_list))
        return in_edge_list


def update_edges_to_from_u(graph, u, new_x, new_y):
    graph.nodes[u]['x'] = new_x
    graph.nodes[u]['y'] = new_y
    for vertex in graph[u]:
        graph.add_edge(u, vertex, weight=distance_in_graph(graph, u, vertex))
    for vertex in nx.DiGraph.predecessors(graph, u):
        graph.add_edge(vertex, u, weight=distance_in_graph(graph, vertex, u))


def blob_parser(net_file,place_file):
    length1 = 27  # 0 to 26
    length2 = 27
    G = nx.DiGraph()
    net_tree = ET.parse(net_file)
    net_root = net_tree.getroot()
    # for child in net_root:
    #     print(child.tag, child.attrib)
    place = open(place_file, 'r')
    place_dict = dict()
    start_dict = False
    while True:
        new_line = place.readline()
        if len(new_line) == 0:
            break
        # print(new_line)
        if new_line[:5] == "Array":
            new_line = new_line.split()
            length1 = int(new_line[2])
            length2 = int(new_line[4])
        if new_line[
           :2] == "#-":  # this string is the beginning of the line which separates unwanted content from wanted
            # content
            start_dict = True
            break
    while start_dict:
        new_line = place.readline()
        if len(new_line) == 0:
            break
        new_line = new_line.split()
        place_dict[new_line[0]] = tuple(new_line[1:])
    place.close()
    add_nodes_recursive(G, net_root, place_dict, 0)
    print("")
    print("Graph G size is " + str(len(G.nodes)))
    # for node in G.nodes:
    #     print(str(node)+" "+str(G.nodes[node]))

    # Adding edges:
    print("\nStarting edge construction")
    in_edge_list = edge_construction(net_root, dict(), G)
    print("IN_EDGE_LIST " + str(in_edge_list))
    print("\n###############\n")
    for coord in in_edge_list:
        # print("coord is "+str(coord))
        for v in in_edge_list[coord]:
            for u in in_edge_list[coord][v]:
                # print(str(u)+" "+str(v))
                # forbidden = {'open', 'top^iReset'}
                if u in G.nodes and v in G.nodes:
                    G.add_edge(u, v, weight=distance_in_graph(G, u, v))

    # Remove flip-flops with in-edges as well as out-edges
    for edge in G.edges:
        if G.nodes[edge[1]]['type'] == "ff" and len(G[edge[1]]) > 0:
            G.remove_node(edge[1])

    # print("Graph G size is "+str(len(G.nodes)))

    longest_path = nx.dag_longest_path(G)
    print("Longest path in original graph is " + str(longest_path))
    for v in longest_path:
        print(str(G.nodes[v]['x']) + " " + str(G.nodes[v]['y']))
    length_longest = nx.dag_longest_path_length(G)
    print("longest path has length " + str(length_longest) + " with " + str(len(longest_path)) + " nodes.")
    for i in range(len(longest_path) - 3):
        v1 = longest_path[i]
        v2 = longest_path[i + 1]
        v3 = longest_path[i + 2]
        print("I am starting to move: " + str(v1) + " " + str(v2) + " " + str(v3))
        # condition to check whether we want to do the new graph or not
        # if yes:
        d = distance_in_graph(G, v1, v2) + distance_in_graph(G, v2, v3)
        print("v1 v2 are at distance " + str(distance_in_graph(G, v1, v2)))
        print("v3 v2 are at distance " + str(distance_in_graph(G, v2, v3)))

        left = max(min(G.nodes[v1]['x'] - d, G.nodes[v3]['x'] - d), 0)
        right = min(max(G.nodes[v1]['x'] + d, G.nodes[v3]['x'] + d), length1)
        bottom = max(min(G.nodes[v1]['y'] - d, G.nodes[v3]['y'] - d), 0)
        top = min(max(G.nodes[v1]['y'] + d, G.nodes[v3]['y'] + d), length2)
        old_coordinates = (G.nodes[v2]['x'], G.nodes[v2]['y'])
        print(str((top - bottom) * (right - left)) + " is the total number of points we check")
        for x in range(left, right):
            for y in range(bottom, top):
                #             try x,y as new coordinates if new sum of distances is smaller
                new_v1v2 = abs(G.nodes[v1]['x'] - x) + abs(G.nodes[v1]['y'] - y) + 8
                new_v2v3 = abs(G.nodes[v3]['x'] - x) + abs(G.nodes[v3]['y'] - y) + 8
                if new_v1v2 + new_v2v3 >= d:
                    continue
                changing_vertices = [node for node in in_edge_list[old_coordinates] if node != v2]
                G.nodes[v2]['x'] = x
                G.nodes[v2]['y'] = y
                G.add_edge(v1, v2, weight=distance_in_graph(G, v1, v2))
                G.add_edge(v2, v3, weight=distance_in_graph(G, v2, v3))
                # changing_vertices = [node for node in in_edge_list[old_coordinates]]
                # G.edges[]
                for u in changing_vertices:
                    update_edges_to_from_u(G, u, x, y)
                longest_path_new = nx.dag_longest_path(G)
                new_longest_length = nx.dag_longest_path_length(G)
                if length_longest > new_longest_length:
                    print("FOUND A BETTER CONNECTION")
                    print("Change all nodes from the cluster in " + str(old_coordinates) + " to " + str((x, y)))
                    new_d = distance_in_graph(G, v1, v2) + distance_in_graph(G, v2, v3)
                    print("For our triplet, the sum of taxicab distances changed from " + str(d) + " to " + str(
                        new_d) + " [which should be the same as " + str(new_v2v3 + new_v1v2) + "]. ")
                    print("new longest path has length " + str(new_longest_length) + " with " + str(
                        len(longest_path_new)) + " nodes.")
                    print("New longest path is : " + str(longest_path_new))
                    if longest_path_new != longest_path:
                        print("NEW LONGEST PATH IS DIFFERENT!")

                print("\n###############\n")
                for u in changing_vertices:
                    update_edges_to_from_u(G, u, old_coordinates[0], old_coordinates[1])
                G.nodes[v2]['x'] = old_coordinates[0]
                G.nodes[v2]['y'] = old_coordinates[1]
                G.add_edge(v1, v2, weight=distance_in_graph(G, v1, v2))
                G.add_edge(v2, v3, weight=distance_in_graph(G, v2, v3))

    print("no of edges: " + str(len(G.edges)))


if __name__ == '__main__':
    blob_parser('blob_merge_prepacked.net','blob_merge_prepacked.place')