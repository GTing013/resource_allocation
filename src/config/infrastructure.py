class InfrastructureConfig:
    def __init__(self):
        self.prometheus_url = 'prometheus:9090'
        self.kubernetes_config = {
            'namespace': 'resource-allocation',
            'deployment_template': 'deployment.yaml',
            'service_template': 'service.yaml'
        }
        self.monitoring_interval = 60  # 秒
        self.resource_limits = {
            'cpu': 8,
            'memory': '16Gi',
            'storage': '100Gi'
        }