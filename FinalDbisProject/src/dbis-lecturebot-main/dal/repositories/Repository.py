from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel

from dal.settings.dbcontext import session


class Repository:
    def __init__(self):
        self.query = ''
        self.session = session
        self.consistency_level = ConsistencyLevel.ONE

    def begin(self):
        self.query += "BEGIN BATCH\n\n"

    def commit(self):
        self.query += "APPLY BATCH;"
        statement = SimpleStatement(self.query, consistency_level=self.consistency_level)
        session.execute(statement)
        self.query = ''
