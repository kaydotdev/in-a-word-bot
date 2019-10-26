from sqlalchemy.orm.attributes import InstrumentedAttribute


class Repository(object):
    def __init__(self, session, model_base, db_engine):
        self.DBEngine = db_engine
        self.Session = session
        self.ModelBase = model_base
        self.ModelBase.metadata.create_all(self.DBEngine)

    def __map_entity(self, entity_model, entity):
        mapped_values = {}

        for item in entity_model.__dict__.items():
            field_name = item[0]
            field_type = item[1]
            is_column = isinstance(field_type, InstrumentedAttribute)
            if is_column:
                mapped_values[field_name] = getattr(entity, field_name)

        return mapped_values

    def get_all(self, entity_model):
        return self.Session.query(entity_model).all()

    def get_by_id(self, entity_model, identity):
        return self.Session.query(entity_model).filter_by(Id=identity).first()

    def get_by_raw_query(self, query):
        return self.Session.query(query)

    def create(self, entity):
        self.Session.add(entity)

    def update(self, entity_model, entity, identity, is_autoincrement):
        if is_autoincrement:
            self.Session.query(entity_model).filter_by(Id=identity).update(self.__map_entity(entity_model, entity))
        else:
            self.Session.query(entity_model).filter_by(URL=identity).update(self.__map_entity(entity_model, entity))

    def drop(self, entity_model, identity, is_autoincrement):
        if is_autoincrement:
            self.Session.query(entity_model).filter_by(Id=identity).delete()
        else:
            self.Session.query(entity_model).filter_by(URL=identity).delete()
