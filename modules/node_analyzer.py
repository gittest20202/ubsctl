from kubernetes import client, config

class KubernetesNodeAnalyzer:
    def __init__(self):
        config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def check_node_issues(self):
        results = []
        try:
            nodes = self.v1.list_node().items

            for node in nodes:
                node_name = node.metadata.name
                conditions = node.status.conditions
                
                for condition in conditions:
                    if condition.status != "True":
                        result = {
                            "kind": "Node",
                            "name": node_name,
                            "type": "NodeCondition",
                            "reason": condition.type,
                            "message": f"{condition.type} is {condition.status}"
                        }
                        results.append(result)
        
        except Exception as e:
            print(f"Error: {e}")
        
        return results

