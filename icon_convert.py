import base64

with open("icon32.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

with open("icon32.py", "w") as python_file:
    python_file.write("icon32 = '{}'\n".format(encoded_string))
