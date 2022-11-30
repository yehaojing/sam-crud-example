import boto3
import os
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
import uuid

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ['ddb_table_name'])
app = APIGatewayRestResolver()

def lambda_handler(event, context):
    return app.resolve(event, context)

@app.post("/user")
def post_user():
    body = app.current_event.json_body
    body["id"] = str(uuid.uuid1())
    table.put_item(
        Item=body
    )

    return {
        "statusCode": 202,
        "message": "New user created.",
        "user": body
    }

@app.get("/user/<id>")
def get_user(id):
    resp = table.get_item(
        Key={
            "id": id
        }
    )

    if "Item" in resp.keys():
        return { "statusCode": 200, "user": resp["Item"] }
    else:
        return { "statusCode": 404, "message": "User not found."}

@app.get("/user")
def get_user():
    resp = table.scan()

    if "Items" in resp.keys():
        return { "statusCode": 200, "users": resp["Items"] }
    else:
        return { "statusCode": 404, "message": "No users found."}

@app.put("/user/<id>")
def update_user(id):
    body = app.current_event.json_body
    body.update(
        {"id":id}
    )
    table.put_item(
        Item=body
    )

    return {
        "statusCode": 202,
        "message": "User updated.",
        "user": body
    }

@app.delete("/user/<id>")
def delete_user(id):
    resp = table.delete_item(
        Key={
            "id": id
        }
    )

    return {
        "statusCode": 202,
        "message": "User deleted."
    }