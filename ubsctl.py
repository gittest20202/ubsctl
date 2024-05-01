#!/usr/bin/env python
import argparse
from modules.deployment_analyzer import DeploymentAnalyzer
from modules.pod_analyzer import PodAnalyzer
from modules.utilies import print_colored_result
from openai import OpenAI
def main():
    print("========================================")
    print("Welcome to the UBS Kubernetes Analyzer Tool!")
    print("========================================")
    parser = argparse.ArgumentParser(description="Kubernetes Analyzer Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    analyser_parser = subparsers.add_parser("analyser", help="Analyze Kubernetes resources")
    analyser_parser.add_argument("-k", "--kind", choices=["pod", "pods", "deploy", "deployment"], help="Specify the resource kind (pod/pods or deploy/deployment)")
    analyser_parser.add_argument("-n", "--namespace", help="Specify the namespace")
    analyser_parser.add_argument("-d", "--deployment", help="Specify the deployment name")
    args = parser.parse_args()
    if args.command == "analyser":
        if args.kind in ["pod","pods"]:
            analyzer = PodAnalyzer()
            results = analyzer.analyze_pod_lifecycle()
            for result in results:
                print_colored_result(result)
        elif args.kind in ["deploy","deployment"]:
            if args.namespace:
                if args.deployment:
                  analyzer = DeploymentAnalyzer()
                  results=analyzer.analyze_deployments_ns(args.namespace,args.deployment)  
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
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

