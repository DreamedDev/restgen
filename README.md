# Zero coding REST API

### About:

>Zero coding REST API is based on config file (what is explained below) tool for instant backend code generation. It allows you to generate API based on REST architecture.

As an input, the tool execepts YAML file, while as output it returns fully working, based on the [Flask](https://flask.palletsprojects.com/en/2.0.x/) framework, API.

The configuration file specifies:

* database structure
* application model definition

And it provides:
* flask server
* db config
* ORM application model based on SQLAlchemy framework
* many popular in usage endpoints based on REST API standard

Config file is maximally shortened with many default values and intuitive in usage. Rules are presented below:

```yaml
# Auto generated restgen config.yml file. Complete /.../ sections
# Available KEY_TYPE values below.
# If you want to use default value for any section leave it empty.
# For example for /class_type_arg/ key you can define value /class_name/:::/CASCADE_TYPE/ for default /RELATION_TYPE/ and /BACKREF_TYPE/:
# Ending colons can be skipped. For example: for db key you can shorten value /DB_TYPE/:/database/::::: to /DB_TYPE/:/database/
# For section __privileges__ default 'default' value for each generated endpoint is public. You can delete this all section if nothing to change.

# Available KEY_TYPE values (case-insensitive except PRIMITIVE_TYPE):
# CONFIG_TYPE: YAML | YAML_SHORT
# DB_TYPE: SQLITE | MYSQL | POSTGRES | MSSQL
# DB_CREATE_TYPE: DB_CREATE_ON | DB_CREATE_OFF
# PRIMITIVE_TYPE: BigInteger | Boolean | Date | DateTime | Enum | Float | Integer | Interval | LargeBinary | MatchType | Numeric | PickleType | SchemaType | SmallInteger | String | Text | Unicode | UnicodeText
# RELATION_TYPE: ONE_TO_MANY | MANY_TO_ONE | ONE_TO_ONE | MANY_TO_MANY
# CASCADE_TYPE: CASCADE | CASCADE_DELETE | CASCADE_UPDATE | CASCADE_OFF

# Default values:
# db: /DB_TYPE required/:/database required/:default user:password required if not sqlite:localhost:default port:CREATE_OFF
# /class_type_arg/: /class_name required/:RELATION_TYPE required:BACKREF_OFF:CASCADE_OFF

config: /CONIF_TYPE/
db: /DB_TYPE/:/database/:/user/:/password/:/host/:/port/:/DB_CREATE_TYPE/
model:
  /ClassName/:
    /primiteive_arg/: /PRIMITIVE_TYPE/
    /class_type_arg/: /class_name/:/RELATION_TYPE/:BACK_POPULATES/:/CASCADE_TYPE/
  /.../

```

### Example:
```yaml
db: sqlite:car_showroom
model:
  Car:
    brand: String
    model: String
    price: Integer
    color: String
  CarShowroom:
    name: String
    address: String
    cars: Car:one_to_many
```

# Home REST server generation tutorial

### I. Generate your REST app.

**Step 0:** Check how to use restgen.
```bash
./restgen -h
```

**Step 1:** Init new project with config.yaml template.
```bash
./restgen init Home
```

**Step 2:** Define your REST app in config.yaml file inside generated project.\
```
example/Home.yaml -> config.yaml
```

**Step 3:** Generate your REST app.
```bash
./restgen generate Home
```
Congratulation!!! You just created REST app. App works independently of the generating tool, so you can move it whenever you want (docker, server, etc.).

### II. Run generated REST server.

If you want to run your app you can generate your database schema and run server.

**Step 0:** Go to your app directory.
```bash
cd Home
```

**Step 1:** Generate your database schema using model_generator.py
```bash
python3 model_generator.py
```

**Step 2:** Run your REST server.
```bash
python3 main.py
```

### III. Verify, play and modify your REST app.

Verify your REST server performance. Generated endpoinds you can find in Home/api.py file.

**Step 1:**
```
GET http://localhost:5000/child
```
Response body:
```json
{
    "child_arr": []
}
```

**Step 2:**
```
POST http://localhost:5000/child
```
Request body:
```json
{
    "name": "Tomek",
    "age": 12
}
```
Response body:
```json
{
    "message": "child posted successfully."
}
```

**Step 3:**
```
POST http://localhost:5000/child
```
Request body:
```json
{
    "name": "Janek",
    "age": 16
}
```
Response body:
```json
{
    "message": "child posted successfully."
}
```

**Step 4:**
```
GET http://localhost:5000/child
```
Response body:
```json
{
    "child_arr": [
        {
            "age": 12,
            "id": 1,
            "name": "child1"
        },
        {
            "age": 16,
            "id": 2,
            "name": "Janek"
        }
    ]
}
```

**Step 5:**
```
GET http://localhost:5000/child/1
```
Response body:
```json
{
    "child": {
        "age": 12,
        "name": "child1"
    }
}
```

**Step 6:**
```
DELETE http://localhost:5000/child/1
```
Response body:
```json
{
    "message": "The child has been deleted."
}
```

**Step 7:**
```
GET http://localhost:5000/child
```
Response body:
```json
{
    "child_arr": [
        {
            "age": 16,
            "id": 2,
            "name": "Janek"
        }
    ]
}
```

Play and modify your REST api:

Check README.md to get to know more about restgen and structure of generated REST server project. Feel freely with project modification. It's fully human-readable.

**Step 0:** Go to CarShowroom/api.py

**Step 1:** Add hello_world endpoint
```python
@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello World'}), 200
```
**Step 2:** Check your server after modification.

### IV. Regenerate REST app

**Step 1:** Modify config.yaml file. Eg. change db name.
```yaml
db: sqlite:home
...
```

**Step 2:** Regenerate your project.
```bash
python3 ./restgen generate Home
```

**Step 3:** Accept it.
```
Do you want override project?[Y/N]: y
```
Project regenerated. Changes from this example are visible in Home/config.py


### Attention:
Zero coding REST API doesn't solve any problems bound with advanced REST API development with comlex logic but it's usefull for typical CRUD application and also gives very fast start even for bigger project generating base application code. So it can give great results for smaller prjects and super fast start for greater projects.