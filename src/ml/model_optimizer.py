class ModelOptimizer:
    def __init__(self):
        self.learning_rate = 0.01
        self.batch_size = 32
        self.epochs = 100
        
    def optimize_model(self, model, training_data):
        """优化模型参数"""
        # 添加早停机制
        early_stopping = EarlyStopping(
            patience=5,
            min_delta=0.01
        )
        
        # 添加学习率调度
        lr_scheduler = ReduceLROnPlateau(
            factor=0.5,
            patience=3
        )
        
        # 训练模型
        history = model.fit(
            training_data,
            epochs=self.epochs,
            batch_size=self.batch_size,
            callbacks=[early_stopping, lr_scheduler]
        )
        
        return model, history