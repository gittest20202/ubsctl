#!/usr/bin/env python
import argparse
from modules.deployment_analyzer import DeploymentAnalyzer
from modules.pod_analyzer import PodAnalyzer
from modules.utilies import print_colored_result
def main():
    print("========================================")
    print("Welcome to the UBS Kubernetes Analyzer Tool!")
    print("========================================")
    parser = argparse.ArgumentParser(description="Kubernetes Analyzer Tool")
    parser.add_argument("-k", "--kind", choices=["pod", "deploy"], help="Specify the resource kind (pod or deploy)")
    args = parser.parse_args()
    if args.kind == "pod":
        analyzer = PodAnalyzer()
        results = analyzer.analyze_pod_lifecycle()
        for result in results:
            print_colored_result(result)
    elif args.kind == "deploy":
        analyzer = DeploymentAnalyzer()
        results = analyzer.analyze_deployments()
        for result in results:
            print_colored_result(result)
    else:
        parser.print_help()
if __name__ == "__main__":
    main()

