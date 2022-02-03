class DatabaseConfig:
    def __init__(self, db) -> None:
        db += ':' * (6 - db.count(':'))
        self.db_type, self.name, self.user, self.password, self.host, self.port, self.create_type = db.split(':')
        self.db_type = self.db_type.lower()
        self.create_type = self.create_type.lower()
        if self.db_type not in {'sqlite', 'mysql', 'postgres', 'mssql'}:
            print('Incorrect DB_TYPE')
            raise Exception


class PrivilegeConfig:
    def __init__(self, privileges: str):
        privileges += ':' * (4 - privileges.count(':'))
        privileges = [privilege.lower() for privilege in privileges.split(':')]
        self.default, self.get, self.post, self.put, self.delete = privileges
        self.default = self.default if self.default != '' else 'public'
        self.get = self.get if self.get != '' else self.default
        self.post = self.post if self.post != '' else self.default
        self.put = self.put if self.put != '' else self.default
        self.delete = self.delete if self.delete != '' else self.default


class RelationAttributeConfig:
    def __init__(self, params):
        params += ':' * (3 - params.count(':'))
        self.class_name = params.split(':')[0]
        params = [attr.lower() for attr in params.split(':')[1:]]
        self.relation_type, self.back_populates, self.cascade_type = params
        # self.back_populates = self.back_populates.lower() if self.back_populates != '' and self.back_populates.lower() != '' else ''
        self.cascade_type = self.cascade_type if self.cascade_type != '' else 'cascade_off'


class ClassConfig:
    @staticmethod
    def convert_attributes(attributes: dict) -> dict:
        def convert_value(value):
            return value if value.count(':') == 0 else RelationAttributeConfig(value)
        return {k: convert_value(v) for k, v in attributes.items()}

    def __init__(self, name: str, attributes: dict) -> None:
        self.name = name
        self.privileges = PrivilegeConfig(attributes.pop('__privileges__', ''))
        self.attributes = ClassConfig.convert_attributes(attributes)


class ModelConfig:
    def __init__(self, model: dict) -> None:
        self.classes = [ClassConfig(name, args) for name, args in model.items()]


class Config:
    def __init__(self, db: str, model: dict) -> None:
        self.db = DatabaseConfig(db)
        self.model = ModelConfig(model)


def decode_yarn_config(config_dict: dict) -> Config:
    try:
        return Config(config_dict['db'], config_dict['model'])
    except Exception:
        print('Something went wrong during config file decoding. Check your config.yml file.')
