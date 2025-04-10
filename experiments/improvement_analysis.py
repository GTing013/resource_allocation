import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 直接创建字体对象
font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

def plot_improvement():
    metrics = ['延迟', '吞吐量', '资源利用率', '恢复时间']
    before_values = [161.14, 333.33, 43, 35.50]
    after_values = [161.14, 694.28, 75, 1.21]
    
    plt.figure(figsize=(12, 6))
    x = np.arange(len(metrics))
    width = 0.35
    
    plt.bar(x - width/2, before_values, width, label='优化前')
    plt.bar(x + width/2, after_values, width, label='优化后')
    
    plt.xlabel('性能指标', fontproperties=font)
    plt.ylabel('数值', fontproperties=font)
    plt.title('性能改进分析', fontproperties=font, fontsize=14)
    plt.xticks(x, metrics, fontproperties=font)
    plt.legend(prop=font)
    
    plt.savefig('/Users/huanghaoting/resource_allocation/experiments/results/improvement_analysis.png', 
                dpi=300, 
                bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    plot_improvement()
    print("改进分析图表生成完成！")