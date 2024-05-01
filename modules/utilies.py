from termcolor import colored
from openai import OpenAI
client = OpenAI()
def print_colored_result(result):
    if result["kind"] == "Deployment":
        print(colored("Kind:", "green"), result["kind"])
        print(colored("Name:", "green"), result["name"])
        print(colored("Type:", "green"), result["type"])
        for error in result["errors"]:
            message=[{"role": "user", "content": error["text"]}]
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message
            )
            print(colored("Error:", "red"), error["text"])
            print(colored("Details:", "red"), completion.choices[0].message.content)
            #print(colored("Kubernetes Doc:", "red"), error["kubernetes_doc"])
            print()
    elif result["kind"] == "Pod":
        message=[{"role": "user", "content": result["message"]}]
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message
        )
        print(colored("Kind:", "green"), result["kind"])
        print(colored("Name:", "green"), result["name"])
        print(colored("Type:", "red"), result["type"])
        print(colored("Reason:", "red"), result["reason"])
        print(colored("Error:", "red"), result["message"])
        print(colored("Details:", "red"), completion.choices[0].message.content)
        print()
