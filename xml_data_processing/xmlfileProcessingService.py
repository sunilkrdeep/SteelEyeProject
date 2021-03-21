import csv
import xml.etree.ElementTree as ET


def xmlfileprocessing(dltinsfile, logs):
    """"
    This function process unzipped  xml files to extract required  data and put in list.
    """
    try:
        dltinsTree = ET.parse(dltinsfile)
        dltinsRoot = dltinsTree.getroot()
        getDoc = ET.ElementTree(dltinsRoot)
        logs.logger().info(f'{dltinsfile} is parsed  successfully and started  processing .........')
    except:
        logs.logger().exception(f'{dltinsfile} is failed to parse. {dltinsfile} is not valid',
                                exc_info=True)
    dict_list = []
    logs.logger().info(f'{dict_list} : list is initialized')

    try:
        for TermntdRcrd in getDoc.iter():

            rec_dict = {}
            if str(TermntdRcrd.tag).split('}')[1] == 'TermntdRcrd':

                # logs.logger().info(f'TermntdRcrd : {TermntdRcrd}')

                for rec_attrib in TermntdRcrd:

                    if str(rec_attrib.tag).split('}')[1] == 'FinInstrmGnlAttrbts':

                        for FinInstrmGnlAttrbts in rec_attrib.iter():

                            dict_key = str(FinInstrmGnlAttrbts.tag).split('}')[1]
                            if dict_key != 'FinInstrmGnlAttrbts':

                                if dict_key == 'Id':
                                    rec_dict[dict_key] = FinInstrmGnlAttrbts.text
                                elif dict_key == 'FullNm':
                                    rec_dict[dict_key] = FinInstrmGnlAttrbts.text
                                elif dict_key == 'ClssfctnTp':
                                    rec_dict[dict_key] = FinInstrmGnlAttrbts.text
                                elif dict_key == 'CmmdtyDerivInd':
                                    rec_dict[dict_key] = FinInstrmGnlAttrbts.text
                                elif dict_key == 'NtnlCcy':
                                    rec_dict[dict_key] = FinInstrmGnlAttrbts.text

                    if str(rec_attrib.tag).split('}')[1] == 'Issr':
                        rec_dict['Issr'] = rec_attrib.text

                    dict_list.append(rec_dict)
        logs.logger().info(f'{dltinsfile} is processed successfully')
    except:
        logs.logger().exception(f'{dltinsfile} is not processed successfully.', exc_info=True)

    return dict_list


def saveDictiornarytoCSV(rec_dict, dataCSV, headerFlag, logs):
    """"
    This function save dict_list data in a csv file.
    """
    schema = ['Id', 'FullNm', 'ClssfctnTp', 'CmmdtyDerivInd', 'NtnlCcy', 'Issr']
    logs.logger().info(f'CSV file Schemalist : {schema}')
    try:
        with open(dataCSV, 'a+', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema)
            logs.logger().info(f'{csvfile} is opened ... ')
            if headerFlag:
                writer.writeheader()
                logs.logger().info(f'Header Record is written : {schema}')
            writer.writerows(rec_dict)
            logs.logger().info(f'Dictionary List written in file  : {csvfile}')
    except:
        logs.logger().exception(f'{csvfile} is not written successfully.', exc_info=True)
