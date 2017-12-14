import os
from sklearn.cluster import MeanShift, estimate_bandwidth
from ml import feature_extractor
import config

if __name__ == '__main__':
    dataDirectoryPath = config.ML_DATA_PATH
    data, filenames = feature_extractor.data_loader(os.path.join(dataDirectoryPath, 'node.txt'))
    bandwidth = estimate_bandwidth(data, quantile=0.1)
    ms = MeanShift(bandwidth=bandwidth)
    ms.fit(data)
    with open(os.path.join(dataDirectoryPath, 'node_ms.txt'), 'w') as file:
        for group_feature in ms.cluster_centers_:
            for feature in group_feature:
                file.write(str(feature) + ' ')
            file.write('\n')

        predicts = ms.predict(data)
        clusters = {}
        for i in range(0, len(predicts)):
            if predicts[i] in clusters:
                clusters[predicts[i]].append(filenames[i])
            else:
                clusters[predicts[i]] = [filenames[i]]

        for num, file_names in clusters.items():
            file.write(str(num))
            for file_name in file_names:
                file.write(' ' + file_name)
            file.write('\n')
