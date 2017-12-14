import os


WORK_PATH = os.environ.get('WORK_PATH')

DIRECTORY_PATH = os.path.join(WORK_PATH, 'ais_201710')
SAVE_DIRECTORY_PATH = os.path.join(WORK_PATH, 'classifyFiles/DC_IndustryType')
ML_DIRECTORY_PATH = os.path.join(WORK_PATH, 'classifyFiles/DC_IndustryType/IndustryType="Information Technology Sector"')
ML_SAVE_DIRECTORY_PATH = os.path.join(WORK_PATH, 'classifyFiles/DC_IndustryType')
ML_DATA_PATH = os.path.join(WORK_PATH, 'ml_data')
