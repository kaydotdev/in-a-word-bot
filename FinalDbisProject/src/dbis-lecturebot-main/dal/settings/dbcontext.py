from cassandra.cluster import Cluster

from dal.settings.dbconnection import HOST, KEY_SPACE, PORT


cluster = Cluster([HOST], port=PORT)
session = cluster.connect(KEY_SPACE)
