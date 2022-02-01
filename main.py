import argparse
import os
import filecmp
from core.management import create, override, get_config, core_generate, core_run


def init(project_name):
    if not os.path.isdir(project_name):
        create(project_name)
        print('Project initialized')
    else:
        override(project_name, create)


def generate(project_name):
    if not os.path.exists(project_name):
        print('Not initialized project')
    elif get_config(project_name) is None:
        pass
    else:
        if not os.path.exists(f'{project_name}/.version.yml'):
            override(project_name, core_generate, True)
        elif filecmp.cmp(f'{project_name}/config.yml', f'{project_name}/.version.yml'):
            print('Nothing to update. File config.yml not change since last running/generation')
        else:
            override(project_name, core_generate)


def run(project_name):
    generate(project_name)
    core_run(project_name)


def main():
    parser = argparse.ArgumentParser(description='Restgen: zero coding REST API')
    parser.add_argument('opt', choices=['init', 'generate', 'run'],
                        help='Init config.yml file, complete it and run or just generate REST API')
    parser.add_argument('name', help='Project name')
    args = parser.parse_args()
    eval(f'{args.opt}("{args.name}")')


if __name__ == '__main__':
    main()
