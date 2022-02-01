import urllib.parse


def get_db_uri(db_type, name, user, password, host, port, create_type) -> str:
    name = urllib.parse.quote_plus(name)
    user = urllib.parse.quote_plus(user)
    password = urllib.parse.quote_plus(password)
    host = urllib.parse.quote_plus(host)

    host_default = 'localhost'
    dbs = {
        'mssql': {
            'user': user if user != '' else 'SA',
            'password': password,
            'host': host if host != '' else host_default,
            'port': port if port != '' else 1433,
            'name': name
        },
        'mysql': {
            'user': user if user != '' else 'root',
            'password': password,
            'host': host if host != '' else host_default,
            'port': port if port != '' else 3306,
            'name': name
        },
        'postgres': {
            'user': user if user != '' else 'postgres',
            'password': password,
            'host': host if host != '' else host_default,
            'port': port if port != '' else 5432,
            'name': name
        }
    }
    if db_type != 'sqlite':
        user = dbs[db_type]['user']
        password = dbs[db_type]['password']
        host = dbs[db_type]['host']
        port = dbs[db_type]['port']
        name = dbs[db_type]['name']

    db_loc = f'{user}:{password}@{host}:{port}/{name}'
    db_uris = {
        'mssql': f'mssql+pymssql://{db_loc}',
        'mysql': f'mysql+pymysql://{db_loc}',
        'postgres': f'postgresql://{db_loc}',
        'sqlite': f'sqlite:///./{name}.db'
    }
    return db_uris[db_type]
