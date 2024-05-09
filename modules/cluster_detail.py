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

    def create_tables(self, namespace,name=None):
        table_rows = []
        if name:
          namespace_name = namespace
        else:  
          namespace_name = namespace.metadata.name
        services = self.api_instance.list_namespaced_service(namespace=namespace_name).items
        pods = self.api_instance.list_namespaced_pod(namespace=namespace_name).items
        deployments = self.appsv1.list_namespaced_deployment(namespace=namespace_name).items
        ingresses = self.networkingv1.list_namespaced_ingress(namespace=namespace_name).items
        pvcs = self.corev1.list_namespaced_persistent_volume_claim(namespace=namespace_name).items
        pvs = self.corev1.list_persistent_volume().items

        for service in services:
            service_type = service.spec.type if service.spec.type else "N/A"
            port = service.spec.ports[0].port if service.spec.ports else "N/A"
            table_rows.append([namespace_name, "Service", service.metadata.name, service_type, port, ""])
        for pod in pods:
            table_rows.append([namespace_name, "Pod", pod.metadata.name, "", "", ""])
        for deployment in deployments:
            table_rows.append([namespace_name, "Deployment", deployment.metadata.name, "", "", ""])
        for ingress in ingresses:
            url = ", ".join(rule.host for rule in ingress.spec.rules) if ingress.spec.rules else "N/A"
            table_rows.append([namespace_name, "Ingress", ingress.metadata.name, "", "", url])
        for pvc in pvcs:
            table_rows.append([namespace_name, "PVC", pvc.metadata.name, "", "", ""])
        for pv in pvs:
            table_rows.append([namespace_name, "PV", pv.metadata.name, "", "", ""])

        return table_rows

    def get_resource_details(self, namespace_name=None):
        tables = []  
        if namespace_name is not None:
            namespaces = namespace_name
            tables.append(self.create_tables(namespaces,name=True))
            return tables    
        else:
          namespaces = self.api_instance.list_namespace().items
          for namespace_name in namespaces:
            tables.append(self.create_tables(namespace_name))
        return tables

    def print_resource_details(self, namespace_name=None):
        current_context = config.list_kube_config_contexts()[1]
        print(colored("=======================================================================================", "red"))
        print(colored("Cluster Information:", "green"))
        print(colored("Cluster Name:", "green"), colored(current_context['context']['cluster'], "green"))
        print(colored("=======================================================================================", "red"))

        tables = self.get_resource_details(namespace_name)
        headers = [colored("Namespace", "green"), colored("Resource Type", "green"), colored("Name", "green"),
                   colored("Service Type", "green"), colored("Port", "green"), colored("URL", "green")]
        for table in tables:
            print(tabulate(table, headers=headers, tablefmt="grid"))
