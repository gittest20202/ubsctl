import re
import nltk
from nltk.chat.util import Chat, reflections
from kubernetes import client, config
import argparse
from modules.deployment_analyzer import DeploymentAnalyzer
from modules.pod_analyzer import PodLifecycleAnalyzer
from modules.pvc_analyzer import PvcAnalyzer
from modules.cluster_detail import KubernetesResourceViewer
from modules.log_analyzer import LogAnalyzer
from modules.node_analyzer import KubernetesNodeAnalyzer
from modules.service_analyzer import ServiceAnalyzer
from modules.utilies import print_colored_result
# Load the Kubernetes configuration
def load_kube_config():
    try:
        config.load_kube_config()  # For local development
    except:
        config.load_incluster_config()  # For running inside a Kubernetes cluster


# Define chatbot responses
pairs = [
    [
        r"(please|can you|could you|would you)? analyze pods in namespace (.*)",
        ["Analyzing pods in namespace %2...",]
    ],
    [
        r"(please|can you|could you|would you)? analyze pod (.*) in namespace (.*)",
        ["Analyzing pod %2 in namespace %3...",]
    ],
    [
        r"(please|can you|could you|would you)? analyze deployments in namespace (.*)",
        ["Analyzing deployments in namespace %2...",]
    ],
    [
        r"(please|can you|could you|would you)? get logs of pod (.*) in namespace (.*)",
        ["Fetching logs for pod %2 in namespace %3...",]
    ],
    [
        r"(please|can you|could you|would you)? fetch cluster details",
        ["Fetching cluster details...",]
    ],
    [
        r"(please|can you|could you|would you)? fetch cluster details in namespace (.*)",
        ["Fetching cluster details for namespace %2...",]
    ],
    [
        r"quit",
        ["Goodbye! Have a great day ahead!",]
    ],
    [
        r"(.*)",
        ["I'm sorry, I don't understand that. Could you please rephrase?",]
    ],
]

def analyze_resources(resource, namespace, pod_name=None):
    if not namespace_exists(namespace):
        return f"Namespace '{namespace}' does not exist."
    
    if resource == 'pods':
        items = get_pods(namespace)
    elif resource == 'deployments':
        items = get_deployments(namespace)
    elif resource == 'pod' and pod_name:
        if not pod_exists(namespace, pod_name):
            return f"Pod '{pod_name}' does not exist in namespace '{namespace}'."
        return f"Pod '{pod_name}' exists in namespace '{namespace}'."
    else:
        return "Unknown resource type."
    
    if not items:
        return f"No {resource} found in namespace {namespace}."
    return f"Found {len(items)} {resource} in namespace {namespace}: " + ", ".join(items)

def chatbot():
    print("Hi, I'm your friendly chatbot. Type 'quit' to exit.")
    chat = Chat(pairs, reflections)
    
    while True:
        user_input = input("KUBERNETES BOT> ")
        if user_input.lower() == 'quit' or user_input.lower() == "exit":
            print("Goodbye! Have a great day ahead!")
            break
        
        matched = False
        for pattern, responses in pairs:
            match = re.match(pattern, user_input, re.IGNORECASE)
            if match:
                response = responses[0]
                if "analyzing pods" in response.lower():
                    namespace = match.group(2)
                    analyzer = PodLifecycleAnalyzer()
                    results =  analyzer.analyze_pod_lifecycle()
                    for result in results:
                        print_colored_result(result)
                    matched = True
                    break
                elif "analyzing pod" in response.lower():
                    namespace = match.group(3)
                    analyzer = PodLifecycleAnalyzer()
                    results =  analyzer.analyze_pod_lifecycle(namespace)
                    for result in results:
                        print_colored_result(result)
                    matched = True
                    break
                elif "analyzing deployments" in response.lower():
                    namespace = match.group(2)
                    analysis = analyze_resources('deployments', namespace)
                    print(analysis)
                    matched = True
                    break
                elif "fetching logs" in response.lower():
                    pod_name = match.group(2)
                    namespace = match.group(3)
                    if not namespace_exists(namespace):
                        print(f"Namespace '{namespace}' does not exist.")
                        matched = True
                        break
                    if not pod_exists(namespace, pod_name):
                        print(f"Pod '{pod_name}' does not exist in namespace '{namespace}'.")
                        matched = True
                        break
                    logs = get_pod_logs(namespace, pod_name)
                    print(logs)
                    matched = True
                    break
                elif "fetching cluster details" in response.lower():
                    if "namespace" in response.lower():
                        namespace = match.group(2)
                        details = get_cluster_details(namespace)
                    else:
                        details = get_cluster_details()
                    print(details)
                    matched = True
                    break
                else:
                    response = response % match.groups()
                print(response)
                matched = True
                break
        
        if not matched:
            print("I'm sorry, I don't understand that. Could you please rephrase?")

if __name__ == "__main__":
    load_kube_config()
    chatbot()

