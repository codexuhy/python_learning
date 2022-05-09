from ctypes import util
import re
import os

import calendar
import numpy as np
from datetime import datetime

from smpy import utils as  smpy_utils
import matplotlib.pyplot as plt


def filter_data(input_path):
    """将 文本中所需内容过滤写入新文本
    :param input_path: text_path
    :return:  filter_text_path
    """
    filter_lines = []
    filter_name = 'filter_upload_logs.txt'
    with open(input_path,"r") as f:
        lines = f.readlines()
        for line in lines:
            str1 = 'Start upload path'
            str2 = 'Upload path failed'
            str3 = r'Upload \d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2} success'
            match_start = re.compile(str1).search(line)
            match_failed = re.compile(str2).search(line)
            match_success = re.compile(str3).search(line)
            
            if match_start or match_failed or match_success:
                # print(line)
                filter_lines.append(f'{line}')
                
                with open(filter_name,mode='w') as fw:
                    fw.writelines(filter_lines)
    return  os.path.abspath(filter_name)


def utc_datetime_to_timestamp(timestr):
    """将 utc 时间 (datetime 格式) 转为 utc 时间戳
    :param utc_datetime: {datetime}2016-02-25 20:21:04.242000
    :return: 13位 的毫秒时间戳 1456431664242
    """
    local_datetime = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
    utc_timestamp = np.long(
        calendar.timegm(
            local_datetime.timetuple()) *
        1000.0 +
        local_datetime.microsecond /
        1000.0)

    return utc_timestamp

def extract_data(input_path):
    """
    返回提取的数据列表
    [
        {
            "start_upload_time": "2022-05-09 11:30:42.287",
            "end_time": "2022-05-09 11:30:42.328",
            "file_name": "2022-04-28-06-36-50",
            "status": "failed",
            "failed": "0.041s"
        },
        ...,
        ...

    ]
    """
    status_record_list = []
    with open(input_path,mode='r') as f:
        lines = f.readlines()
        # .是为了表示除了换行符的任一字符。*表示出现0次或无限次  ：加了？是最小匹配，不加是贪婪匹配
        p1 = re.compile(r'[[](.*?)[]]', re.S) #最小匹配 
        
        for i in range(len(lines)):
            line = lines[i]
            if  'Start' in lines[i]:
                start_time = re.findall(p1, line)[0]
                start_timestamp = utc_datetime_to_timestamp((re.findall(p1, line)[0]))
                file_name = re.compile(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}').search(line).group()
                if line !=lines[-1]:
                    if file_name not in lines[i+1]:
                        continue
                    if 'failed' in lines[i+1]:
                        failed_time = re.findall(p1, lines[i+1])[0]
                        failed_timestamp = utc_datetime_to_timestamp(failed_time)
                        status = "failed"
                        deltas_time = round((failed_timestamp - start_timestamp)*0.001/60,3)
                        status_record_list.append({
                            'start_upload_time':start_time,
                            'end_time':failed_time,
                            'file_name':file_name,
                            'status':status,
                            'deltas_time':deltas_time})
                    elif 'success' in lines[i+1]:
                        success_time = re.findall(p1, lines[i+1])[0]
                        success_timestamp = utc_datetime_to_timestamp(success_time)
                        status = "success"
                        deltas_time = round((success_timestamp - start_timestamp)*0.001/60)
                        status_record_list.append({
                            'start_upload_time':start_time,
                            'end_time':success_time,
                            'file_name':file_name,
                            'status':status,
                            'deltas_time':deltas_time})

    return status_record_list

if  __name__ == '__main__':
    input_path = "/data/hongyuan/work/docker_dir/dev_car_jira_tool/upload_logs.txt"
    filter_path = filter_data(input_path)
    status_record_list = extract_data(filter_path)
    status_record = {'name':'status_record_table','data':status_record_list}
    smpy_utils.write_json('status_record.json', status_record, indent=4)
    x_failed = []
    x_success =[]
    for data in status_record_list:
        if data['status'] == 'failed':
            x_failed.append(data['deltas_time'])
        else:
            x_success.append(data['deltas_time'])
    if len(x_failed):
        plt.hist(x_failed)
        plt.savefig("failed_hist.png", dpi=220)
    if len(x_success):
        plt.hist(x_success)
        plt.savefig("success_hist.png", dpi=220)





