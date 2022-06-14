#!/usr/bin/env python
# -*- coding: utf-8 -*-
from atlassian import Jira
import sys
from loguru import logger
from tqdm import tqdm
# import pandas as pd
import argparse

__all__ = ['JiraHelper']
user_name = ''
user_password = ''
class JiraHelper:
    jira_limit_return_number = 50 

    def __init__(self):
        self._jira_api = Jira(url="https://jira.momenta.works", username=user_name,
                              password=user_password)

    def get_issues_info_by_jql(self, jql):
        """
        :param jql:
        """
        return_issues = []
        if not jql:
            return return_issues
        start = 0
        while True:
            issues = self._jira_api.jql(jql=jql, start=start)['issues']
            if not len(issues):
                break

            start = start + self.jira_limit_return_number
            return_issues.extend(issues)
        return return_issues

    def create_jira_issue(self, issue_fields):
        """
        :param issue_fields: jira issue fields, like this format:
        {
            "project": { "key" : "MSDTES" },
            "summary": "issue title",
            "description": "this is description field",
            "issuetype": {"id": 10004, "name": "bug"},
            "assignee": {"name": "hanzhiyuan"},
            "priority": {"name": "Highest"},
            "customfield_11206": "diy field"
        }
        ...
        return json str response: like this:
        {'id': '68493', 'self': 'https://jira.momenta.works/rest/api/2/issue/68493', 'key': 'MSDTES-2735'}
        {'errorMessages': [], 'errors': {'issuetype': 'issue type is required'}}
        """
        return self._jira_api.create_issue(fields=issue_fields)

    def update_issue(self, issue_key, fields):
        """
        :param issue_key: issue key
        {
            "project": { "key" : "MSDTES" },
            "summary": "issue title",
            "description": "this is description field",
            "issuetype": {"id": 10004, "name": "bug"},
            "assignee": {"name": "hanzhiyuan"},
            "priority": {"name": "Highest"},
            "customfield_11206": "diy field"
        }
        ...
        return json str response: like this:
        {'id': '68493', 'self': 'https://jira.momenta.works/rest/api/2/issue/68493', 'key': 'MSDTES-2735'}
        {'errorMessages': [], 'errors': {'issuetype': 'issue type is required'}}
        """
        return self._jira_api.issue_update(issue_key=issue_key, fields=fields)

    def issue_add_comments(self, issue_key, comments):
        """
        add comments
        :param issue_key:
        :param comments:
         return json str response: like this:
        {'id': '68493', 'self': 'https://jira.momenta.works/rest/api/2/issue/68493', 'key': 'MSDTES-2735'}
        {'errorMessages': [], 'errors': {'issuetype': 'issue type is required'}}
        """
        return self._jira_api.issue_add_comment(issue_key, comments)

    def add_attachment(self, issue_key, file_name):
        """
        :param issue_key:
        :param file_name:
         return json str response: like this:
        {'id': '68493', 'self': 'https://jira.momenta.works/rest/api/2/issue/68493', 'key': 'MSDTES-2735'}
        {'errorMessages': [], 'errors': {'issuetype': 'issue type is required'}}
        """
        return self._jira_api.add_attachment(issue_key, filename=file_name)

    def get_issue_status(self,issue_key):
        """
        查看issue状态
        """
        return self._jira_api.get_issue_status(issue_key)

    def get_issue_labels(self,issue_key):
        """
        查看问题标签
        """
        return self._jira_api.get_issue_labels(issue_key)

    def get_comments(self,issue_key):
        url = self._jira_api.resource_url(f"issue/{issue_key}/comment")
        # url = f'/rest/api/2/issue/{issue_key}/comment'
        return self._jira_api.get(url)

def fill_field(project,jira_keys):
    jira = JiraHelper()
    allfields = jira._jira_api.get_all_fields()
    namemap = {field['name']:field['id'] for field in allfields}
    """
    三种链接
    https://jira.momenta.works/browse/MAPRELEASE-30629
    https://jira.momenta.works/browse/MHT-125250
    https://jira.momenta.works/browse/MST-308199

    根据jira的链接获取需求文档对应的jira字段，写入表中
    需求参考：https://momenta.feishu.cn/wiki/wikcnCkgUKV9ckq7qmWj5e1PkQS#
    """

    jira_key = jira_keys.split('\n')[0]
    get_issues = jira.get_issues_info_by_jql(f"project = {project} AND key = {jira_key}") # 若ID列存在多个jira  取第一个进行读取
    issue = get_issues[0]

    issue_key = issue["key"] # MAPRELEASE-30629
    summary = issue["fields"]["summary"]  # 20220326 掉自动  接管（Devcar自闭环_苏州）
    logger.info(f"loading issue key: {issue_key}")
    # logger.info(f"summary: {summary}")
    map_issue_test = issue["fields"][namemap["地图问题-测试："]]
    # 字段1：是否数据问题 对应jira '地图问题-测试：'
    
    first_label = ''
    second_label = ''
    is_data_probelm =''
    if map_issue_test:
        # 字段4：一级标签
        first_label = map_issue_test['value'] # '精度一致性'
        # 字段5：二级标签
        second_label = map_issue_test['child']['value'] # '横向精度偏差'
    
    if first_label in ['道路变化','-','None',]:
        is_data_probelm = '否'
    else:
        is_data_probelm = '是'
    
    # 字段2：问题分类  对应jira  Component/s
    issue_categroy = [i['name'] for i in issue["fields"][namemap["Component/s"]]]
    issue_categroy = ",".join(issue_categroy)

    # 字段3：问题等级
    issue_level = ''
    if project in ['MAPRELEASE','MHT']:
        mpd_level = issue["fields"][namemap["项目MPD"]]['value']
        mpi_level = issue["fields"][namemap["项目MPI"]]['value']
        
        if mpd_level != 'None':
            issue_level = 'P0'
        if mpi_level != 'None':
            issue_level = 'P1'
        
    elif project == 'MST':
        record_reason = issue["fields"][namemap["MSD录制原因"]]
        if record_reason != None:
            if record_reason['value'] == '接管':
                issue_level = 'P0'
            elif record_reason['value'] == '非接管':
                issue_level = 'P1'
    
    # 字段6：修复版本
    fix_version =  '无' if not issue["fields"][namemap['地图问题修复版本']] else issue["fields"][namemap['地图问题修复版本']]

    # 字段7：时间 问题发生时间（优先）没有则取问题创建时间
    jira_date = ''
    if issue["fields"][namemap["Start Date"]] != None:
        jira_date = issue["fields"][namemap["Start Date"]]
    elif issue["fields"][namemap["发生时间"]] != None:
        jira_date = issue["fields"][namemap["发生时间"]][:10].replace('-','/')
    else:
        jira_date = issue["fields"][namemap['Created']][:10].replace('-','/')
    
    labels = issue["fields"][namemap["Labels"]] # 对应Labels字段

    # 字段8：数据版本
    data_version = ''
    # 字段9：测试路线
    test_route = ''

    if project == 'MAPRELEASE':
        for l in labels:
            if l.startswith(u'测试路线'):
                test_route = l.strip()[5:]
            if l.startswith(u'数据版本'):
                data_version = l.split('：')[-1]
    elif project in ['MST','MHT']:
        for i in issue["fields"][namemap["SW version"]]:
            if 'hdmap_data:' in i:
                data_version = i.split(':')[-1]
                break

    if project == 'MAPRELEASE':
        test_route = test_route
    elif project == 'MST':    
        test_route = issue["fields"][namemap["MSD测试路线"]]['value']
    elif project == 'MHT':    
        # test_route = issue["fields"][namemap["Highway测试路线"]]
        test_route = issue['fields']['customfield_13410']['value']   
    
    # 字段10：城市
    test_area = ''
    if project == 'MAPRELEASE':
        test_area = issue["fields"][namemap["测试区域："]]
    elif project in ['MST','MHT']:
        test_area = issue["fields"][namemap["测试区域"]]['value']

    # 字段11：车辆版本
    car_version = ''
    if project == 'MAPRELEASE':
        car_version = issue["fields"][namemap["测试车辆"]]
    elif project == 'MST':
        car_version = issue["fields"][namemap["MSD车辆"]]['value']
    elif project == 'MHT':
        car_version = issue["fields"][namemap["highway车辆"]]['value']

    # 字段12： 状态
    jira_status = jira.get_issue_status(issue_key)

    # 字段13：确认日期
    commentators= ['gongluyue','huangzhuo','zhuo.huang','v-zhangji','v-wangbaihui','v-changlongyu','v-xiaojianxiong']
    comments = jira.get_comments(issue_key)
    author_name = ''
    update_date = ''
    if comments['comments']:
        date_list = [(c['author']['name'],c['created'][:10].replace('-','/'))  for c in comments['comments'] if c['author']['name'] in commentators]
        if len(date_list) >1:
            sorted(date_list)
            author_name = date_list[-1][0]
            update_date = date_list[-1][1]
        elif len(date_list) == 1:
            author_name = date_list[-1][0]
            update_date = date_list[-1][1]

    params = {
        'ID':jira_keys,
        # 'summary':summary,
        '是否数据问题':is_data_probelm,
        '问题分类':issue_categroy,
        '问题等级':issue_level,
        '一级标签':first_label,
        '二级标签':second_label,
        '修复版本':fix_version,
        '发生时间':jira_date,
        '数据版本': data_version,
        '测试路线':test_route,
        '城市':test_area,
        '车辆版本':car_version,
        '状态':jira_status,
        '记录人':author_name,
        '记录时间':update_date
    }
    
    # pprint(params)

    # for key,value in issue["fields"].items():
    #     print(key,'',value)
    
    return params

def handle_excel(input_path:str,output_path:str):
    
    # df = pd.read_excel(file)  # 读取excel
    # # pprint(df)
    # col_names = df.columns.tolist()  # 列名

    # jira_ids = df[col_names[0]] # ID列

    # for jira_id in tqdm(jira_ids):
    #     print(jira_id)
    #     project = jira_id.split('-')[0]
    #     cache = []
    #     cache.append(fill_field(project,jira_id))
    
    # print(df)
    pass

def handle_csv(input_path:str):

    import os
    import csv
    from get_encoding_info import get_encode_info,convert_encode2utf8

    filename = f'output_{os.path.basename(input_path)}'
    output_path = f'{os.path.dirname(input_path)}/{filename}'
    jira_ids = []
    headers = ''
    try:
        encode_info = get_encode_info(input_path)
        if encode_info != 'utf-8':
            convert_encode2utf8(input_path, encode_info, 'utf-8')
            print(f'成功由转换 {encode_info}为utf-8文件')
    except BaseException:
        print(input_path,'存在问题，请检查！')
    
    with open(input_path,encoding='utf-8') as file_obj:
        f_csv = csv.reader(file_obj)
        headers = next(f_csv)
        headers[0].split('\t')
        for row in f_csv:
            # print(row)
            jira_ids.append(row[0])

    # print(headers)
    # print(jira_ids)

    # 数据 cache
    cache = []
    for jira_id in tqdm(jira_ids):
        print(jira_id)
        project = jira_id.split('-')[0]
        cache.append(fill_field(project,jira_id))

    with open(output_path, 'w', encoding='utf-8', newline='') as file_obj:

        # 1.创建DicetWriter对象
        dictWriter = csv.DictWriter(file_obj, headers)
        # 2.写表头
        dictWriter.writeheader()
        # 3.写入数据(一次性写入多行)
        dictWriter.writerows(cache)
    print()
 
if __name__ == "__main__":
    print("-- Update csv --")
    prog = 'python3 fill_field_jira_tool.py'
    description = (
        'run fill_field_jira_tool to automatically populate the table data')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    
    parser.add_argument(
        '--username',
        type=str,
        default=None,
        help=f'input csv path',
    )

    parser.add_argument(
        '--password',
        type=str,
        default=None,
        help=f'input csv path',
    )

    parser.add_argument(
        '--path',
        type=str,
        default=None,
        help=f'input csv path',
    )

    args = parser.parse_args()
    user_name = args.username
    user_password = args.password
    input_path = args.path
    handle_csv(input_path)
