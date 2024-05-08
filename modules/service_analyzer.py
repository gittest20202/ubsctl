from kubernetes import client, config
from kubernetes.client.rest import ApiException
import contextlib

class ServiceAnalyzer:
    def __init__(self):
        pass

    def analyze_all(self, service_list=None):
        config.load_kube_config()
        results = []
        v1 = client.CoreV1Api()
        with contextlib.suppress(client.exceptions.ApiException):
            if service_list is None:
               service_list = v1.list_service_for_all_namespaces()
            for service in service_list.items:
                failures = []
                if not service.spec.ports:
                    failures.append(f"Service has no endpoints: {service.metadata.namespace}/{service.metadata.name}")
                elif hasattr(service, 'subsets'):  
                    for subset in service.subsets:
                        if subset.not_ready_addresses:
                            pods = [address.target_ref.kind + "/" + address.target_ref.name for address in subset.not_ready_addresses]
                            failures.append(f"Service has not ready endpoints, pods: {pods}")

                if failures:
                    results.append({
                        "kind": "Service",
                        "name": f"{service.metadata.namespace}/{service.metadata.name}",
                        "error": failures
                    })
        return results

    def analyze_ns(self, namespace):
        config.load_kube_config()
        v1 = client.CoreV1Api()
        with contextlib.suppress(client.exceptions.ApiException):
            service_list = v1.list_namespaced_service(namespace)
            return self.analyze_all(service_list)

