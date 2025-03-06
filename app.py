import base64
import json
import io
import face_recognition
import numpy as np
import asyncio
import boto3
from concurrent.futures import ThreadPoolExecutor
from botocore.exceptions import BotoCoreError, ClientError

DYNAMODB_TABLE_NAME = "FaceEncodings"
dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def get_encoding_sync(image_b64):
    try:
        image_bytes = base64.b64decode(image_b64)
        image = face_recognition.load_image_file(io.BytesIO(image_bytes))
        encodings = face_recognition.face_encodings(image)
        return json.dumps(encodings[0].tolist()) if encodings else None
    except Exception as e:
        return {"error": f"Encoding error: {str(e)}"}


def compare_encodings_sync(known_str, new_str):
    try:
        known = np.array(json.loads(known_str))
        new = np.array(json.loads(new_str))
        return bool(face_recognition.compare_faces([known], new, tolerance=0.3)[0])
    except Exception as e:
        return {"error": f"Comparison error: {str(e)}"}


def average_encodings_sync(enc1_str, enc2_str):
    try:
        enc1 = np.array(json.loads(enc1_str))
        enc2 = np.array(json.loads(enc2_str))
        return json.dumps(((enc1 + enc2) / 2).tolist())
    except Exception as e:
        return {"error": f"Averaging error: {str(e)}"}


async def get_encoding(image_b64, executor):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, get_encoding_sync, image_b64)
    if isinstance(result, dict) and "error" in result:
        raise Exception(result["error"])
    return result


async def compare_encodings(known, new, executor):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, compare_encodings_sync, known, new)
    if isinstance(result, dict) and "error" in result:
        raise Exception(result["error"])
    return result


async def average_encodings(enc1, enc2, executor):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, average_encodings_sync, enc1, enc2)
    if isinstance(result, dict) and "error" in result:
        raise Exception(result["error"])
    return result


def dynamo_get_encoding(email):
    try:
        response = table.get_item(Key={"email": email})
        return response.get("Item", None)
    except (BotoCoreError, ClientError) as e:
        raise Exception(f"Error retrieving encoding: {str(e)}")


def dynamo_put_encoding(email, encoding_str):
    try:
        table.put_item(Item={"email": email, "encoding": encoding_str})
    except (BotoCoreError, ClientError) as e:
        raise Exception(f"Error saving encoding: {str(e)}")


def dynamo_update_encoding(email, encoding_str):
    try:
        table.update_item(
            Key={"email": email},
            UpdateExpression="SET encoding = :e",
            ExpressionAttributeValues={":e": encoding_str},
        )
    except (BotoCoreError, ClientError) as e:
        raise Exception(f"Error updating encoding: {str(e)}")


async def process_request(email, image_b64, registration, executor):
    try:
        new_encoding = await get_encoding(image_b64, executor)
        if not new_encoding:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No face detected."}),
            }

        if registration:
            dynamo_put_encoding(email, new_encoding)
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Registration successful."}),
            }

        item = dynamo_get_encoding(email)
        if not item or "encoding" not in item:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Email not registered."}),
            }

        stored_encoding = item["encoding"]
        if await compare_encodings(stored_encoding, new_encoding, executor):
            avg_encoding = await average_encodings(
                stored_encoding, new_encoding, executor
            )
            dynamo_update_encoding(email, avg_encoding)
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Face matched and updated."}),
            }

        return {"statusCode": 200, "body": json.dumps({"message": "Face not matched."})}

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Processing error: {str(e)}"}),
        }


async def async_lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        email = body.get("email")
        image_b64 = body.get("image")
        registration = body.get("registration", False)

        if not email or not image_b64:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields."}),
            }

        with ThreadPoolExecutor() as executor:
            return await process_request(email, image_b64, registration, executor)

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format."}),
        }
    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Missing key: {str(e)}"}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Unexpected error: {str(e)}"}),
        }


def lambda_handler(event, context):
    return asyncio.run(async_lambda_handler(event, context))
