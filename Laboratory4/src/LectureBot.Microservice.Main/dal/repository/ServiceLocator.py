class ServiceLocator(object):
    def __init__(self, session, model_base, db_engine):
        self.DBEngine = db_engine
        self.Session = session
        self.ModelBase = model_base
        self.ModelBase.metadata.create_all(self.DBEngine)

    def get_count_of_resources_of_user(self):
        return self.DBEngine.execute('''
        SELECT "UserLogin", COUNT("ResourceURL") 
        FROM "UserHasResources" 
        GROUP BY "UserLogin" 
        ORDER BY COUNT("ResourceURL") DESC;
        ''')
