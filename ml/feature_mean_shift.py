import os
from sklearn.cluster import MeanShift, estimate_bandwidth
import pandas as pd
import numpy as np
from ml import feature_extractor
import config


def draw_correlation_heatmap(data):
    import matplotlib.pyplot as plt
    import seaborn as sb
    sb.heatmap(data.corr(), annot=False, linewidths=0.3)
    fig = plt.gcf()
    fig.set_size_inches(13, 13)
    plt.xticks(fontsize=5)
    plt.xticks(rotation='0')
    plt.yticks(fontsize=5)
    plt.show()


def write_result(target_filepath, mean_shift: MeanShift):
    # write file
    with open(target_filepath, 'w') as file:
        for group_feature in mean_shift.cluster_centers_:
            for feature in group_feature:
                file.write(str(feature) + ' ')
            file.write('\n')

        predicts = mean_shift.predict(data)
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


def check_positive_correlation_labels(data):
    result_set = set()
    for column1 in data.corr().columns:
        for column2 in data.corr().columns:
            if column1 != column2 and data.corr()[column1][column2]>= 1:
                result_set.add(column1)
                result_set.add(column2)
    print(result_set)
    return len(result_set) == 0


def data_join_columns(data, columns: list, new_column_name) -> None:
    if len(columns) <= 1:
        return
    s = data[columns[0]]
    for i in range(1, len(columns)):
        s += data[columns[i]]
    data[new_column_name] = s / len(columns)
    data.drop(columns=columns, inplace=True)


def optimize_node(data):
    # join positive correlation labels
    incidentTTP = ['stix:TTP', 'stix:Incident', 'stix:Incidents', 'incident:Description', 'incident:Incident_Reported',
                   'incident:Time', 'incident:Title', 'stixCommon:Value', 'ttp:Behavior', 'ttp:Description',
                   'ttp:Intended_Effect', 'ttp:Resources', 'ttp:Targeted_Systems', 'ttp:Title', 'ttp:Victim_Targeting']
    data_join_columns(data, incidentTTP, 'incidentTTP')
    stixCOA = ['coa:Description', 'coa:Stage', 'coa:Title', 'stix:Course_Of_Action', 'stix:Courses_Of_Action']
    data_join_columns(data, stixCOA, 'stixCOA')
    indicatorSighting = ['indicator:Sighting', 'indicator:Sightings']
    data_join_columns(data, indicatorSighting, 'indicatorSighting')
    cyberRelated = ['cybox:Related_Object', 'cybox:Related_Objects', 'cybox:Relationship']
    data_join_columns(data, cyberRelated, 'cyberRelated')
    WinRegistryKeyObjKeyValue = ['WinRegistryKeyObj:Hive', 'WinRegistryKeyObj:Key', 'WinRegistryKeyObj:Value',
                                 'WinRegistryKeyObj:Values']
    data_join_columns(data, WinRegistryKeyObjKeyValue, 'WinRegistryKeyObjKeyValue')
    WinRegistryKeyObjNameData = ['WinRegistryKeyObj:Data', 'WinRegistryKeyObj:Name']
    data_join_columns(data, WinRegistryKeyObjNameData, 'WinRegistryKeyObjNameData')
    HTTPSessionObj = ['HTTPSessionObj:HTTP_Client_Request', 'HTTPSessionObj:HTTP_Request_Header',
                      'HTTPSessionObj:HTTP_Request_Response', 'HTTPSessionObj:Parsed_Header',
                      'HTTPSessionObj:User_Agent']
    data_join_columns(data, HTTPSessionObj, 'HTTPSessionObj')
    EmailMessageObjLink = ['EmailMessageObj:Link', 'EmailMessageObj:Links']
    data_join_columns(data, EmailMessageObjLink, 'EmailMessageObjLink')
    EmailMessageObjBody = ['EmailMessageObj:Raw_Body', 'EmailMessageObj:X_Originating_IP']
    data_join_columns(data, EmailMessageObjBody, 'EmailMessageObjBody')
    EmailMessageObjFile = ['EmailMessageObj:Attachments', 'EmailMessageObj:File']
    data_join_columns(data, EmailMessageObjFile, 'EmailMessageObjFile')
    stixProfile = ['stix:Profiles', 'stixCommon:Profile']
    data_join_columns(data, stixProfile, 'stixProfile')
    stixCommon = ['stixCommon:Tools', 'cyboxCommon:Metadata', 'cyboxCommon:Tool', 'cyboxCommon:Value',
                  'stixCommon:Contributing_Sources', 'stixCommon:Source']
    data_join_columns(data, stixCommon, 'stixCommon')
    stixTime = ['stixCommon:Time', 'stix:Information_Source', 'cyboxCommon:Produced_Time']
    data_join_columns(data, stixTime, 'stixTime')
    indicator = ['indicator:Indicator', 'indicator:Composite_Indicator_Expression']
    data_join_columns(data, indicator, 'indicator')
    cyboxCommonHash = ['cyboxCommon:Type', 'FileObj:Hashes', 'cyboxCommon:Hash', 'cyboxCommon:Simple_Hash_Value']
    data_join_columns(data, cyboxCommonHash, 'cyboxCommonHash')
    cyboxCommonProperty = ['cyboxCommon:Property', 'cyboxCommon:Custom_Properties']
    data_join_columns(data, cyboxCommonProperty, 'cyboxCommonProperty')


if __name__ == '__main__':
    dataDirectoryPath = config.ML_DATA_PATH

    # # node data
    # node_data, labels,filenames = feature_extractor.feature_file_loader(os.path.join(dataDirectoryPath, 'node.txt'))
    # data = pd.DataFrame(data=np.array(node_data), columns=labels, index=filenames)
    # optimize_node(data)

    # title data
    title_data, labels, filenames = feature_extractor.feature_file_loader((os.path.join(dataDirectoryPath, 'title.txt')))
    data = pd.DataFrame(data=np.array(title_data), columns=labels, index=filenames)

    #draw_correlation_heatmap(data)

    bandwidth = estimate_bandwidth(data, quantile=0.1)
    ms = MeanShift(bandwidth=bandwidth)
    ms.fit(data)
    print(ms.cluster_centers_)
    write_result(os.path.join(dataDirectoryPath, 'title_ms.txt'), ms)

