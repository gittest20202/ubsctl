from kubernetes import client, config
from tabulate import tabulate
from termcolor import colored

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
        table_rows = []
        for namespace in namespaces:
            namespace_name = namespace.metadata.name
            services = self.api_instance.list_namespaced_service(namespace=namespace_name).items
            pods = self.api_instance.list_namespaced_pod(namespace=namespace_name).items
            deployments = self.appsv1.list_namespaced_deployment(namespace=namespace_name).items
            ingresses = self.networkingv1.list_namespaced_ingress(namespace=namespace_name).items
            pvcs = self.corev1.list_namespaced_persistent_volume_claim(namespace=namespace_name).items
            pvs = self.corev1.list_persistent_volume().items
            table_rows.append([colored(f"Namespace: {namespace_name}", "green"), "", "", "", "", ""])
            for service in services:
                table_rows.append(["", colored("Service", "blue"), colored(service.metadata.name, "blue"), "", "", ""])
            for pod in pods:
                table_rows.append(["", colored("Pod", "yellow"), colored(pod.metadata.name, "yellow"), "", "", ""])
            for deployment in deployments:
                table_rows.append(["", colored("Deployment", "magenta"), colored(deployment.metadata.name, "magenta"), "", "", ""])
            for ingress in ingresses:
                table_rows.append(["", colored("Ingress", "cyan"), colored(ingress.metadata.name, "cyan"), "", "", ""])
            for pvc in pvcs:
                table_rows.append(["", colored("PVC", "red"), colored(pvc.metadata.name, "red"), "", "", ""])
            for pv in pvs:
                table_rows.append(["", colored("PV", "green"), colored(pv.metadata.name, "green"), "", "", ""])

        return table_rows

    def print_resource_details(self):
        current_context = config.list_kube_config_contexts()[1]
        print(colored("=======================================================================================","red"))
        print(colored("Cluster Information:", "green"))
        print(colored("Cluster Name:","green"), colored(current_context['context']['cluster'],"green"))
        print(colored("=======================================================================================","red"))
        table_rows = self.get_resource_details()
        headers = [colored("Namespace","green"), colored("Resource Type","green"), colored("Name","green"), colored("Service Type","green"), colored("Port","green"), colored("URL","green")]
        print(tabulate(table_rows, headers=headers))
