# pip3 install neo4j-driver
# python3 neo4j_example1.py

from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
  "neo4j+s://295c2445.databases.neo4j.io",
  auth=basic_auth("neo4j", "7_WtKz9W6QzpbVxHEC_hRFnV96j2QBcspYkWThPC5BM"))

#delete
cypher_delete = "MATCH (n) DETACH DELETE n"

with driver.session() as session:
  session.write_transaction(lambda tx: tx.run(cypher_delete).data())

#create
cypher_create = "CREATE (ee:Person {name: 'Emil', from: 'Sweden', kloutScore: 99})"

with driver.session() as session:
  session.write_transaction(lambda tx: tx.run(cypher_create).data())

#update
cypher_update = "MATCH (n {name: 'Emil'}) SET n.kloutScore = 100"
with driver.session() as session:
  session.write_transaction(lambda tx: tx.run(cypher_update).data())

#read
cypher_query = "MATCH (ee:Person) WHERE ee.name = 'Emil' RETURN ee as person"

with driver.session() as session:
  results = session.read_transaction(lambda tx: tx.run(cypher_query).data())
  print('Emil info:')
  for record in results:
    print(record['person'])


# create 4 more persons and 7 'KNOWS' relationships
more_create = '''MATCH (ee:Person) WHERE ee.name = 'Emil'
CREATE (js:Person { name: 'Johan', from: 'Sweden', learn: 'surfing' }),
(ir:Person { name: 'Ian', from: 'England', title: 'author' }),
(rvb:Person { name: 'Rik', from: 'Belgium', pet: 'Orval' }),
(ally:Person { name: 'Allison', from: 'California', hobby: 'surfing' }),
(ee)-[:KNOWS {since: 2001}]->(js),
(ee)-[:KNOWS {rating: 5}]->(ir),
(js)-[:KNOWS]->(ir),
(js)-[:KNOWS]->(rvb),
(ir)-[:KNOWS]->(js),
(ir)-[:KNOWS]->(ally),
(rvb)-[:KNOWS]->(ally)'''

with driver.session() as session:
  session.write_transaction(lambda tx: tx.run(more_create).data())


# read friends of Emil
friend_query = "MATCH (ee:Person)-[:KNOWS]-(friends) WHERE ee.name = 'Emil' RETURN friends"

with driver.session() as session:
  results = session.read_transaction(lambda tx: tx.run(friend_query).data())
  print('Emil friends:')
  for record in results:
    print(record['friends'])


driver.close()

