#!/usr/bin/env python
import argparse
from modules.deployment_analyzer import DeploymentAnalyzer
from modules.pod_analyzer import PodAnalyzer
from modules.pvc_analyzer import PvcAnalyzer
from modules.log_analyzer import LogAnalyzer
from modules.utilies import print_colored_result
from openai import OpenAI

def main():
    print("========================================")
    print("Welcome to the UBS Kubernetes Analyzer Tool!")
    print("========================================")
    parser = argparse.ArgumentParser(description="Kubernetes Analyzer Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyser subcommand
    analyser_parser = subparsers.add_parser("analyser", help="Analyze Kubernetes resources")
    analyser_parser.add_argument("-k", "--kind", choices=["pod", "pods", "deploy", "deployment","pvc", "pvcs"], help="Specify the resource kind (pod/pods or deploy/deployment or pvc/pvcs)")
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
                    results = analyzer.analyze_deployments_ns(args.namespace, args.deployment)
                    for result in results:
                        print_colored_result(result)
                else:
                    analyser_parser.print_help()
            else:
                analyzer = DeploymentAnalyzer()
                results = analyzer.analyze_deployments()
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

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
analyzer = PvcAnalyzer()
analyzer.analyze(namespace="default")

