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
        ??????issue??????
        """
        return self._jira_api.get_issue_status(issue_key)

    def get_issue_labels(self,issue_key):
        """
        ??????????????????
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
    ????????????
    https://jira.momenta.works/browse/MAPRELEASE-30629
    https://jira.momenta.works/browse/MHT-125250
    https://jira.momenta.works/browse/MST-308199

    ??????jira????????????????????????????????????jira?????????????????????
    ???????????????https://momenta.feishu.cn/wiki/wikcnCkgUKV9ckq7qmWj5e1PkQS#
    """

    jira_key = jira_keys.split('\n')[0]
    get_issues = jira.get_issues_info_by_jql(f"project = {project} AND key = {jira_key}") # ???ID???????????????jira  ????????????????????????
    issue = get_issues[0]

    issue_key = issue["key"] # MAPRELEASE-30629
    summary = issue["fields"]["summary"]  # 20220326 ?????????  ?????????Devcar?????????_?????????
    logger.info(f"loading issue key: {issue_key}")
    # logger.info(f"summary: {summary}")
    map_issue_test = issue["fields"][namemap["????????????-?????????"]]
    # ??????1????????????????????? ??????jira '????????????-?????????'
    
    first_label = ''
    second_label = ''
    is_data_probelm =''
    if map_issue_test:
        # ??????4???????????????
        first_label = map_issue_test['value'] # '???????????????'
        # ??????5???????????????
        second_label = map_issue_test['child']['value'] # '??????????????????'
    
    if first_label in ['????????????','-','None',]:
        is_data_probelm = '???'
    else:
        is_data_probelm = '???'
    
    # ??????2???????????????  ??????jira  Component/s
    issue_categroy = [i['name'] for i in issue["fields"][namemap["Component/s"]]]
    issue_categroy = ",".join(issue_categroy)

    # ??????3???????????????
    issue_level = ''
    if project in ['MAPRELEASE','MHT']:
        mpd_level = issue["fields"][namemap["??????MPD"]]['value']
        mpi_level = issue["fields"][namemap["??????MPI"]]['value']
        
        if mpd_level != 'None':
            issue_level = 'P0'
        if mpi_level != 'None':
            issue_level = 'P1'
        
    elif project == 'MST':
        record_reason = issue["fields"][namemap["MSD????????????"]]
        if record_reason != None:
            if record_reason['value'] == '??????':
                issue_level = 'P0'
            elif record_reason['value'] == '?????????':
                issue_level = 'P1'
    
    # ??????6???????????????
    fix_version =  '???' if not issue["fields"][namemap['????????????????????????']] else issue["fields"][namemap['????????????????????????']]

    # ??????7????????? ????????????????????????????????????????????????????????????
    jira_date = ''
    if issue["fields"][namemap["Start Date"]] != None:
        jira_date = issue["fields"][namemap["Start Date"]]
    elif issue["fields"][namemap["????????????"]] != None:
        jira_date = issue["fields"][namemap["????????????"]][:10].replace('-','/')
    else:
        jira_date = issue["fields"][namemap['Created']][:10].replace('-','/')
    
    labels = issue["fields"][namemap["Labels"]] # ??????Labels??????

    # ??????8???????????????
    data_version = ''
    # ??????9???????????????
    test_route = ''

    if project == 'MAPRELEASE':
        for l in labels:
            if l.startswith(u'????????????'):
                test_route = l.strip()[5:]
            if l.startswith(u'????????????'):
                data_version = l.split('???')[-1]
    elif project in ['MST','MHT']:
        for i in issue["fields"][namemap["SW version"]]:
            if 'hdmap_data:' in i:
                data_version = i.split(':')[-1]
                break

    if project == 'MAPRELEASE':
        test_route = test_route
    elif project == 'MST':    
        test_route = issue["fields"][namemap["MSD????????????"]]['value']
    elif project == 'MHT':    
        # test_route = issue["fields"][namemap["Highway????????????"]]
        test_route = issue['fields']['customfield_13410']['value']   
    
    # ??????10?????????
    test_area = ''
    if project == 'MAPRELEASE':
        test_area = issue["fields"][namemap["???????????????"]]
    elif project in ['MST','MHT']:
        test_area = issue["fields"][namemap["????????????"]]['value']

    # ??????11???????????????
    car_version = ''
    if project == 'MAPRELEASE':
        car_version = issue["fields"][namemap["????????????"]]
    elif project == 'MST':
        car_version = issue["fields"][namemap["MSD??????"]]['value']
    elif project == 'MHT':
        car_version = issue["fields"][namemap["highway??????"]]['value']

    # ??????12??? ??????
    jira_status = jira.get_issue_status(issue_key)

    # ??????13???????????????
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
        '??????????????????':is_data_probelm,
        '????????????':issue_categroy,
        '????????????':issue_level,
        '????????????':first_label,
        '????????????':second_label,
        '????????????':fix_version,
        '????????????':jira_date,
        '????????????': data_version,
        '????????????':test_route,
        '??????':test_area,
        '????????????':car_version,
        '??????':jira_status,
        '?????????':author_name,
        '????????????':update_date
    }
    
    # pprint(params)

    # for key,value in issue["fields"].items():
    #     print(key,'',value)
    
    return params

def handle_excel(input_path:str,output_path:str):
    
    # df = pd.read_excel(file)  # ??????excel
    # # pprint(df)
    # col_names = df.columns.tolist()  # ??????

    # jira_ids = df[col_names[0]] # ID???

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
            print(f'??????????????? {encode_info}???utf-8??????')
    except BaseException:
        print(input_path,'???????????????????????????')
    
    with open(input_path,encoding='utf-8') as file_obj:
        f_csv = csv.reader(file_obj)
        headers = next(f_csv)
        headers[0].split('\t')
        for row in f_csv:
            # print(row)
            jira_ids.append(row[0])

    # print(headers)
    # print(jira_ids)

    # ?????? cache
    cache = []
    for jira_id in tqdm(jira_ids):
        print(jira_id)
        project = jira_id.split('-')[0]
        cache.append(fill_field(project,jira_id))

    with open(output_path, 'w', encoding='utf-8', newline='') as file_obj:

        # 1.??????DicetWriter??????
        dictWriter = csv.DictWriter(file_obj, headers)
        # 2.?????????
        dictWriter.writeheader()
        # 3.????????????(?????????????????????)
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
