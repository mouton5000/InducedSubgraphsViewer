"""
Author : Dimitri Watel
Year : 2020

Model of the flask application, contains all the functions manipulating the database.

The database managed with TinyDB and stored in a file named **db.json**.
"""

from tinydb import TinyDB, Query, where
import networkx as nx
from networkx.algorithms import isomorphism as isoalg

# Build the database
db = TinyDB('db.json')


def add_iso(g_id):
    """
    Add the graph with id **g_id** in I by storing it in the database with the type 'iso'
    :param g_id: id of a graph
    :return: True
    """
    db.insert({'type': 'iso', 'g_id': g_id})
    return True


def remove_iso(g_id):
    """
    Remove the graph with id **g_id** in I by removing that id stored with the type 'iso' from the database
    :param g_id: id of a graph
    :return: True
    """
    q = Query()
    db.remove((q.type == 'iso') & (q.g_id == g_id))
    return True


def add_node(g_id, u_id, x, y):
    """
    Add a node with id **u_id** to the graph with id **g_id** at coordinates **x** and **y** by storing all those information in the
    database with the type 'node'. If such a node is already associated to the graph in the database, nothing is done.
    :param g_id: id of a graph
    :param u_id: id of a node
    :param x: x coordinate of the node
    :param y: y coordinate of the node
    :return: True if the node is added to the graph and False otherwise
    """
    q = Query()
    i = db.search((q.type == 'node') & (q.g_id == g_id) & (q.u_id == u_id))  # Prevent dupplicates
    if len(i) == 0:
        db.insert({'type': 'node', 'g_id': g_id, 'u_id': u_id, 'x': x, 'y': y})
        return True
    else:
        return False


def add_edge(g_id, u_id, v_id):
    """
    Add an edge linking the nodes with ids **u_id** and **v_id** to the graph with id **g_id** by storing all those information in
    the database with the type 'edge'. If such an edge is already associated to the graph in the database, if **u_id** equals **v_id**
    or if **u_id** or **v_id** do not belong to the graph in the database, nothing is done.
    :param g_id: id of a graph
    :param u_id: id of a node
    :param v_id: id of a node
    :return: True if the edge is added to the graph and False otherwise
    """
    if u_id == v_id:
        return False
    if v_id < u_id:
        u_id, v_id = v_id, u_id

    q = Query()
    i = db.search((q.type == 'node') & (q.g_id == g_id) & ((q.u_id == u_id) | (q.u_id == v_id)))
    if len(i) != 2:
        return False
    i = db.search((q.type == 'edge') & (q.g_id == g_id) & (q.u_id == u_id) & (q.v_id == v_id))  # Prevent dupplicates
    if len(i) == 0:
        db.insert({'type': 'edge', 'g_id': g_id, 'u_id': u_id, 'v_id': v_id})
        return True
    return False


def remove_node(g_id, u_id):
    """
    Remove the node with id **u_id** from the graph with id **g_id** by removing all those information stored in the
    database with the type 'node'. Remove also every edge incident to that node from the graph by removing every
    document from the database containing the type 'edge' and where the id of one of the two extremities is **u_id**
     If no such node exists in the graph in the database, nothing is done.
    :param g_id: id of a graph
    :param u_id: id of a node
    :return: True if the node is removed from the graph and False otherwise
    """
    q = Query()
    r = db.remove((q.type == 'node') & (q.g_id == g_id) & (q.u_id == u_id))
    if len(r) > 0:
        db.remove((q.type == 'edge') & (q.g_id == g_id) & ((q.u_id == u_id) | (q.v_id == u_id)))
        return True
    return False


def remove_edge(g_id, u_id, v_id):
    """
    Remove the edge linking the nodes with id **u_id** and **v_id** from the graph with id **g_id** by removing all those
    information stored in the database with the type 'edge'. If no such edge exists in the graph in the database, nothing is
    done.
    :param g_id: id of a graph
    :param u_id: id of a node
    :param v_id: id of a node
    :return: True if the edge is removed from the graph and False otherwise
    """
    if u_id == v_id:
        return False
    if v_id < u_id:
        u_id, v_id = v_id, u_id
    q = Query()
    r = db.remove((q.type == 'edge') & (q.g_id == g_id) & (q.u_id == u_id) & (q.v_id == v_id))
    return len(r) > 0


def move_node(g_id, u_id, x, y):
    """
    Update the coordinates of the node with id **u_id** in the graph with id **g_id** to **x** and **y** by updating
    the 'x' and 'y' fields of the document containing those ids with the type 'node'. If no such node is associated
    to the graph in the database, nothing is done.
    :param g_id: id of a graph
    :param u_id: id of a node
    :param x: x coordinate of the node
    :param y: y coordinate of the node
    :return: True if the node is moved and False otherwise
    """
    q = Query()
    r = db.update({'x': x, 'y': y}, (q.type == 'node') & (q.g_id == g_id) & (q.u_id == u_id))
    return len(r) > 0


def save_main_name(name):
    """
    Update the name of the graph with id 0 in the database to **name** by updating the field 'name' of the document containing that
    id with the type 'properties'
    :param name: new name of the graph with id 0
    :return: True if the name is not None and False otherwise
    """
    if name is None:
        return False
    q = Query()
    db.upsert({'type': 'properties', 'g_id': 0, 'name': name}, (q.type == 'properties') & (q.g_id == 0))
    return True


def remove_graph(g_id):
    """
    Remove every occurrence of the graph with id **g_id** from the database
    :param g_id: id of a graph
    :return: True
    """
    db.remove(where('g_id') == g_id)
    return True


def erase_graph(g1_id, g2_id, name=None):
    """
    Erase the graph with id **g2_id** with a copy of the graph with id **g1_id**. To do so, every document where
    the field 'g_id' equals **g2_id** is removed and every document where the type is not 'iso' and where
    the field 'g_id' equals **g1_id** is copied, modified so that the field is replaced by **g2_id** and reinserted
    in the database. If the parameter **name** is not None, the name of the copied graph is set to **name** by the
    field 'name' of the document
    containing that id with the type 'properties'.

    g1_id should not equal g2_id otherwise nothing is done.
    :param g1_id: id of a graph
    :param g2_id: id of a graph
    :param name: new name of the copied graph
    :return: False is g1_id equals g2_id and g2_id otherwise.
    """
    if g1_id == g2_id:
        return False
    if g2_id is None:
        g2_id = max(x['g_id'] for x in db.search(where('type') == 'node')) + 1
    remove_graph(g2_id)
    q = Query()
    for x in db.search((q.g_id == g1_id) & (q.type != 'iso')):
        y = dict(x)
        y['g_id'] = g2_id
        db.insert(y)
    if name is not None:
        db.upsert({'type': 'properties', 'g_id': g2_id, 'name': name}, (q.type == 'properties') & (q.g_id == g2_id))
    return g2_id


def _get_graph(g_id):
    """
    A networkx graph object corresponding to the graph with id **g_id**. If no such graph exists an empty graph is
    returned
    :param g_id: id of a graph
    :return: a networkx graph object corresponding to the graph with id **g_id**
    """
    q = Query()
    nodes = (res['u_id'] for res in db.search((q.g_id == g_id) & (q.type == 'node')))
    edges = ((res['u_id'], res['v_id']) for res in db.search((q.g_id == g_id) & (q.type == 'edge')))

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g


def get_graph_dict(g_id):
    """
    Return a dict containing all the information of the graph with id **g_id** stored in the database. The dict has the
    following format :
    {
    'nodes' : list of ids of the nodes of the graph,
    'edges' : list of edges of the graph, each edge is described by the ids of the two extremities of the edge
    'name': the name of the graph stored in the document with type 'properties',
    'iso': True if the graph id is stored with the type 'iso' and False otherwise
    }

    :param g_id: id of a graph
    :return: A dict containing all the information of the graph with id **g_id** stored in the database
    """
    q = Query()
    nodes = [(res['u_id'], res['x'], res['y']) for res in db.search((q.g_id == g_id) & (q.type == 'node'))]
    edges = [(res['u_id'], res['v_id']) for res in db.search((q.g_id == g_id) & (q.type == 'edge'))]
    try:
        name = db.search((q.type == 'properties') & (q.g_id == g_id))[0]['name']
    except IndexError:
        name = ''
    iso = len(db.search((q.type == 'iso') & (q.g_id == g_id))) != 0
    return {'nodes': nodes, 'edges': edges, 'name': name, 'iso': iso}


def get_graph_infos():
    """
    Return a list of dicts containing some information of all the graphs stored in the database. Each dict has the
    following format :
    {
        'graph_id': the id of the graph,
        'name': the name of the graph,
        'iso': True if the graph id is stored with the type 'iso' and False otherwise
    }
    :return: A list of dicts containing some information of all the graphs stored in the database.
    """
    q = Query()
    isos = [res['g_id'] for res in db.search(q.type == 'iso')]
    names = [{'graph_id': res['g_id'], 'name': res['name'], 'iso': res['g_id'] in isos}
             for res in db.search((q.type == 'properties'))]
    names.sort(key=lambda x: x['name'])
    return names


def get_induced_subgraphs():
    """
    Return a list of dicts describing all the subgraphs of the graph with id 0 that are isomorphic to at least one graph for
    which the id is stored in the database with the type 'iso'.
    The list has the following format:
    [
    For each subgraph
        {
            'subgraph_id': the id of the graph stored with the type 'iso' isommorphic to the subgraph
            'nodes': the list of nodes of the subgraph
            'edges': the list of edges of the subgraph, each edge is described by the ids of the two extremities of
            the edge
        }
    ]
    :return: a list of dicts describing all the subgraphs of the graph with id 0 that are isomorphic to at least one graph for
    which the id is stored in the database with the type 'iso'.
    """
    q = Query()
    g = _get_graph(0)
    isos = [res['g_id'] for res in db.search(q.type == 'iso')]
    subgraphs = ((id, _get_graph(id)) for id in isos)

    inds = set()
    induced_subgraphs = []

    for id, subgraph in subgraphs:
        gm = isoalg.GraphMatcher(g, subgraph)
        for gm in gm.subgraph_isomorphisms_iter():
            k = frozenset(gm.keys())
            if k not in inds:
                inds.add(k)
                induced_subgraphs.append({'subgraph_id': id, 'nodes': list(k), 'edges': list(nx.Graph.subgraph(g, k).edges())})

    return induced_subgraphs

