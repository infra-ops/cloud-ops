from cassandra.cluster import Cluster
from cqlengine.management import sync_table
cluster = Cluster()
session = cluster.connect('rjil')


result = session.execute("select * from serverhall2")[0]

print dir(result)


























#https://academy.datastax.com/resources/getting-started-apache-cassandra-and-python-part-i?unit=1984

'''
session.execute("""

insert into users (lastname, age, city, email, firstname) values ('Jones', 35, 'Austin', 'bob@example.com', 'Bob')

""")

'''
