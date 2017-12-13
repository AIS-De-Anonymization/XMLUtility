from xml.dom import minidom
import os
import config


def extractRedactedText(filePath):
    textList = []
    root = minidom.parse(filePath).documentElement
    if root.getElementsByTagName('stix:Indicators'):
        indicators = root.getElementsByTagName('stix:Indicators')[0]
        for indicator in indicators.childNodes:
            descriptionNodeList = indicator.getElementsByTagName('indicator:Description')
            if descriptionNodeList:
                descriptionNode = descriptionNodeList[0]
                if descriptionNode.childNodes:
                    textNode = descriptionNode.childNodes[0]
                    text = textNode.nodeValue
                    if 'REDACTED' in text:
                        textList.append(text)
        return textList


def saveToFile(target_path, textList):
    f = open(target_path, 'w')
    if textList:
        for text in textList:
            f.write(text.encode('ascii', 'ignore').decode('ascii') + '\n')
    f.close()

def copyRawXML(origin_path, origin_txt_path, target_path):
    for filename in os.listdir(origin_txt_path):
        real_filename = filename[0:-4] + '.xml'
        os.symlink(os.path.join(origin_path, real_filename), os.path.join(target_path, real_filename))


if __name__ == '__main__':
    txtPath='../../dispatch.isi.jhu.edu/extracted/'
    copyRawXML(config.DIRECTORY_PATH,txtPath,config.SAVE_DIRECTORY_PATH)
    exit() # remove to extract
    directoryPath = config.DIRECTORY_PATH
    saveDirectoryPath = config.SAVE_DIRECTORY_PATH
    for filename in os.listdir(directoryPath):
        saveFilename = filename[:filename.index('.')] + '.txt'
        saveToFile(os.path.join(saveDirectoryPath, saveFilename), extractRedactedText(os.path.join(directoryPath, filename)))
    print('END')