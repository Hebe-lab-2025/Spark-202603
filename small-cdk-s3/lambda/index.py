import json

def lambda_handler(event, context):
    print("=== Lambda START ===")
    print("Lambda was triggered successfully.")
    print("Received event:")
    print(json.dumps(event, indent=2))

    records = event.get("Records", [])
    if records:
        first_record = records[0]
        bucket_name = first_record.get("s3", {}).get("bucket", {}).get("name", "unknown-bucket")
        object_key = first_record.get("s3", {}).get("object", {}).get("key", "unknown-key")

        print(f"Bucket name: {bucket_name}")
        print(f"Object key: {object_key}")

    print("=== Lambda END ===")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Lambda executed successfully"
        })
    }