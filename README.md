# InducedSubgraphsViewer
With this tool, you can build an undirected graph G, select a bunch S of subgraph and show all the induced subgraphs of G that are isomorphic to at least one graph in S.

## Installation
Mandatory: python3

```python
# Set up virtualenv if you want to
python3 -m venv env

# Install all necessary packages
pip3 install -r requirements.txt

# Set up default database (only on first install or to reset the database)
./initiate_db.sh

# Start InducedSubgraphsViewer
./start.sh
```

## Informations
First draw the graph G on the right of the webpage. To do so use the available buttons by clicking on "Edit". You can add, remove and move nodes and edges.
Then, on the left part of the webpage, you can see a list. Select any graph in that list to show it on the lower-left part of the page. Select every graph you look for in G by clicking on the Select checkbox, under the list.

Finally, on the bottom-center part of the page, click on COMPUTE to run the search algorithm. Every subgraph of G isomorphic to at least one selected graph of the list is colored red. Click the NEXT and PREVIOUS buttons to show the subgraphs one by one.

For instance, if you want to search for all the claws in the graph G, choose the claw on the list on the left, click on the Select Checkbox, and click COMPUTE. Use NEXT to show all the claws in G one by one.

You can manage the list of subgraphs with the menu on the upper-left corner of the page.
To add a graph to the list, build the graph on the right, choose a name (click on the name to edit it) and click on the leftmost button.
You can replace the current graph of the list (that is shown on the lower left corner) by clicking on the second button.
Conversely, you can replace the current edited graph by the current graph of the list with the third button.
Finally, you can remove the edited graph and the current graph of the list with the fourth and fifth buttons.

## Data
All changes being made to the database are save in db.json.
Feel free to backup this file if you need to.
Be aware that the script `initiate_db.sh` will replace your current database changes.
