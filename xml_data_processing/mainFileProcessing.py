import os
import time
import json

from xml_data_processing.downloadZipfiles import remove_old_files, \
    esma_registers_download, downloadZipfiles, \
    unzipdownload
from xml_data_processing.file_logger import file_logger
from xml_data_processing.xmlfileProcessingService import xmlfileprocessing, saveDictiornarytoCSV


def main():
    """"
   This is main function which calls all Dataline function and execute functions in sequence.
   """
    with open("application.json", encoding='utf-8') as json_config:
        config_data = json.load(json_config)
        logdir = config_data['logdir']
        logfile = config_data['logfile']
        url = config_data['url']
        zippath = config_data['zippath']
        xmlfile = config_data['xmlfile']
        dltinspath = config_data['dltinspath']
        csvDatafile = config_data['csvDatafile']
        dltinsDir = config_data['dltinsDir']

    logs = file_logger(logdir, logfile)
    logs.logger().info(f'Configuration Inforamtion  :  {config_data}')
    remove_old_files(zippath, dltinspath, xmlfile, logs)
    time.sleep(5)
    esma_registers_download(url, xmlfile, logs)
    downloadZipfiles(xmlfile, zippath, logs)
    unzipdownload(zippath, dltinspath, logs)
    time.sleep(2.4)

    headerFlag = True

    for filename in os.listdir(dltinsDir):
        if filename.endswith(".xml"):
            # print(filename)
            logs.logger().info(f'Data Processing File  :  {filename}')
            if os.path.isdir(dltinsDir):
                try:
                    dltinsfile = dltinsDir + filename
                    logs.logger().info(f'Data Processing File  :  {dltinsfile}')
                    dict_list = xmlfileprocessing(dltinsfile, logs)
                    saveDictiornarytoCSV(dict_list, csvDatafile, headerFlag, logs)
                    headerFlag = False

                except OSError as e:
                    logs.logger().exception(f'{e.strerror} ERROR OCCURED.', exc_info=True)


if __name__ == "__main__":
    main()
