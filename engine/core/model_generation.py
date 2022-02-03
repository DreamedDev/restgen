def get_model_lines():
    # Read model template
    with open('engine/templates/flask/model.template', 'r') as flask_model_template:
        flask_model_lines = flask_model_template.readlines()
        return flask_model_lines


def add_primitive_arg(field_name, field_type, flask_model_lines, model_file_str):
    # Create primitive arg
    model_file_str += ''.join(flask_model_lines[7]).format(
        field_name=field_name,
        field_type=field_type
    )
    return model_file_str


def make_relationship_str(rel_field_name, rel_cls, field_type, cmp_relationship, cls_name, back_populates_str, use_list_str):
    # Add id arg into cls/related cls depend on relationship.
    if field_type.relation_type == cmp_relationship:
        relationship_str = f'    {cls_name}_id = db.Column(db.Integer, db.ForeignKey(\'{cls_name}.id\'))\n'
    else:
        relationship_str = ''
    # Make relationship string with/without back_populates and use_list (use_list=False for one_to_one relationship).
    relationship_str += f'    {rel_field_name} = db.relationship(\'{rel_cls}\'{back_populates_str}{use_list_str})\n'
    return relationship_str


def get_relationship_str(field_name, field_type):
    # Add id arg into cls if many_to_one relationship (if not id arg in related cls).
    if field_type.relation_type == 'many_to_one':
        cls_name = field_type.class_name.lower()
        relationship_str = f'    {cls_name}_id = db.Column(db.Integer, db.ForeignKey(\'{cls_name}.id\'))\n'
    else:
        relationship_str = ''
    # Make relationship string with/without back_populates and use_list (use_list=False for one_to_one relationship).
    back_populates_str = f', back_populates=\'{field_type.back_populates}\'' if field_type.back_populates != '' else ''
    use_list_str = ', use_list=False' if field_type.relation_type == 'one_to_one' else ''
    relationship_str += f'    {field_name} = db.relationship(\'{field_type.class_name}\'{back_populates_str}{use_list_str})\n'
    return relationship_str


def get_related_relationship_str(cls, field_name, field_type):
    # Add id arg into related cls if one_to_many relationship (if not id arg in main relationship cls).
    if field_type.relation_type == 'one_to_many':
        cls_name = cls.name.lower()
        related_str = f'    {cls_name}_id = db.Column(db.Integer, db.ForeignKey(\'{cls_name}.id\'))\n'
    else:
        related_str = ''
    # Make related relationship string with/without back_populates.
    related_back_populates_str = f', back_populates=\'{field_name}\'' if field_type.back_populates != '' else ''
    related_str += f'    {field_type.back_populates} = db.relationship(\'{cls.name}\'{related_back_populates_str})\n'
    return related_str


def add_not_many_to_many_arg(cls, field_name, field_type, flask_model_lines, model_file_str):
    # Create arg with relationship for cls and add it into model cls.
    model_file_str += get_relationship_str(field_name, field_type)
    # Create relationship for related cls.
    related_str = get_related_relationship_str(cls, field_name, field_type)
    # Find related cls END position.
    related_cls_pos = model_file_str.find(f'    # END: {field_type.class_name}')
    # Add related cls relationship into model file.
    model_file_str = model_file_str[:related_cls_pos] + related_str + model_file_str[related_cls_pos:]
    return model_file_str


def get_association_table_str(cls, field_name, field_type):
    # Read association table template
    with open('engine/templates/flask/association.template', 'r') as association_template:
        association_table_lines = association_template.readlines()
        # Define back_populates.
        left_back_populates_str = f', back_populates=\'{field_name}\'' if field_type.back_populates != '' else ''
        right_back_populates_str = f', back_populates=\'{field_type.back_populates}\'' if field_type.back_populates != '' else ''
        # Make association table
        association_table_str = ''.join(association_table_lines[:6]).format(
            cls_name=f'{cls.name}_{field_type.class_name}',
            left=cls.name.lower(),
            right=field_type.class_name.lower(),
            left_cls=cls.name,
            right_cls=field_type.class_name,
            left_back_populates=left_back_populates_str,
            right_back_populates=right_back_populates_str)
        # Add related cls back_populates if defined
        if field_type.back_populates != '':
            association_table_str += association_table_lines[6].format(
                left=cls.name.lower(),
                left_cls=cls.name,
                left_back_populates=left_back_populates_str
            )
        return association_table_str


def add_many_to_many_arg(cls, field_name, field_type, model_file_str):
    # Create association table
    association_table_str = get_association_table_str(cls, field_name, field_type)
    # Add association above all model classes
    model_begin = model_file_str.find(f'# Model classes:\n')
    model_file_str = model_file_str[:model_begin] + association_table_str + '\n\n' + model_file_str[model_begin:]
    # Create back_populates if defined
    back_populates_str = f', back_populates=\'{cls.name.lower()}\'' if field_type.back_populates != '' else ''
    related_back_populates_str = f', back_populates=\'{field_type.class_name.lower()}\'' if field_type.back_populates != '' else None
    # Create relationship for main cls
    model_file_str += f'    {field_name} = db.relationship(\'{cls.name}_{field_type.class_name}\'{back_populates_str})\n'
    # Add relationship into related cls if back_populates defined
    if field_type.back_populates != '':
        related_relationship_str = f'    {field_type.back_populates} = db.relationship(\'{cls.name}_{field_type.class_name}\'{related_back_populates_str})\n'
        related_cls_pos = model_file_str.find(f'    # END: {field_type.class_name}\n')
        model_file_str = model_file_str[:related_cls_pos] + related_relationship_str + model_file_str[related_cls_pos:]
    return model_file_str


def generate_model_file(project_name, config):
    # Read model template and join imports
    with open('engine/templates/flask/model.template', 'r') as flask_model_template:
        flask_model_lines = flask_model_template.readlines()
        model_file_str = ''.join(flask_model_lines[0:4])
        # Create model classes
        for cls in config.model.classes:
            model_file_str += ''.join(flask_model_lines[4:7]).format(cls_name=cls.name, cls_table_name=cls.name.lower())
            # Create args for each model class
            for field_name, field_type in cls.attributes.items():
                # Create primitive arg
                if type(field_type) == str and field_name != 'id':
                    model_file_str = add_primitive_arg(field_name, field_type, flask_model_lines, model_file_str)
                # Create cls arg (with relationship)
                elif field_name != 'id':
                    # Arg with one_to_many/many_to_one/one_to_one relationship generation (same generating algorithm)
                    if field_type.relation_type != 'many_to_many':
                        model_file_str = add_not_many_to_many_arg(cls, field_name, field_type, flask_model_lines, model_file_str)
                    # Arg with many_to_many relationship generation
                    elif field_type.relation_type == 'many_to_many':
                        model_file_str = add_many_to_many_arg(cls, field_name, field_type, model_file_str)
            # Finish class generation with END comment (used in relationship generation to find related class)
            model_file_str += f'    # END: {cls.name}\n\n\n'
        # Save model
        with open(f'{project_name}/model.py', 'w+') as flask_model:
            flask_model.write(model_file_str)
