import shutil
from core.db import get_db_uri
from core.model_generation import generate_model_file
from core.api_generation import generate_api


def generate_config_file(project_name, config):
    with open('templates/flask/config.template', 'r') as flask_config_template:
        with open(f'{project_name}/config.py', 'w+') as flask_config:
            flask_config.write(
                flask_config_template.read().format(
                    db_uri=get_db_uri(**config.db.__dict__)
                )
            )


def generate_model_generator_file(project_name, config):
    if not config.db.create_type == 'db_create_on':
        shutil.copy('templates/flask/model_generator.py', project_name)
    else:
        shutil.copy('templates/flask/model_create_generator.py', f'{project_name}/model_generator.py')


def generate(project_name, config):
    create_db_file_str = ''
    security_file_str = ''
    requirements_file_str = ''
    run_script_file_str = ''

    # config.py generation:
    generate_config_file(project_name, config)
    # main.py generation:
    shutil.copy('templates/flask/main.py', project_name)
    # model.py generation:
    generate_model_file(project_name, config)
    # model_generation.py generation:
    generate_model_generator_file(project_name, config)
    # api.py generation:
    generate_api(project_name, config)
