import numpy as np
import matplotlib.pyplot as plt
def data_info(data,show_fig=False):
    all_features=[]
    for key in data:
        feature=data[key]

        print(f" {key} feature about max, min, average, median: ", np.max(feature),np.min(feature),np.mean(feature),np.median(feature))
        if feature:
            all_features.append(feature)
    if show_fig:
        plt.violinplot(all_features)
        plt.show()
