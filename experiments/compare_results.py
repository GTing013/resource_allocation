import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 直接创建字体对象
font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

def plot_comparison(traditional, improved):
    metrics = ['延迟', '吞吐量', '资源利用率', '恢复时间']
    trad_values = [161.14, 694.28, 43, 35.50]
    opt_values = [66.67, 850, 75, 0.98]
    
    plt.figure(figsize=(12, 6))
    x = np.arange(len(metrics))
    width = 0.35
    
    plt.bar(x - width/2, trad_values, width, label='传统')
    plt.bar(x + width/2, opt_values, width, label='优化')
    
    plt.xlabel('性能指标', fontproperties=font)
    plt.ylabel('数值', fontproperties=font)
    plt.title('性能优化对比分析', fontproperties=font, fontsize=14)
    plt.xticks(x, metrics, fontproperties=font)
    plt.legend(prop=font)
    
    plt.savefig('/Users/huanghaoting/resource_allocation/experiments/results/performance_comparison.png', 
                dpi=300, 
                bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    plot_comparison(None, None)
    print("图表生成完成！")