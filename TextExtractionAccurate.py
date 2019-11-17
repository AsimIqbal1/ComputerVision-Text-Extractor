from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import pathlib
from PIL import Image
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
import time


endpoint = 'cognitive service end point'
key = '[your key here from microsoft cognitive services]'

# Set credentials
credentials = CognitiveServicesCredentials(key)

# Create client
client = ComputerVisionClient(endpoint, credentials)

print("Done!")

path = "[path to extarct from]"
# path = "F:/Downloads-F/karan-johar-train.jpg"

#-----------------TEXT FROM IMAGE-------------#
print("#-----------------TEXT FROM IMAGE-------------#")
# import models
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
import time
image = open(path, 'rb')

raw = True
custom_headers = None
numberOfCharsInOperationId = 36

# Async SDK call
rawHttpResponse = client.batch_read_file_in_stream(image, custom_headers,  raw)

# Get ID from returned headers
operationLocation = rawHttpResponse.headers["Operation-Location"]
idLocation = len(operationLocation) - numberOfCharsInOperationId
operationId = operationLocation[idLocation:]

# SDK call
while True:
    result = client.get_read_operation_result(operationId)
    if result.status not in ['NotStarted', 'Running']:
        break
    time.sleep(1)

# Get data
if result.status == TextOperationStatusCodes.succeeded:
    for textResult in result.recognition_results:
        for line in textResult.lines:
            print(line.text)
            print(line.bounding_box)