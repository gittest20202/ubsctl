from termcolor import colored
from openai import OpenAI
from openai import AzureOpenAI
import os

#api_version = os.environ["AZURE_API_VERSION"]
#azure_endpoint = os.environ["AZURE_AI_URL"]
#api_key = os.environ["AZURE_API_KEY"]
model='gpt-3.5-turbo'
#client = AzureOpenAI(api_version=api_version, azure_endpoint=azure_endpoint, api_key=api_key)
client = OpenAI()
def print_colored_result(result):
    if result["kind"] == "Deployment":
        print(colored("Kind:", "green"), colored(result["kind"],"green"))
        print(colored("Name:", "green"), colored(result["name"],"green"))
        print(colored("Type:", "green"), colored(result["type"],"green"))
        for error in result["errors"]:
            message=[{"role": "user", "content": error["text"]}]
            completion = client.chat.completions.create(
            model= model,
            messages=message
            )
            print(colored("Error:", "red"), colored(error["text"],"red"))
            print(colored("Details:", "red"), colored(completion.choices[0].message.content,"green"))
            print(colored("Kubernetes Doc:", "red"), error["kubernetes_doc"])
            print()
    elif result["kind"] == "Pod":
        message=[{"role": "user", "content": result["message"]}]
        completion = client.chat.completions.create(
        model= model,
        messages=message
        )
        print(colored("Kind:", "green"), result["kind"])
        print(colored("Name:", "green"), result["name"])
        print(colored("Type:", "red"), result["type"])
        print(colored("Reason:", "red"), result["reason"])
        print(colored("Error:", "red"), result["message"])
        print(colored("Details:", "red"), completion.choices[0].message.content)
        print()
    elif result["kind"] == "PVC":
        message=[{"role": "user", "content": result["errors"]}]
        completion = client.chat.completions.create(
        model= model,
        messages=message
        )
        print(colored("Kind:", "green"), result["kind"])
        print(colored("Name:", "green"), result["name"])
        print(colored("Type:", "red"), result["type"])
        print(colored("Error:", "red"), result["reason"])
        print(colored("Reason:", "red"), result["errors"])
        print(colored("Details:", "red"), completion.choices[0].message.content)
        print()
    elif result["kind"] == "Node":
        message=[{"role": "user", "content": result["message"]}]
        completion = client.chat.completions.create(
        model= model,
        messages=message
        )
        print(colored("Kind:", "green"), result["kind"])
        print(colored("Name:", "green"), result["name"])
        print(colored("Type:", "red"), result["type"])
        print(colored("Error:", "red"), result["reason"])
        print(colored("Reason:", "red"), result["message"])
        print(colored("Details:", "red"), completion.choices[0].message.content)
        print()
