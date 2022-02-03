def args_to_string(cls, http_method):
    args = ''
    for field_name, field_type in cls.attributes.items():
        if type(field_type) == str and field_name != 'id':
            if http_method == 'GET':
                args += f'\'{field_name}\': {cls.name.lower()}.{field_name}, '
            elif http_method == 'POST' or http_method == 'PUT':
                args += f'{field_name}={cls.name.lower()}[\'{field_name}\'], '
    return args


def basic_api_update(project_name, api_template, cls, args):
    with open(f'engine/templates/api/{api_template}', 'r') as basic_api_template:
        endpoint_str = basic_api_template.read().format(
            cls_name=cls.name.lower(),
            cls=cls.name,
            args=args
        )
        with open(f'{project_name}/api.py', 'a') as api:
            api.write(endpoint_str)


def relationship_args_to_string(cls, http_method, field):
    args = ''
    for field_name, field_type in cls.attributes.items():
        if type(field_type) == str and field_name != 'id':
            if http_method == 'GET':
                args += f'\'{field_name}\': {cls.name.lower()}.{field_name}, '
            elif http_method == 'POST' or http_method == 'PUT':
                args += f'{field_name}={cls.name.lower()}[\'{field_name}\'], '
    return args


def relationship_api_update(project_name, api_template, cls, field_name, related_args, related_cls):
    with open(f'engine/templates/api/{api_template}', 'r') as basic_api_template:
        endpoint_str = basic_api_template.read().format(
            cls_name=cls.name.lower(),
            cls=cls.name,
            field_name=field_name,
            related_cls_name=related_cls.name.lower(),
            related_args=related_args
        )
        with open(f'{project_name}/api.py', 'a') as api:
            api.write(endpoint_str)


# Eg. children <-> parents (many_to_many)
# Eg. /children | /parents (Group of children/parents operations)
def create_cls_endpoints(project_name, cls):
    # GET
    args = args_to_string(cls, 'GET')
    basic_api_update(project_name, 'get/get_cls.template', cls, args)
    pass


# Eg. /children/id | /parents/id (Specific child/parent operations)
def create_cls_obj_endpoints(project_name, cls):
    # GET
    args = args_to_string(cls, 'GET')
    basic_api_update(project_name, 'get/get_cls_obj.template', cls, args)
    # POST
    args = args_to_string(cls, 'POST')
    basic_api_update(project_name, 'post/post_cls_obj.template', cls, args)
    # PUT
    args = args_to_string(cls, 'PUT')
    basic_api_update(project_name, 'put/put_cls_obj.template', cls, args)
    # DELETE
    args = args_to_string(cls, 'DELETE')
    basic_api_update(project_name, 'delete/delete_cls_obj.template', cls, args)
    pass


# Eg. /parents/id/children (Specific parent's children operations)
def create_relation_cls_endpoints(project_name, cls, field_name, field_value, related_cls):
    # GET
    if field_value.relation_type == 'one_to_many' or field_value.relation_type == 'many_to_many':
        related_args = relationship_args_to_string(related_cls, 'GET', related_cls.name)
    else:
        related_args = relationship_args_to_string(related_cls, 'GET', field_name)
    relationship_api_update(project_name, 'get/get_relation_cls_head.template', cls, field_name, related_args, related_cls)
    if field_value.relation_type == 'one_to_many' or field_value.relation_type == 'many_to_many':
        relationship_api_update(project_name, 'get/get_relation_cls_many.template', cls, field_name, related_args, related_cls)
    else:
        relationship_api_update(project_name, 'get/get_relation_cls_one.template', cls, field_name, related_args, related_cls)


def get_cls_by_name(cls_name, config):
    for cls in config.model.classes:
        if cls.name == cls_name:
            return cls
    return None


def generate_api(project_name, config):
    with open(f'{project_name}/api.py', 'w+') as api:
        with open('engine/templates/api/api_imports.template', 'r') as api_imports_template:
            api.write(api_imports_template.read())
    for cls in config.model.classes:
        create_cls_endpoints(project_name, cls)
        create_cls_obj_endpoints(project_name, cls)
        for key, value in cls.attributes.items():
            if type(value) != str:
                cls_name = value.class_name
                related_cls = get_cls_by_name(cls_name, config)
                create_relation_cls_endpoints(project_name, cls, key, value, related_cls)
