from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from array import array
import os
from PIL import Image
import sys
import time
import streamlit as st

def ocr_service_azure(file_img):
    subscription_key = 'fd491eddafea4ae9ad79cde8da773efe'
    endpoint = 'https://ocrservicedemo.cognitiveservices.azure.com/'

    # Assigning Client
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # Read file
    #read_image_url = "https://carwow-uk-wp-2.imgix.net/LEAF-source-1-scaled-e1612178298223.jpg"

    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(file_img, raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                # Check if the line contains a license plate number
                if any(char.isdigit() for char in line.text) and any(char.isalpha() for char in line.text):
                    return line
if __name__=="__main__":
    # Custom CSS to center the title
    st.markdown("""
        <style>
        .centered-title {
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    #st.title('Vehicle Number Extraction')
    st.markdown('<h1 class="centered-title">Vehicle Number Extraction</h1>', unsafe_allow_html=True)
    upload_file = st.file_uploader('Upload a file: ', type=['JPEG', 'PNG', 'BMP', 'PDF', 'TIFF'])
    #output_text = st.text_area("Output", value="")
    st.session_state.ocr = "Processing"
    if st.button("DO OCR"):
        line = ocr_service_azure(upload_file)
        print(line.text)
        print(line.bounding_box)
        output_text = st.text_area("Output", value=line.text)
        print(output_text)
