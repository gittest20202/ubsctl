#!/usr/bin/env python
import argparse
from modules.deployment_analyzer import DeploymentAnalyzer
from modules.pod_analyzer import PodAnalyzer
from modules.pvc_analyzer import PvcAnalyzer
from modules.cluster_detail import KubernetesResourceViewer
from modules.log_analyzer import LogAnalyzer
from modules.utilies import print_colored_result
from openai import OpenAI
from termcolor import colored
import pyfiglet

def main():
    print(colored("===========================================================================================================================================================================================","green"))
    text = "Welcome to UBS Kubernetes Analyzer Tool!"
    banner = pyfiglet.figlet_format(text, width=200)
    print(colored(banner,"green"))
    print(colored("===========================================================================================================================================================================================","green"))
    print()
    print()
    parser = argparse.ArgumentParser(description="Kubernetes Analyzer Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Cluster Details
    analyser_parser = subparsers.add_parser("cluster-details", help="Cluster Details")
    # Analyser subcommand
    analyser_parser = subparsers.add_parser("analyser", help="Analyze Kubernetes resources")
    analyser_parser.add_argument("-k", "--kind", choices=["pod", "pods", "deploy", "deployment","pvc", "pvcs","svc","services","service"], help="Specify the resource kind (pod/pods or deploy/deployment or pvc/pvcs or svc/service/services)")
    analyser_parser.add_argument("-n", "--namespace", help="Specify the namespace")
    analyser_parser.add_argument("-d", "--deployment", help="Specify the deployment name")
    analyser_parser.add_argument("-p", "--pvc", help="Specify the pvc name")
    
    # Logs subcommand
    logs_parser = subparsers.add_parser("logs", help="Get logs of Kubernetes resources")
    logs_parser.add_argument("-k", "--kind", choices=["pod", "pods"], help="Specify the resource kind (pod/pods)")
    logs_parser.add_argument("-n", "--namespace", help="Specify the namespace")
    logs_parser.add_argument("-p", "--pod", help="Specify the pod name")

    args = parser.parse_args()
    
    if args.command == "analyser":
        if args.kind in ["pod", "pods"]:
            analyzer = PodAnalyzer()
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
                    analyzer = DeploymentAnalyzer()
                    results = analyzer.analyze_all(args.namespace)
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
         viewer = KubernetesResourceViewer()
         viewer.print_resource_details()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
analyzer = PvcAnalyzer()
analyzer.analyze(namespace="default")

