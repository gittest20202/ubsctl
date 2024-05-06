from tabulate import tabulate
from termcolor import colored
from kubernetes import client, config

class KubernetesResourceViewer:
    def __init__(self):
        config.load_kube_config()
        self.api_instance = client.CoreV1Api()
        self.appsv1 = client.AppsV1Api()
        self.networkingv1 = client.NetworkingV1Api()
        self.corev1 = client.CoreV1Api()
        self.storagev1 = client.StorageV1Api()

    def get_resource_details(self):
        namespaces = self.api_instance.list_namespace().items
        resources_by_type = {
            "Namespace": [],
            "Deployment": [],
            "Pod": [],
            "Service": [],
            "PVC": [],
            "Ingress": []
        }

        for namespace in namespaces:
            namespace_name = namespace.metadata.name
            resources_by_type["Namespace"].append(namespace_name)

            services = self.api_instance.list_namespaced_service(namespace=namespace_name).items
            for service in services:
                resources_by_type["Service"].append(service.metadata.name)

            pods = self.api_instance.list_namespaced_pod(namespace=namespace_name).items
            for pod in pods:
                resources_by_type["Pod"].append(pod.metadata.name)

            deployments = self.appsv1.list_namespaced_deployment(namespace=namespace_name).items
            for deployment in deployments:
                resources_by_type["Deployment"].append(deployment.metadata.name)

            ingresses = self.networkingv1.list_namespaced_ingress(namespace=namespace_name).items
            for ingress in ingresses:
                resources_by_type["Ingress"].append(ingress.metadata.name)

            pvcs = self.corev1.list_namespaced_persistent_volume_claim(namespace=namespace_name).items
            for pvc in pvcs:
                resources_by_type["PVC"].append(pvc.metadata.name)

        return resources_by_type

    def print_resource_details(self):
        print(colored("=======================================================================================", "red"))
        print(colored("Cluster Information:", "green"))
        current_context = config.list_kube_config_contexts()[1]
        print(colored("Cluster Name:", "green"), colored(current_context['context']['cluster'], "green"))
        print(colored("=======================================================================================", "red"))

        resources_by_type = self.get_resource_details()
        table_rows = []
        for resource_type, resource_names in resources_by_type.items():
            for resource_name in resource_names:
                table_rows.append([colored(resource_type, "green"), colored(resource_name, "white")])

        headers = [colored("Resource Type", "green"), colored("Name", "green")]
        print(tabulate(table_rows, headers=headers, tablefmt="plain"))

viewer = KubernetesResourceViewer()
viewer.print_resource_details()
