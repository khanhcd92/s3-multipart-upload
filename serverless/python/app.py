import os
import boto3
from flask_cors import CORS
from flask import Flask, jsonify, request

app = Flask(__name__)
cors = CORS(app)

BUCKET_NAME = os.environ['BUCKET_NAME']
s3 = boto3.client('s3')


@app.route("/start-upload", methods=["GET"])
def start_upload():
    file_name = request.args.get('file_name')
    response = s3.create_multipart_upload(
        Bucket=BUCKET_NAME, 
        Key=file_name
    )

    return jsonify({
        'upload_id': response['UploadId']
    })

@app.route("/get-upload-url", methods=["GET"])
def get_upload_url():
    file_name = request.args.get('file_name')
    upload_id = request.args.get('upload_id')
    part_no = request.args.get('part_no')
    signed_url = s3.generate_presigned_url(
        ClientMethod ='upload_part',
        Params = {
            'Bucket': BUCKET_NAME,
            'Key': file_name, 
            'UploadId': upload_id, 
            'PartNumber': int(part_no)
        }
    )

    return jsonify({
        'upload_signed_url': signed_url
    })

@app.route("/complete-upload", methods=["POST"])
def complete_upload():
    file_name = request.json.get('file_name')
    upload_id = request.json.get('upload_id')
    print(request.json)
    parts = request.json.get('parts')
    response = s3.complete_multipart_upload(
        Bucket = BUCKET_NAME,
        Key = file_name,
        MultipartUpload = {'Parts': parts},
        UploadId= upload_id
    )
    
    return jsonify({
        'data': response
    })


if __name__ == "__main__":
    app.run()
