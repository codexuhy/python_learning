from ctypes import util
from math import floor
import re
import os

import calendar
import numpy as np
from datetime import datetime

from smpy import utils as smpy_utils
import matplotlib.pyplot as plt


class LogAnalysis(object):
    def __init__(
            self,
            workdir=f'{os.path.dirname(__file__)}/workdir',
    ):
        self.workdir = workdir
        os.makedirs(self.workdir, exist_ok=True)

    def filter_log(self, input_path):
        """将 文本中所需内容过滤写入新文本
        :param input_path: text_path
        :return:  filter_text_path
        """
        output_log_path = f'{self.workdir}/filter_upload.log'
        output_dev_car_log_path = f'{self.workdir}/filter_dev_car_upload.log'
        filter_lines = []
        dev_car_filter_lines = []

        with open(input_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                str1 = 'Total file size'
                str2 = 'Start upload path'
                str3 = 'Upload path failed'
                str4 = r'Upload \d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2} success'

                match_size = re.compile(str1).search(line)
                match_start = re.compile(str2).search(line)
                match_failed = re.compile(str3).search(line)
                match_success = re.compile(str4).search(line)

                if match_size or match_start or match_failed or match_success:
                    # print(line)
                    filter_lines.append(f'{line}')

                    with open(output_log_path, mode='w') as fw:
                        fw.writelines(filter_lines)

                dev_car_str1 = 'Start upload to devcar_online.'
                dev_car_str2 = 'File size = '
                dev_car_str3 = 'Success upload to devcar_online'

                dev_car_match_start = re.compile(dev_car_str1).search(line)
                dev_car_match_size = re.compile(dev_car_str2).search(line)
                dev_car_match_success = re.compile(dev_car_str3).search(line)

                if dev_car_match_start or dev_car_match_size or dev_car_match_success:
                    dev_car_filter_lines.append(f'{line}')

                    with open(output_dev_car_log_path, mode='w') as fw:
                        fw.writelines(dev_car_filter_lines)

        return output_log_path,output_dev_car_log_path

    def utc_datetime_to_timestamp(self, timestr):
        """将 utc 时间 (datetime 格式) 转为 utc 时间戳
        :param utc_datetime: {datetime}2016-02-25 20:21:04.242000
        :return: 13位 的毫秒时间戳 1456431664242
        """
        local_datetime = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
        utc_timestamp = np.long(
            calendar.timegm(local_datetime.timetuple()) * 1000.0 +
            local_datetime.microsecond / 1000.0)
        return utc_timestamp

    def extract_field_to_json(self, input_path,dev_car_input_path):
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
        output_json_path = f'{self.workdir}/status_record.json'
        status_record_list = []
        with open(input_path, mode='r') as f:
            lines = f.readlines()
            # .是为了表示除了换行符的任一字符。*表示出现0次或无限次  ：加了？是最小匹配，不加是贪婪匹配
            p1 = re.compile(r'[[](.*?)[]]', re.S)  #最小匹配

            for i in range(len(lines)):
                line = lines[i]
                if 'Total file size' in line:
                    total_file_size = round(
                        int(re.findall(r'\d+', line)[-1]) / 1024 / 1024,
                        3)  # unit:MB
                    print()
                    if ('Start' in lines[i + 1]):
                        start_time = re.findall(p1, lines[i + 1])[0]
                        start_timestamp = self.utc_datetime_to_timestamp(
                            (re.findall(p1, lines[i + 1])[0]))
                        file_name = re.compile(
                            r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}').search(
                                lines[i + 1]).group()
                        if line != lines[-2]:
                            if file_name not in lines[
                                    i +
                                    2]:  # start中取出的filename应该在end_time中，不在则丢弃
                                continue
                            if 'failed' in lines[i + 2]:
                                failed_time = re.findall(p1, lines[i + 2])[0]
                                failed_timestamp = self.utc_datetime_to_timestamp(
                                    failed_time)
                                status = "failed"
                                deltas_time = round(
                                    (failed_timestamp - start_timestamp) *
                                    0.001 / 60, 3)
                                upload_speed = round(total_file_size * 1024 /
                                                     (deltas_time * 60), 3)  # unit: kb/s
                                status_record_list.append({
                                    'start_upload_time':
                                    start_time,
                                    'end_time':
                                    failed_time,
                                    'file_name':
                                    file_name,
                                    'status':
                                    status,
                                    'deltas_time':
                                    deltas_time,
                                    'total_file_size':
                                    total_file_size,
                                    'upload_speed':
                                    upload_speed
                                })
                            elif 'success' in lines[i + 2]:
                                success_time = re.findall(p1, lines[i + 2])[0]
                                success_timestamp = self.utc_datetime_to_timestamp(
                                    success_time)
                                status = "success"
                                deltas_time = round(
                                    (success_timestamp - start_timestamp) *
                                    0.001 / 60)  # unit:min
                                upload_speed = round(total_file_size * 1024 /
                                                     (deltas_time * 60), 3)  # unit: kb/s
                                status_record_list.append({
                                    'start_upload_time':
                                    start_time,
                                    'end_time':
                                    success_time,
                                    'file_name':
                                    file_name,
                                    'status':
                                    status,
                                    'deltas_time':
                                    deltas_time,
                                    'total_file_size':
                                    total_file_size,
                                    'upload_speed':
                                    upload_speed
                                })
        status_record = {
            'name': 'status_record_table',
            'data': status_record_list
        }
        smpy_utils.write_json(output_json_path, status_record, indent=4)

        output_dev_car_json_path = f'{self.workdir}/dev_car_status_record.json'
        dev_car_status_record_list = []
        with open(dev_car_input_path, mode='r') as f:
            lines = f.readlines()
            # .是为了表示除了换行符的任一字符。*表示出现0次或无限次  ：加了？是最小匹配，不加是贪婪匹配
            p1 = re.compile(r'[[](.*?)[]]', re.S)  #最小匹配

            for i in range(len(lines)):
                line = lines[i]

                if ('Start' in lines[i]):
                    start_time = re.findall(p1, lines[i])[0]
                    start_timestamp = self.utc_datetime_to_timestamp(
                        (re.findall(p1, lines[i])[0]))
                    file_name = lines[i].split(':')[-1].strip()
                    if line != lines[-2]:
                        total_file_size = round((int(re.findall(p1, lines[i+1])[4])/1024/1024),3)
                        if total_file_size < 1:
                            continue
                        if file_name not in lines[
                                i +
                                2]:  # start中取出的filename应该在end_time中，不在则丢弃
                            continue
                        if 'failed' in lines[i + 2]:
                            failed_time = re.findall(p1, lines[i + 2])[0]
                            failed_timestamp = self.utc_datetime_to_timestamp(
                                failed_time)
                            status = "failed"
                            deltas_time = round(
                                (failed_timestamp - start_timestamp) *
                                0.001, 3)
                            upload_speed = round(total_file_size * 1024 /
                                                    deltas_time, 3)  # unit: kb/s
                            dev_car_status_record_list.append({
                                'start_upload_time':
                                start_time,
                                'end_time':
                                failed_time,
                                'file_name':
                                file_name,
                                'status':
                                status,
                                'deltas_time':
                                deltas_time,
                                'total_file_size':
                                total_file_size,
                                'upload_speed':
                                upload_speed
                            })
                        elif 'Success' in lines[i + 2]:
                            success_time = re.findall(p1, lines[i + 2])[0]
                            success_timestamp = self.utc_datetime_to_timestamp(
                                success_time)
                            status = "success"
                            deltas_time = round(
                                (success_timestamp - start_timestamp) *
                                0.001)  # unit:min
                            upload_speed = round(total_file_size * 1024 /
                                                    deltas_time, 3)  # unit: kb/s
                            dev_car_status_record_list.append({
                                'start_upload_time':
                                start_time,
                                'end_time':
                                success_time,
                                'file_name':
                                file_name,
                                'status':
                                status,
                                'deltas_time':
                                deltas_time,
                                'total_file_size':
                                total_file_size,
                                'upload_speed':
                                upload_speed
                            })
        dev_car_status_record = {
            'name': 'dev_car_status_record_table',
            'data': dev_car_status_record_list
        }
        smpy_utils.write_json(output_dev_car_json_path, dev_car_status_record, indent=4)

        return status_record_list,dev_car_status_record_list
    
    
    def draw_hist(self,x_axis,title,output_path):
        plt.hist(x_axis,bins=40)
        plt.title(title)
        plt.savefig(output_path, dpi=220)
        plt.close()

    def draw_bar(self,x,y,path="bar.png"):
        """
        y：条形图数据
        x:x轴坐标
        path：图片保存路径
        """
        # 设置图像大小
        # 创建一个分辨率为1600*640的空白画布
        plt.figure(figsize=(20,8),dpi=80)
        # 创建x轴显示的参数（此功能在与在图像中x轴仅显示能被10整除的刻度，避免刻度过多分不清楚）
        # x_tick = list(map(lambda num: "" if num % 10 != 0 else num, x))
        # 设置x,y轴的说明
        plt.xlabel('total size(Mb)', size=15)
        plt.ylabel('upload speed(kb/s)', size=15)
        # 打开网格线
        plt.grid(alpha=0.3)
        # 绘制条形图
        plt.barh(range(len(x)), y, height=0.3, color='orange') # 区别于竖的条形图 不能使用width
        # # 显示y轴刻度
        plt.yticks(range(len(x)), x,fontsize=10)
        plt.title('upload_speed/total_size')

        plt.savefig(path, dpi=80)
        plt.close()
        
        # 柱状图纵向显示
        # plt.bar(range(len(y)), y,width=0.3)
        # plt.title('total_size/upload_speed')
        # plt.xlabel('upload_speed(kb/s)', size=300)
        # plt.ylabel('total size(Mb)', size=300)
        # plt.grid(alpha=0.3)
        # plt.xticks(range(len(y)), x,fontsize=5)
        # plt.savefig("大小与上传速度柱状图.png", dpi=700)
        # plt.show()

    def consume_task(self, input_path):
        filter_path,filter_dev_car_path = self.filter_log(input_path)
        status_record_list,dev_car_status_record_list = self.extract_field_to_json(filter_path,filter_dev_car_path)

        x_failed = []
        x_success = []
        x_total_file_size = []
        x_upload_speed = []
        output_failed_path = f'{self.workdir}/failed_hist.png'
        output_success_path = f'{self.workdir}/success_hist.png'
        output_size_path = f'{self.workdir}/total_file_size_hist.png'
        output_speed_path = f'{self.workdir}/upload_speed_hist.png'

        for data in status_record_list:
            if data['status'] == 'failed':
                x_failed.append(data['deltas_time'])
            else:
                x_success.append(data['deltas_time'])
            x_total_file_size.append(data['total_file_size'])
            x_upload_speed.append(data['upload_speed'])

        if len(x_failed):
            self.draw_hist(x_failed,"failed success",output_failed_path)
        if len(x_success):
            self.draw_hist(x_success,"upload success",output_success_path)
        if len(x_total_file_size):
            self.draw_hist(x_total_file_size,"total file size",output_size_path)
        if len(x_upload_speed):
            self.draw_hist(x_upload_speed,"upload speed",output_speed_path)
        
        indices = []
        for  data in dev_car_status_record_list:
            idx = floor(data['upload_speed'] / 500)
            indices.append(idx)
        indices =np.array(indices)
        max_idx = np.max(indices)
        x = []
        y = []
        
        for i in range(max_idx):
            total_size = 0
            indices_0 = np.where(indices == i)[0]
            for index in indices_0:
                total_size += dev_car_status_record_list[index]['total_file_size']
            x.append(i*500)
            y.append(total_size)

        x_labels = []

        for item in range(0, max_idx*500, 500):
            x = item + 500
            # if x == 300:
            #     x_labels.append("{}~{}".format(0, 300))
            if x % 500 == 0:
                x_labels.append("{}~{}".format(x, x+500))
            else:
                x_labels.append(None)

        output_dev_car_speed_path = f'{self.workdir}/dev_car_upload_speed_bar.png'
        self.draw_bar(x_labels,y,output_dev_car_speed_path)
        print() 

if __name__ == '__main__':

    log_analysis = LogAnalysis(
        workdir=f'{os.path.dirname(__file__)}/workdir', )
    log_analysis.consume_task(
        input_path=f'/data/hongyuan/work/log-analysis/test/upload.log')
