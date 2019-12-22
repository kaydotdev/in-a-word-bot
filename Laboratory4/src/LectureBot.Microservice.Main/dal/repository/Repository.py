from sqlalchemy.orm.attributes import InstrumentedAttribute


class Repository(object):
    def __init__(self, session, model_base, db_engine, entity_model):
        self.DBEngine = db_engine
        self.Session = session
        self.ModelBase = model_base
        self.ModelBase.metadata.create_all(self.DBEngine)
        self.entity_model = entity_model

    def map_entity(self, entity):
        mapped_values = {}

        for item in self.entity_model.__dict__.items():
            field_name = item[0]
            field_type = item[1]
            is_column = isinstance(field_type, InstrumentedAttribute)
            if is_column:
                mapped_values[field_name] = getattr(entity, field_name)

        return mapped_values

    def get_all(self):
        return self.Session.query(self.entity_model).all()

    def create(self, entity):
        self.Session.add(entity)
