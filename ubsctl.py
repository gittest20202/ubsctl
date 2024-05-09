#!/usr/bin/env python
import argparse
from modules.deployment_analyzer import DeploymentAnalyzer
from modules.pod_analyzer import PodLifecycleAnalyzer
from modules.pvc_analyzer import PvcAnalyzer
from modules.cluster_detail import KubernetesResourceViewer
from modules.log_analyzer import LogAnalyzer
from modules.node_analyzer import KubernetesNodeAnalyzer
from modules.service_analyzer import ServiceAnalyzer
from modules.utilies import print_colored_result
from openai import OpenAI
from termcolor import colored
import os

def set_env_variable():
    AZURE_API_VERSION = input("Enter API Version: ")
    AZURE_API_KEY = input("Enter API Key: ")
    MODEL = input("Enter your Model Name: ")
    AZURE_AI_URL = input("Enter your URL: ")

    os.environ["AZURE_API_VERSION"] = AZURE_API_VERSION
    os.environ["MODEL"] = MODEL
    os.environ["AZURE_AI_URL"] = AZURE_AI_URL
    os.environ["AZURE_API_KEY"] = AZURE_API_KEY

    print("Environment variables set successfully.")
    exit()
def main():
    print(colored("===========================================================================================================================================================================================","green"))
    text = "Welcome to UBS Kubernetes Analyzer Tool!"
    #banner = pyfiglet.figlet_format(text, width=200)
    print(colored(text,"green"))
    print(colored("===========================================================================================================================================================================================","green"))
    print()
    print()
    parser = argparse.ArgumentParser(description="Kubernetes Analyzer Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
   




    # Cluster Details
    analyser_parser = subparsers.add_parser("cluster-details", help="Cluster Details")
    analyser_parser.add_argument("-n", "--namespace", help="Specify the namespace")
    # Analyser subcommand
    analyser_parser = subparsers.add_parser("analyser", help="Analyze Kubernetes resources")
    analyser_parser.add_argument("-k", "--kind", choices=["pod", "pods", "deploy", "deployment","pvc", "pvcs","svc","services","service","nodes"], help="Specify the resource kind (pod/pods or deploy/deployment or pvc/pvcs or svc/service/services)")
    analyser_parser.add_argument("-n", "--namespace", help="Specify the namespace")
    analyser_parser.add_argument("-d", "--deployment", help="Specify the deployment name")
    analyser_parser.add_argument("-p", "--pvc", help="Specify the pvc name")
   
    
    logs_parser = subparsers.add_parser("set", help="Set OpenAI Creds")
    # Logs subcommand
    logs_parser = subparsers.add_parser("logs", help="Get logs of Kubernetes resources")
    logs_parser.add_argument("-k", "--kind", choices=["pod", "pods"], help="Specify the resource kind (pod/pods)")
    logs_parser.add_argument("-n", "--namespace", help="Specify the namespace")
    logs_parser.add_argument("-p", "--pod", help="Specify the pod name")

    args = parser.parse_args()
    
    if args.command == "analyser":
        if args.kind in ["pod", "pods"]:
            if args.namespace:
                analyzer = PodLifecycleAnalyzer()
                results =  analyzer.analyze_pod_lifecycle(args.namespace)
                for result in results:
                  print_colored_result(result)
            else:    
                analyzer = PodLifecycleAnalyzer()
                results = analyzer.analyze_pod_lifecycle()
                for result in results:
                  print_colored_result(result)
        elif args.kind in ["pvc","pvcs"]:
            if args.namespace:
              analyzer = PvcAnalyzer()
              results = analyzer.analyze(namespace=args.namespace)
              for result in results:
                print_colored_result(result)
            else:
               analyser_parser.print_help()
        elif args.kind in ["nodes"]:
             analyzer = KubernetesNodeAnalyzer()
             issues = analyzer.check_node_issues()
             for issue in issues:
                 print_colored_result(issue)
        elif args.kind in ["deploy", "deployment"]:
            if args.namespace:
                if args.deployment:
                    analyzer = DeploymentAnalyzer()
                    results = analyzer.analyze_deployments(args.namespace, args.deployment)
                    for result in results:
                        print_colored_result(result)
                else:
                    analyzer = DeploymentAnalyzer()
                    results = analyzer.analyze_deployments(args.namespace)
                    for result in results:
                        print_colored_result(result)
            else:
                analyzer = DeploymentAnalyzer()
                results = analyzer.analyze_deployments()
                for result in results:
                    print_colored_result(result)
    
        elif args.kind in ["svc", "services", "service"]:
            if args.namespace:
                analyzer = ServiceAnalyzer()
                results = analyzer.analyze_ns(args.namespace)
                for result in results:
                        print_colored_result(result)
            else:
                    analyzer = ServiceAnalyzer()
                    results = analyzer.analyze_all()
                    for result in results:
                        print_colored_result(result)
        else:
            analyser_parser.print_help()
    elif args.command == "logs":
        if args.kind in ["pod","pods"]:
            analyzer = LogAnalyzer()
            results = analyzer.analyze_all_pods()
            for result in results:
                  print_colored_result(result)
        else:
            logs_parser.print_help()

    elif args.command == "cluster-details":
         if args.namespace:
           viewer = KubernetesResourceViewer()
           viewer.print_resource_details(args.namespace)
         else :
           viewer = KubernetesResourceViewer()
           viewer.print_resource_details()
    elif args.command == "set":
        set_env_variable()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
analyzer = PvcAnalyzer()
analyzer.analyze(namespace="default")

