"""
Author : Dimitri Watel
Year : 2020

Controller of the flask application.

With this application, the user can define a set I of graphs, and highlight, in a graph G, the induced subgraphs
that are isomorphic to at least one graph of I.

The application has one webpage in which the user can build and edit a graph G and a list J of graphs.
The user can:
- build and edit the nodes and edges of G
- add G to J
- clear G
- erase G with a graph of J
- delete a graph of J
- build a sublist I of J
- highlight, in a graph G, the induced subgraphs that are isomorphic to at least one graph of I.
Each graph is associated with a name to recognize it in the application.

Every information is stored in a persistent database using TinyDB.

"""

from flask import Flask, request, render_template, jsonify
import model.graph_db as gdb


# Initialize flask application
app = Flask(__name__)


@app.route('/')
def main_page():
    """ Main route, return the (sole) webpage of the application"""
    return render_template('mainView.html')


@app.route('/graph')
@app.route('/graph/<int:graph_id>')
def get_graph(graph_id=0):
    """
    Build the graph with id **graph_id** according to the information stored in the database.
    If the id is 0, the graph G is returned, otherwise a graph of J is returned.
    A json file corresponding to the graph is built with the following format:
    {
    'nodes' : list of ids of the nodes of the graph,
    'edges' : list of edges of the graph, each edge is described by the ids of the two extremities of the edge
    'name': the name of the graph,
    'iso': the string 'true' or 'false' depending if the graph belongs to J or not
    }
    If no graph with the given id exists in the database, an empty graph is returned.
    :param graph_id: id of a graph.
    :return: a json file corresponding to the graph with id **graph_id**.
    """
    return jsonify(gdb.get_graph_dict(graph_id))


@app.route('/erase_main_graph/<int:graph_id>')
def erase_main_graph(graph_id):
    """
    Replace the graph G in the database by a copy of the graph with id **graph_id**.
    If **graph_id** is 0, nothing is done.
    A name can be given with a GET argument **name**. In that case, the name of G is replaced in the database, except
    if **graph_id** is 0.
    If no graph with the given id exists in the database, G is cleared.
    :param graph_id: id of a graph.
    :return: the string '0' if the graph is erased and 'false' otherwise
    """
    name = request.args.get('name', None)
    erased = gdb.erase_graph(graph_id, 0, name)
    return str(erased).lower()


@app.route('/save_main_graph')
@app.route('/save_main_graph/<int:graph_id>')
def save_main_graph(graph_id=None):
    """
    Add G to the list J by either replacing an existing graph or adding it to the end of the list.

    Replace the graph with id **graph_id** in the database by a copy of G. If **graph_id**
    is None, the copy of G is associated with a new id that does not belong to any graph of J.
    If **graph_id** is 0, nothing is done.
    A name can be given with a GET argument **name**. In that case, the name of the erased/added graph is replaced in
    the database, except if graph_id is 0.
    :param graph_id: id of a graph.
    :return: the id of the erased/added graph if the graph G is added to J and 'false' otherwise
    """
    name = request.args.get('name', None)
    g_id = gdb.erase_graph(0, graph_id, name)
    return str(g_id)


@app.route('/save_main_name')
def save_main_name():
    """
    A name can be given with a GET argument **name**. In that case, the name of G is replaced in the database.
    :return: the string 'true' if the name is replaced and 'false' otherwise
    """
    name = request.args.get('name', None)
    b = gdb.save_main_name(name)
    return str(b).lower()


@app.route('/delete_graph')
@app.route('/delete_graph/<int:graph_id>')
def delete_graph(graph_id=0):
    """
    Remove the graph with id **graph_id** in the database. If no such graph exists, nothing is done.
    :param graph_id: id of a graph
    :return: the string 'true'
    """
    b = gdb.remove_graph(graph_id)
    return str(b).lower()


@app.route('/add_node/<int:node_id>')
def add_node(node_id):
    """
    Add a node with id **node_id** to G. If the node already exists in G, nothing is done.
    Two coordinates x and y can be given with GET arguments **x** and **y**. In that case, the coordinates are
    stored in the databse with the node.

    :param node_id: id of a node
    :return: the string 'true' if the given node is added and 'false' otherwise
    """
    x = int(float(request.args.get('x', None)))
    y = int(float(request.args.get('y', None)))
    added = gdb.add_node(0, node_id, x, y)
    return str(added).lower()


@app.route('/move_node/<int:node_id>')
def move_node(node_id):
    """
    Change the coordinates of the node with id **node_id** in G, if the node already exists in G. Otherwise nothing is
    done. The two coordinates x and y can be given with GET arguments **x** and **y**.

    :param node_id: id of a node
    :return: the string 'true' if the given node is moved and 'false' otherwise
    """
    x = int(float(request.args.get('x', None)))
    y = int(float(request.args.get('y', None)))
    b = gdb.move_node(0, node_id, x, y)
    return str(b).lower()


@app.route('/remove_node/<int:node_id>')
def remove_node(node_id):
    """
    Remove the node with id **node_id** from G. If the node does not exists in G, nothing is done. Every edge incident
    to that node is also removed.
    :param node_id: id of a node
    :return: the string 'true' if the given node is removed and 'false' otherwise
    """
    b = gdb.remove_node(0, node_id)
    return str(b).lower()


@app.route('/add_edge/<int:node1_id>/<int:node2_id>')
def add_edge(node1_id, node2_id):
    """
    Add a new edge to G linking the nodes with id **node1_id** and **node2_id**. If one of the two nodes does not
    belong to G, if the two ids are equal or if the edges already exists in G, nothing is done.

    :param node1_id: id of a node
    :param node2_id: id of a node
    :return: the string 'true' if the new edge is added to G and 'false' otherwise
    """
    added = gdb.add_edge(0, node1_id, node2_id)
    return str(added).lower()


@app.route('/remove_edge/<int:node1_id>/<int:node2_id>')
def remove_edge(node1_id, node2_id):
    """
        Remove the edge linking the nodes with id **node1_id** and **node2_id** from G. If no such edge exists in G,
        nothing is done.

        :param node1_id: id of a node
        :param node2_id: id of a node
        :return: the string 'true' if the edge is remove from G and 'false' otherwise
        """
    b = gdb.remove_edge(0, node1_id, node2_id)
    return str(b).lower()


@app.route('/add_iso/<int:graph_id>')
def add_iso(graph_id):
    """
    Add the graph with id **graph_id** of J to I. If no such graph exists, an empty graph, with the given id is
    returned.
    :param graph_id: id of a graph
    :return: the string 'true'
    """
    b = gdb.add_iso(graph_id)
    return str(b).lower()


@app.route('/remove_iso/<int:graph_id>')
def remove_iso(graph_id):
    """
    Remove the graph with id **graph_id** of J from I. If no such graph exists, nothing is done.
    :param graph_id: id of a graph
    :return: the string 'true'
    """
    b = gdb.remove_iso(graph_id)
    return str(b).lower()


@app.route('/graphs_infos')
def graphs_infos():
    """
    Build and return a JSON file containing some information on all the graphs.
    The json file is built with the following format:
    [
    For each graph in the database :
        {
            'graph_id': the id of the graph,
            'name': the name of the graph,
            'iso': the string 'true' or 'false' depending if the graph belongs to J or not
        }
    ]
    :return: a JSON file containing some information on all the graphs.
    """
    return jsonify(gdb.get_graph_infos())


@app.route('/induced_subgraphs')
def get_induced_subgraphs():
    """
    Build and return a JSON file describing all the subgraphs of G that are isomorphic to at least one graph of I.
    The json file is built with the following format:
    [
        For each subgraph
        {
            'subgraph_id': the id of the graph in I isomorphic to the subgraph
            'nodes': the list of nodes belonging to at least one such subgraph
            'edges': the list of edges belonging to at least one such subgraph
        }
    ]
    :return: a JSON file describing all the subgraphs of G that are isomorphic to at least one graph of I.
    """
    return jsonify(gdb.get_induced_subgraphs())


if __name__ == '__main__':
    app.run()
