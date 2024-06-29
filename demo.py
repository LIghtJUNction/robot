from flask import Flask, request
import requests # type: ignore
import json

app = Flask(__name__)


def send_message_to_api(url, data):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Message sent successfully.")
    elif response.status_code == 422:
        print("Validation Error. Details:")
        print(response.json())
    else:
        print("Error:", response.status_code)


@app.route('/text', methods=['POST'])
def callback():
    data = request.get_json()

    if "sender" not in data:
        return "Error: 'sender' key not found in data", 400

    if "content" not in data:
        return "Error: 'content' key not found in data", 400

    user = data.get("sender")
    xinxi = data.get("content")

    print("Sender:", user)
    print("Content:", xinxi)

    # 发送生成回复请求
    url_generate = "http://localhost:11434/api/generate"
    data_generate = {
        "model": "gemma:2b",   #这里可以自己切换模型，切换之前先到终端运行一下模型，以便下载文件
        "prompt": xinxi        #模型下载地址  https://ollama.com/library
    }

    response_generate = requests.post(url_generate, json=data_generate)

    if response_generate.status_code == 200:
        try:
            response_text = response_generate.text
            response_list = response_text.split("\n")
            full_response = ""
            for item in response_list:
                if item.strip():
                    response_data = json.loads(item)
                    full_response += response_data["response"].replace(" ", "") + " "
            print("Full Response:", full_response)

            # 发送消息到指定接口
            url_send_message = "http://localhost:9999/text"


            # 发送生成的回复消息到指定接口
            data_send_response = {
                "msg": full_response,
                "receiver": user,
                "aters": ""
            }

            send_message_to_api(url_send_message, data_send_response)

        except json.decoder.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))
    else:
        print("Error:", response_generate.status_code)

    return "Message received"


if __name__ == '__main__':
    app.run(host='localhost', port=9998)