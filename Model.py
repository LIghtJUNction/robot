import datetime
import os
import random
import requests
import json
"""
快速介绍 这是用于接入ollama 模型的一个
类: OllamaModel
方法如下:
1.产生单个回复  参数为prompt 其他默认即可 stream为false表示不及时返回大模型的生成,也就是官方文档的非流式,返回最终结果,true也支持返回最终结果

2.chat方法,和第一个类似,但是支持聊天历史记录,适合连续对话

3.列出现在运行的模型

4.列出本地所有模型

5.显示当前运行模型的信息

6.复制一份当前模型的副本(也可以传入你要复制的模型名)

7.删除当前(默认)运行的模型



"""

class OllamaModel:
    def __init__(self, host="127.0.0.1", port=11434):
        self.base_url = f"http://{host}:{port}/api"
        self.name = self.list_local_models()[0]       # 模型名字
        
    def generate_completion(self, prompt, stream=True,system="默认使用中文回答,且尽量精简",):  # 已测试,功能正常 6/27/2024
        url = f"{self.base_url}/generate"
        headers = {"Content-Type": "application/json"}
        payload = {"model": self.name, "prompt": prompt, "stream": stream,"system":system,"option":{"seed":random(1,100)}}

        try:
            if stream:
                full_response = ""  # 初始化一个空字符串用于累积响应部分
                with requests.post(url, json=payload, headers=headers, stream=True) as response:
                    response.raise_for_status()
                    for raw_response in response.iter_lines():
                        if raw_response:
                            try:
                                data = json.loads(raw_response.decode('utf-8'))
                                response_part = data.get('response', '')
                                full_response += response_part  # 累积响应部分
                                print(response_part, end='', flush=True)
                            except json.JSONDecodeError:
                                print(f"Failed to parse JSON object: {raw_response}")
                return full_response  # 返回完整的响应
            else:
                response = requests.post(url, json=payload, headers=headers,stream=False)
                response.raise_for_status()
                data = response.json()
                return data.get('response', '')

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return ""
    
    def chat(self,messages,stream=True):
        url = f"{self.base_url}/chat"
        headers = {"Content-Type": "application/json"}
        payload = {"model":self.name,"messages":messages}
        try:
            if stream:
                full_response = ""  # 初始化一个空字符串用于累积响应部分
                with requests.post(url, json=payload, headers=headers, messages=messages ,stream=True) as response:
                    response.raise_for_status()
                    for raw_response in response.iter_lines():
                        if raw_response:
                            try:
                                data = json.loads(raw_response.decode('utf-8'))
                                response_part = data.get('response', '')
                                full_response += response_part  # 累积响应部分
                                print(response_part, end='', flush=True)
                            except json.JSONDecodeError:
                                print(f"Failed to parse JSON object: {raw_response}")

                return full_response  # 返回完整的响应
            else:
                response = requests.post(url, json=payload, headers=headers,stream=False)
                response.raise_for_status()
                data = response.json()
                return data.get('response', '')
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return ""
        
    def list_running_model(self): # 已测试功能正常 6/27/2024
        url = f"{self.base_url}/ps"
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
                    # 提取name字段
            running_models = []
            for model in json_data["models"]:
                name = model["name"]
                running_models.append(name)
            return running_models
        except requests.RequestException as e:
            print(f"An error occurred while listing running models: {e}")
            return []
        
    def list_local_models(self): #  已测试正常 6/27/2024 返回一个列表
        url = f"{self.base_url}/tags"
        try:
            response = requests.get(url)
            response.raise_for_status()
            models = response.json()
            # 提取name字段
            model_names = []
            for model in models["models"]:
                model_names.append(model["name"])
            return model_names
        except requests.RequestException as e:
            print(f"An error occurred while listing the models: {e}")
            return []

    def show_model_info(self,name):  #已测试正常 6/27/2024
        if name == None:
            name = self.name
        
        url = f"{self.base_url}/show"
        payload = {"name": name}
        try:
            response = requests.post(url, json=payload)  # 使用 params 参数传递查询参数
            response.raise_for_status()
            model_info = response.json()
            return model_info
        except requests.RequestException as e:
            print(f"An error occurred while retrieving the model information: {e}")
            return {}
    
    def copy_model(self, name,NewName): # 不打算测试
        if name == None:
            name = self.name
        if NewName == None:
            return print("copy_model(self, name,NewName),你需要输入拷贝后的新文件名!")
        url = f"{self.base_url}/copy"
        headers = {"Content-Type": "application/json"}
        payload = {"source": name, "destination": name}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Model {self.name} copied successfully from {source_model}.")
        except requests.RequestException as e:
            print(f"An error occurred while copying the model: {e}")

    def delete_model(self,name): # 不打算测试
        if name == None:
            name = self.name
        
        url = f"{self.base_url}/delete"
        try:
            response = requests.delete(url)
            response.raise_for_status()
            print(f"Model {name} deleted successfully.")
        except requests.RequestException as e:
            print(f"An error occurred while deleting the model: {e}")
    
    def pull_model(self, name): # 不打算测试 在线下载一个模型用的
       
        url = f"{self.base_url}/pull"
        headers = {"Content-Type": "application/json"}
        payload = {"name": name}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Model {name} pulled successfully .")
        except requests.RequestException as e:
            print(f"An error occurred while pulling the model: {e}")

    def push_model(self, name): #不打算测试
        if name == None:
            name = self.name
        
        url = f"{self.base_url}/push"
        headers = {"Content-Type": "application/json"}
        payload = {"name": name}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Model {name} pushed successfully.")
        except requests.RequestException as e:
            print(f"An error occurred while pushing the model: {e}")
    
    def create_model(self, modelfile):  # 不打算测试
        
        # 示例 modelfile="FROM llama3\nSYSTEM You are mario from Super Mario Bros."
        url = f"{self.base_url}/creat"
        headers = {"Content-Type": "application/json"}
        payload = {"model": self.name, "modefile":modelfile}
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Model created successfully.")
        except requests.RequestException as e:
            print(f"An error occurred while creating the model: {e},建议使用本功能前检查一下Model.py文件ollamamodel类,本方法没有测试")

# 以下用于添加聊天历史记录(message) 供chat()方法使用

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.history.append(message)
        # 保持聊天记录不超过max_length条
        if len(self.history) > self.max_length:
            self.history.pop(0)

    def get_history(self):
        return json.dumps(self.history, indent=4) 

class EmbeddingGenerator:    # 保存embedding文件 并建立索引文件 和数据调用器
    def __init__(self, base_url, model_name, index_file="index.json"):
        self.base_url = base_url
        self.name = model_name
        self.index_file = index_file
        # 创建索引文件，如果不存在的话
        if not os.path.exists(self.index_file):
            with open(self.index_file, 'w') as f:
                json.dump([], f)

    def generate_embeddings(self, prompt):  #  产生文件
        url = f"{self.base_url}/embeddings"
        headers = {"Content-Type": "application/json"}
        payload = {"model": self.name, "prompt": prompt}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            embeddings_response = response.json()

            # 生成文件名
            safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{self.name}_{safe_prompt}_{timestamp}.json"

            # 将嵌入向量保存到文件中
            with open(file_name, "w") as file:
                json.dump(embeddings_response, file, indent=4)

            # 更新索引文件
            with open(self.index_file, 'r+') as f:
                index = json.load(f)
                index_entry = {
                    "file_name": file_name,
                    "timestamp": timestamp,
                    "model_name": self.name,
                    "prompt": prompt
                }

                index.append(index_entry)
                f.seek(0)
                json.dump(index, f, indent=4)

            # 打印成功消息
            print(f"Embeddings have been saved to {file_name}")
            
            return embeddings_response
        except requests.RequestException as error:
            print(f"An error occurred while generating embeddings: {error}")
            return {}

    def get_embedding_file(self, query_prompt): # 查找embedding文件
        with open(self.index_file, 'r') as f:
            index = json.load(f)
            for entry in index:
                if query_prompt in entry['prompt']:
                    return entry['file_name']
        return None



    """"
    model：生成嵌入的模型名称
    prompt：要生成嵌入的文本
    用于从指定模型生成文本的嵌入（embedding）。文本嵌入是将文本转化为数值向量的过程，这些向量可以在机器学习和自然语言处理任务中用于表示和操作文本数据。
    """
    
    


    """我决定把这个单独拿出来做文章
    def generate_embeddings(self, prompt):
        url = f"{self.base_url}/embeddings"
        headers = {"Content-Type": "application/json"}
        payload = {"model": self.name, "prompt": prompt}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            embeddings = response.json()

            # 将嵌入向量保存到文件中
            with open("embeddings.json", "w") as f:
                json.dump(embeddings, f, indent=4)

            # 仅打印成功消息
            print("Embeddings have been saved to embeddings.json")

            return embeddings
        except requests.RequestException as e:
            print(f"An error occurred while generating embeddings: {e}")
            return {}

        """

"""
API接口如下
This class provides APIs for interacting with a model. It includes methods for creating, copying, pulling, pushing, and deleting models, as well as generating embeddings and listing running models.
    API Interface:
        * Generate a completion
        * Generate a chat completion
        * Create a Model
        * List Local Models
        * Show Model Information
        * Copy a Model
        * Delete a Model
        * Pull a Model
        * Push a Model
        * Generate Embeddings
        * List Running Models
    # API 接口:
        # 生成完成
        # 生成聊天完成
        # 创建模型
        # 列出本地模型
        # 展示模型信息
        # 拷贝模型
        # 删除模型
        # 拉取模型
        # 推送模型
        # 生成嵌入向量
        # 列出运行中的模型
"""

"""
# Example usage:
# Initialize the model
ollama_model = OllamaModel(model_name="llama3:8b")

# Generate completion with streaming
ollama_model.generate_completion("Why is the sky blue?", stream=True)

# Generate completion without streaming
final_response = ollama_model.generate_completion("Why is the sky blue?", stream=False)
print(final_response)

# List local models
models = ollama_model.list_local_models()
print(models)

# Show model information
model_info = ollama_model.show_model_info()
print(model_info)

"""

llama = OllamaModel()

llama.generate_completion("你好啊",True)
