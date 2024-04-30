from termcolor import colored
import openai
def print_colored_result(result):
    if result["kind"] == "Deployment":
        print(colored("Kind:", "green"), result["kind"])
        print(colored("Name:", "green"), result["name"])
        print(colored("Type:", "green"), result["type"])
        for error in result["errors"]:
            print(colored("Error:", "red"), error["text"])
            print(colored("Kubernetes Doc:", "red"), error["kubernetes_doc"])
        print()
    elif result["kind"] == "Pod":
        print(colored("Kind:", "green"), result["kind"])
        print(colored("Name:", "green"), result["name"])
        print(colored("Type:", "red"), result["type"])
        print(colored("Reason:", "red"), result["reason"])
        #print(colored("Message:", "red"), result["message"])
        print(colored("Message:", "red"), result["message"])
        print()
