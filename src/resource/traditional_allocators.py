class TraditionalAllocators:
    def __init__(self):
        self.resources = {
            'cpu': {'total': 100, 'allocated': 0},
            'memory': {'total': 1024, 'allocated': 0}  # GB
        }

    def round_robin(self, tasks):
        """轮询（Round Robin）分配
        - 优点：公平，简单
        - 缺点：不考虑任务优先级和资源需求差异
        """
        allocated = {}
        available_resources = self.resources['cpu']['total']
        share = available_resources / len(tasks)
        
        for task in tasks:
            allocated[task.id] = share
            
        return allocated

    def static_priority(self, tasks):
        """静态优先级分配
        - 优点：考虑业务重要性
        - 缺点：资源利用率低，优先级低的任务可能长期得不到资源
        """
        allocated = {}
        available_resources = self.resources['cpu']['total']
        
        # 按优先级排序
        sorted_tasks = sorted(tasks, key=lambda x: x.priority, reverse=True)
        
        for task in sorted_tasks:
            if task.priority == 'high':
                allocated[task.id] = available_resources * 0.5
            elif task.priority == 'medium':
                allocated[task.id] = available_resources * 0.3
            else:
                allocated[task.id] = available_resources * 0.2
                
        return allocated

    def fixed_quota(self, tasks):
        """固定配额分配
        - 优点：稳定，可预测
        - 缺点：资源浪费，无法应对负载变化
        """
        allocated = {}
        quotas = {
            'small': 0.2,
            'medium': 0.3,
            'large': 0.5
        }
        
        for task in tasks:
            allocated[task.id] = self.resources['cpu']['total'] * quotas[task.size]
            
        return allocated

    def threshold_based(self, tasks, metrics):
        """阈值触发分配
        - 优点：简单的动态调整
        - 缺点：反应滞后，容易震荡
        """
        allocated = {}
        base_allocation = self.resources['cpu']['total'] / len(tasks)
        
        for task in tasks:
            cpu_usage = metrics[task.id]['cpu_usage']
            if cpu_usage > 80:
                allocated[task.id] = base_allocation * 1.5
            elif cpu_usage < 30:
                allocated[task.id] = base_allocation * 0.8
            else:
                allocated[task.id] = base_allocation
                
        return allocated

    def proportional_share(self, tasks):
        """比例分配
        - 优点：按需分配
        - 缺点：可能出现资源争抢
        """
        allocated = {}
        total_weight = sum(task.weight for task in tasks)
        
        for task in tasks:
            share = (task.weight / total_weight) * self.resources['cpu']['total']
            allocated[task.id] = share
            
        return allocated