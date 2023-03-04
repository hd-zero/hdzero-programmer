import base64

# 读取图像文件并编码为Base64字符串
with open("icon32.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# 将Base64编码字符串写入Python文件中
with open("icon32.py", "w") as python_file:
    python_file.write("icon32 = '{}'\n".format(encoded_string))
