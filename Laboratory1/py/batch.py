from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
import hmac
import hashlib

# Configs
cassandra_port = '127.0.0.1'
key_space_name = 'lecturebot'
secret_key = "8581b093484655e699dd47ea78bb0d67e4e2aa9928e29a2653f232663f620dc5"  # Password Salt


###


# User defined functions
def get_password_hash(salt, password):
    return hmac.new(bytes(salt, 'UTF-8'), msg=bytes(password, 'UTF-8'), digestmod=hashlib.sha256).hexdigest().upper()


###


# Defined queries
register_new_users_resource_batch_query = SimpleStatement(
    """   
    BEGIN BATCH

    INSERT INTO user_lectures(login, password_hash, password_salt, role, resources)
    VALUES (%s, %s);

    INSERT INTO resource_components (url, description, times_visited)
    VALUES (%s, %s, %s);

    APPLY BATCH;
    """,
    consistency_level=ConsistencyLevel.ONE)

cluster = Cluster([cassandra_port])
session = cluster.connect(key_space_name)

session.execute(
    register_new_users_resource_batch_query,
    ("admin",
     {'https://docs.apigee.com/private-cloud/v4.17.09/about-cassandra-replication-factor-and-consistency-level'},
     'https://docs.apigee.com/private-cloud/v4.17.09/about-cassandra-replication-factor-and-consistency-level',
     'About Cassandra Replication Factor and Consistency Level',
     1)
)