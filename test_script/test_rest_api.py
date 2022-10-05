import requests

patient_attribute = "PatientName"
patient_dept = "Ortho"
counter=0

rest_api_base_url = "https://expose-synapse-data.azurewebsites.net"

url_get = "{}/{}".format(rest_api_base_url,"patientNames")

url_post = "{}/{}/{}".format(rest_api_base_url,"patientDetails",patient_attribute)
request_payload = {"department" : patient_dept}


response_get = requests.get(url_get)
response_post = requests.post(url_post,json=request_payload)

expected_get_resp = {"patient_names" : ["Beth","Steve","Liz","Mike","Kim","Bob","George","Shaun","Kelly","Kevin"]}
expected_post_resp = {"patient_PatientName_dept_Ortho":['Liz', 'Mike', 'Bob', 'Shaun']}

actual_get_resp = response_get.json()
actaul_post_resp = response_post.json()

if actual_get_resp == expected_get_resp:
	counter+=1
	print("GET request successful with Actual and Expected = {}".format(actual_get_resp))
else:
	print("GET request failed where Expected = {} and Actual = {}".format(expected_get_resp,actual_get_resp))

if actaul_post_resp == expected_post_resp:
	counter+=1
	print("POST request successful with Actual and Expected = {}".format(actaul_post_resp))
else:
	print("POST request failed where Expected = {} and Actual = {}".format(expected_post_resp,actaul_post_resp))

if counter >= 2:
	print("Both GET and POST requests passed successfully......")



