import numpy as np
from typing import List, Tuple, Dict
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import time
import logging

logging.basicConfig(level=logging.INFO)

class MLResourceAllocator:
    def __init__(self, history_window: int = 100, prediction_window: int = 10):
        self.history_window = history_window
        self.prediction_window = prediction_window
        self.cpu_history: List[float] = []
        self.memory_history: List[float] = []
        self.scaler = StandardScaler()
        self.model = RandomForestRegressor(n_estimators=100)
        self.is_model_trained = False

    def update_metrics(self, cpu_usage: float, memory_usage: float):
        """更新资源使用历史"""
        self.cpu_history.append(cpu_usage)
        self.memory_history.append(memory_usage)

        if len(self.cpu_history) > self.history_window:
            self.cpu_history = self.cpu_history[-self.history_window:]
            self.memory_history = self.memory_history[-self.history_window:]

    def prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """准备训练数据"""
        if len(self.cpu_history) < self.history_window:
            raise ValueError("Insufficient historical data for training")

        X = []
        y_cpu = []
        y_memory = []

        for i in range(len(self.cpu_history) - self.prediction_window):
            X.append([
                self.cpu_history[i:i+self.prediction_window],
                self.memory_history[i:i+self.prediction_window]
            ])
            y_cpu.append(self.cpu_history[i+self.prediction_window])
            y_memory.append(self.memory_history[i+self.prediction_window])

        X = np.array(X)
        y = np.column_stack((y_cpu, y_memory))

        return X, y

    def train_model(self):
        """训练预测模型"""
        if len(self.cpu_history) < self.history_window:
            logging.warning("Not enough data for training")
            return

        try:
            X, y = self.prepare_training_data()
            X_reshaped = X.reshape(X.shape[0], -1)
            X_scaled = self.scaler.fit_transform(X_reshaped)
            self.model.fit(X_scaled, y)
            self.is_model_trained = True
            logging.info("Model training completed successfully")
        except Exception as e:
            logging.error(f"Error during model training: {e}")

    def predict_resource_demand(self) -> Tuple[float, float]:
        """预测未来资源需求"""
        if not self.is_model_trained:
            return np.mean(self.cpu_history), np.mean(self.memory_history)

        try:
            recent_data = np.array([
                self.cpu_history[-self.prediction_window:],
                self.memory_history[-self.prediction_window:]
            ])
            recent_data_reshaped = recent_data.reshape(1, -1)
            recent_data_scaled = self.scaler.transform(recent_data_reshaped)
            prediction = self.model.predict(recent_data_scaled)[0]
            
            # 添加安全边界
            cpu_prediction = max(prediction[0] * 1.1, 0.1)  # 至少保留10%CPU
            memory_prediction = max(prediction[1] * 1.1, 0.1)  # 至少保留10%内存
            
            return cpu_prediction, memory_prediction
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            return np.mean(self.cpu_history), np.mean(self.memory_history)

    def allocate_resources(self, available_cpu: float, available_memory: float) -> Dict[str, float]:
        """根据预测结果分配资源"""
        cpu_demand, memory_demand = self.predict_resource_demand()
        
        # 计算分配比例
        cpu_allocation = min(cpu_demand, available_cpu)
        memory_allocation = min(memory_demand, available_memory)
        
        return {
            'cpu': cpu_allocation,
            'memory': memory_allocation
        }

    def evaluate_performance(self, actual_cpu: float, actual_memory: float) -> Dict[str, float]:
        """评估分配性能"""
        predicted_cpu, predicted_memory = self.predict_resource_demand()
        
        cpu_error = abs(predicted_cpu - actual_cpu) / actual_cpu if actual_cpu > 0 else 0
        memory_error = abs(predicted_memory - actual_memory) / actual_memory if actual_memory > 0 else 0
        
        return {
            'cpu_prediction_error': cpu_error,
            'memory_prediction_error': memory_error,
            'average_error': (cpu_error + memory_error) / 2
        }