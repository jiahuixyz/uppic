import pathlib
import sys
import requests
import base64
import json
import uuid
import datetime
import os


def get_properties(path):
    with open(path, 'r', encoding='utf-8') as f:
        properties = {}
        for line in f:
            if line.find('=') > 0:
                strs = line.replace('\n', '').split('=')
                properties[strs[0]] = strs[1]
        return properties


# 上传文件
def upload_file(pic_path, user, repo, token):
    with open(pic_path, 'rb') as f:
        pic_data = base64.b64encode(f.read()).decode()

    ext = os.path.splitext(pic_path)[1]
    file_name = str(uuid.uuid1()) + ext
    path = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}/{file_name}"
    headers = {"Authorization": "token " + token}
    data = json.dumps({"message": "pic", "content": pic_data})

    print("upload pic...")
    response = requests.put(url=url, data=data, headers=headers)
    response.encoding = "utf-8"
    # print(response.status_code)
    # print(response.text)
    # result = json.loads(response.text)
    if response.status_code == 201:
        print("upload success!")
        print(f"https://{user}.github.io/{repo}/{path}/{file_name}")
        print(f"https://raw.githubusercontent.com/{user}/{repo}/master/{path}/{file_name}")
        print(f"https://cdn.jsdelivr.net/gh/{user}/{repo}/{path}/{file_name}")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("pic path is need!")
    elif len(sys.argv) > 2:
        print("arg is too much!")

    pic_path = sys.argv[1]
    if not os.path.exists(pic_path) or not os.path.isfile(pic_path):
        print("pic is not exist!")

    home_path = str(pathlib.Path.home())
    p = get_properties(f"{home_path}/.uppic/config")
    user = p["user"]
    repo = p["repo"]
    token = p["token"]

    upload_file(pic_path, user, repo, token)
