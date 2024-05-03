from kubernetes import client, config
from kubernetes.client.rest import ApiException
import contextlib
class PvcAnalyzer:
    def __init__(self):
        pass

    def analyze(self, namespace):
        config.load_kube_config()
        core_v1 = client.CoreV1Api()
        kind = "PersistentVolumeClaim"
        results = []
        with contextlib.suppress(client.exceptions.ApiException):
            pvc_lists  = core_v1.list_namespaced_persistent_volume_claim(namespace).items
        pre_analysis = {}
        for pvc in pvc_lists:
            failures = []
            if pvc.status.phase == "Pending":
                with contextlib.suppress(client.exceptions.ApiException):
                    events = core_v1.list_namespaced_event(namespace, field_selector=f"involvedObject.name={pvc.metadata.name}")
                    latest_event = max(events.items, key=lambda event: event.last_timestamp)
                if latest_event.reason == "ProvisioningFailed" and latest_event.message:
                    failures.append({
                        "text": f" Pvc {pvc.metadata.namespace}/{pvc.metadata.name} Provisioning Failed"
                        })
                if failures:
                    result = {
                        "kind": "PVC",
                        "name": f"{pvc.metadata.namespace}/{pvc.metadata.name}",
                        "type": "error",
                        "reason": latest_event.reason,
                        "errors": latest_event.message
                    }
                    results.append(result)

        return(results)    
