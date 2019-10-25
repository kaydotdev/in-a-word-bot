# Class for supporting transaction integrity
class UnitOfWork(object):
    def __init__(self, session, modelbase):
        self.Session = session
        self.ModelBase = modelbase

    def commit(self):
        self.Session.commit()
