import glob
import sys
import requests
import xml.etree.ElementTree as ET
import os, zipfile


def remove_old_files(zippath, dltinspath, xmlfile, logs):
    """"
    This function deletes all old xml, zip files.
    """
    zipfiles = glob.glob(zippath + '*.*')
    dltinsfiles = glob.glob(dltinspath + '\\*.xml')
    logs.logger().info(f'Starting function : {remove_old_files.__name__} .')
    try:
        os.remove(xmlfile)
        logs.logger().info(f'{xmlfile} : old xml files  is removed successfully.')

    except OSError as e:
        logs.logger().error(f'{xmlfile}  have error {e.strerror}.')
    except:
        print(sys.exc_info()[0], "occurred.")
        logs.logger().error(f'{sys.exc_info()[0]} OCCURED.')

    for zf in zipfiles:
        try:
            os.remove(zf)
            logs.logger().info(f'{zf} : zipped file  is removed successfully.')
        except OSError as e:
            logs.logger().error(f'{zf}  have error {e.strerror}.')

    for df in dltinsfiles:
        try:
            os.remove(df)
            logs.logger().info(f'{df} : xmldata file  is removed successfully.')
        except OSError as e:
            logs.logger().error(f'{df}  have error {e.strerror}.')


def esma_registers_download(url, xmlfile, logs):
    """"
    This function download first xml file which has all zip files urls.
    It creates http urls to downlaod to zip files.
    """
    logs.logger().info(f'Starting function : {remove_old_files.__name__} .')
    try:
        response = requests.get(url)
        logs.logger().info(f'successfully connected : {url}')

    except:
        logs.logger().exception(f'failed to connect url : {url} ', exc_info=True)

    try:
        with open(xmlfile, 'wb') as file:
            file.write(response.content)
            logs.logger().info(f'{xmlfile} is downloaded successfully.')
    except:
        logs.logger().exception(f'{xmlfile} is failed  to download.', exc_info=True)


def downloadZipfiles(xmlfile, zippath, logs):
    """"
    This function donwload zip files.
    """
    logs.logger().info(f'Starting function : {remove_old_files.__name__} .')
    try:
        xmldoc = ET.parse(xmlfile)
        results = xmldoc.find('result')
        logs.logger().info(f'{xmlfile} is parsed successfully and STRING "result" found ')
    except:
        logs.logger().exception(f'{xmlfile} is failed to parse. {xmlfile} is not valid',
                                exc_info=True)

    for node in results.getiterator():
        for key, value in dict(node.attrib).items():
            if value == 'download_link':
                dltins_url = node.text
                urllist = dltins_url.split('/')

                logs.logger().info(f'url : {urllist}')
                for str in urllist:
                    if str.startswith('DLTINS'):
                        file_name = str

                logs.logger().info(f'filename : {file_name}')
                file_path = zippath + file_name
                logs.logger().info(f'file_path : {file_path}')

                try:
                    response = requests.get(dltins_url)
                    logs.logger().info(f'successfully connected : {dltins_url}')
                except:
                    logs.logger().exception(f'failed to connect url : {dltins_url} ', exc_info=True)
                try:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                        logs.logger().info(f'{file_path} is downloaded successfully.')
                except:
                    logs.logger().exception(f'{file_path} is failed  to download.', exc_info=True)


def unzipdownload(zippath, dltinspath, logs):
    """"
    It extract zipped files which creates data xml files.
    """
    logs.logger().info(f'Starting function : {remove_old_files.__name__} .')
    for filename in os.listdir(zippath):
        if filename.endswith(".zip"):

            if os.path.isdir(dltinspath):
                try:
                    zipped = zipfile.ZipFile(zippath + filename)
                    zipped.extractall(path=dltinspath)
                    logs.logger().info(f'{zipped} file is extracted successfully.')
                except zipfile.BadZipfile as e:
                    logs.logger().exception(f'{filename} is BAD ZIPPED.', exc_info=True)
                    try:
                        os.remove(filename)
                        logs.logger().info(f'{filename} file is removed successfully.')
                    except OSError as e:
                        logs.logger().exception(f'{e} is OS Error.', exc_info=True)
