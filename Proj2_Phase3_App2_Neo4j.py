# pip3 install neo4j-driver
# python3 neo4j_example2.py

from neo4j import GraphDatabase, basic_auth

#https://neo4j.com/product/graph-data-science/
driver = GraphDatabase.driver(
  "neo4j://44.200.201.165:7687",
  auth=basic_auth("neo4j", "millimeters-canal-acceleration"))

#delete
cypher_delete = "MATCH (n) DETACH DELETE n"

#with driver.session() as session:
#  session.write_transaction(lambda tx: tx.run(cypher_delete).data())


#create
cypher_create = '''
create (s:Loc {name:"s"}), 
(t:Loc {name:"t"}), (y:Loc {name:"y"}),
(x:Loc {name:"x"}), (z:Loc {name:"z"}),
(s)-[:ROAD {cost:10}]->(t), (s)-[:ROAD {cost:5}]->(y),
(t)-[:ROAD {cost:1}]->(x), (t)-[:ROAD {cost:2}]->(y),
(y)-[:ROAD {cost:3}]->(t), (y)-[:ROAD {cost:9}]->(x), (y)-[:ROAD {cost:2}]->(z),
(x)-[:ROAD {cost:4}]->(z),
(z)-[:ROAD {cost:7}]->(s), (z)-[:ROAD {cost:6}]->(x)
'''

data_science = '''
CALL gds.graph.create('myGraph', 'Loc', 'ROAD', {relationshipProperties:'cost'})
'''

with driver.session() as session:
  session.write_transaction(lambda tx: tx.run(cypher_create).data())
  session.write_transaction(lambda tx: tx.run(data_science).data())


#find shortest path from s to x
cypher_query = '''
MATCH (source:Loc{name:"s"}), (target:Loc{name:"x"})
CALL gds.shortestPath.dijkstra.stream('myGraph', {
    sourceNode: source,
    targetNode: target,
    relationshipWeightProperty: 'cost'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
RETURN totalCost, [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames
'''

with driver.session() as session:
  results = session.read_transaction(lambda tx: tx.run(cypher_query).data())
  print('Shortest path from s to x:')
  for record in results:
    print(record)


driver.close()

