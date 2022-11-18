from flask import Flask,redirect,url_for,render_template,request
import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT="https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints"
COS_API_KEY_ID="VgpAIWmBsADKDiceL4TtHisrZJRakzyAcHY8KJh7e8eu"
COS_INSTANCE_CRN="crn:v1:bluemix:public:cloud-object-storage:global:a/4d0964bde14f425bbbd5fdececfb7325:690d9f1c-9462-402b-b1f7-9a1c368dc601::"



# Create resource https://s3.ap.cloud-object-storage.appdomain.cloud
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

app=Flask(__name__)


def get_item(bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        file = cos.Object(bucket_name, item_name).get()

        print("File Contents: {0}".format(file["Body"].read()))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))


def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

  
@app.route('/')
def index():
    files = get_bucket_contents('ibmbucket-2')
    return render_template('index.html', files = files)


if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)