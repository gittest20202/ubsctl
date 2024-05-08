import contextlib
from kubernetes import client, config

class PodLifecycleAnalyzer:
    def analyze_pod_lifecycle(self, namespace=None):
        config.load_kube_config()
        core_v1 = client.CoreV1Api()
        results = []

        with contextlib.suppress(client.exceptions.ApiException):
            events_list = core_v1.list_event_for_all_namespaces().items if not namespace else \
                core_v1.list_namespaced_event(namespace).items
            for event in events_list:
                if event.involved_object.kind.lower() == "pod" and event.reason in [
                    "Failed", "ImagePullBackOff", "CrashLoopBackOff", "OOMKilled",
                    "FailedCreatePodSandBox", "Pending", "Unhealthy", "ErrImageNeverPull",
                    "ImageInspectError", "CreateContainerConfigError", "CreateContainerError",
                    "InvalidImageName", "FailedScheduling"
                ]:
                    result = {
                        "kind": event.involved_object.kind,
                        "name": f"{event.involved_object.namespace}/{event.involved_object.name}",
                        "type": event.type,
                        "reason": event.reason,
                        "message": event.message,
                    }
                    results.append(result)

        # Check Pod status against additional conditions
        pod_list = core_v1.list_pod_for_all_namespaces(watch=False).items if not namespace else \
            core_v1.list_namespaced_pod(namespace).items
        for pod in pod_list:
            status = pod.status.container_statuses
            if isinstance(status, list):
                for container_status in pod.status.container_statuses:
                    if container_status.state.waiting:
                        if container_status.state.waiting.reason in [
                            "Failed", "ImagePullBackOff", "CrashLoopBackOff", "OOMKilled",
                            "FailedCreatePodSandBox", "Pending", "Unhealthy", "ErrImageNeverPull",
                            "ImageInspectError", "CreateContainerConfigError", "CreateContainerError",
                            "InvalidImageName", "FailedScheduling", "Pending"
                        ]:
                            result = {
                                "kind": "Pod",
                                "name": f"{pod.metadata.namespace}/{pod.metadata.name}",
                                "type": "Warning",
                                "reason": "PodStatusCondition",
                                "message": f"Pod status is '{container_status.state.waiting.reason}'",
                            }
                            results.append(result)

        return results

