data_path = "D:\\boat-project-lora-network\\device\\boat\\src\\storage\\1671449137.805654.json"

import json
with open(data_path, "r", encoding = "utf-8") as fin:
  data = json.load(fin)

import base64
file_name = "test_img.png"
imgdata = base64.b64decode(data["image"])
with open(file_name, "wb") as fin:
  fin.write(imgdata)