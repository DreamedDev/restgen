import yaml
import shutil
import os
from core import generation, running
from core.yarn_config_decoder import decode_yarn_config


def create(project_name):
    os.mkdir(project_name)
    shutil.copy('templates/config.yml', f'{project_name}/config.yml')


def override(project_name, override_method, acceptance_skip=False):
    if not acceptance_skip:
        print('Do you want override project?[Y/N]: ', end='')
    acceptance = input().lower() if not acceptance_skip else 'y'
    if acceptance == 'y':
        shutil.move(project_name, '.tmp')
        override_method(project_name)
        shutil.rmtree('.tmp')
        print('New project initialized/regenerated')
    else:
        print('Project not overwritten')


def get_yml_config(project_name):
    if os.path.isdir(project_name):
        with open(f'{project_name}/config.yml', 'r') as config_file:
            try:
                return yaml.safe_load(config_file)
            except Exception:
                print('Invalid config.yml file.')
    else:
        print('Not initialized project')
        return None


def get_config(project_name):
    yml_config_dict = get_yml_config(project_name)
    return decode_yarn_config(yml_config_dict)


def core_generate(project_name):
    if os.path.isdir('.tmp'):
        os.mkdir(project_name)
        shutil.copy('.tmp/config.yml', f'{project_name}/.version.yml')
        shutil.copy('.tmp/config.yml', f'{project_name}/config.yml')
    generation.generate(project_name, get_config(project_name))


def core_run(project_name):
    running.run(get_config(project_name))
