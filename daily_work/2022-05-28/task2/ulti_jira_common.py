#!/usr/bin/env python
# -*- coding: utf-8 -*-
from atlassian import Jira
import pprint
import sys
import pymongo
import re
import datetime
import time
from pymdi import pymdi
from loguru import logger
from tqdm import tqdm
__all__ = ['JiraHelper']

class JiraHelper:
    jira_limit_return_number = 50 

    def __init__(self):
        self._jira_api = Jira(url="https://jira.momenta.works", username="xxxx",
                              password="xxxx")

    def mviz_link_finder(self, name):
        """
        highway和urban场景拉取mviz_link视频链接和description链接
        """
        client = pymdi.Client(token="ad86e83f-62d0-47e3-979b-164e906997a1")
        result = client.query(
            {
                "bool": {
                    "must": [
                        {"tag": "mviz_converted"},
                        {"tag": "from_dpp"},
                        {"type": "bag"},
                        {"category": "msd"},
                        {"wildcard":
                            {"name": name}  # *_20211114-111124*
                        }
                    ]
                }
            }, limit=50
        )
        result_data = result["data"]
        mviz_link = "None"
        # mdi_link = "None"
        case_link = "None"
        try:
            # assert len(result_data)== 1 
            metas = client.get_meta([x["md5"] for x in result_data])
            for meta in metas:
                if "mviz" not in meta:
                    continue
                mviz_meta = meta["mviz"]
                if "key" not in mviz_meta:
                    continue
                mviz_key = mviz_meta["key"]
                mviz_link = "https://mviz.momenta.works/player/v3/?user=MSD&format=multi_pbe_gz&path=%2F%2Fobs.cn-east-3.myhuaweicloud.com%2Fmviz-msd-data-obs%2F{}".format(
                    mviz_key.replace("/", "%2F"))



                # mdi_link = ("mdi fetch -o " + meta["name"] + " " + meta["md5"])

                case_key = meta["dxp"]["key"]
                case_link = 'aws --profile msquare-ro --endpoint=http://obs.cn-east-3.myhuaweicloud.com s3 cp s3://msquare-data-s3-obs/{} .'.format(
                                    case_key)
                logger.info(f'mviz_link：{mviz_link}')
                # logger.info(f'mdi_link：{mdi_link}')
                logger.info(f'case_link：{case_link}')
        except:
            logger.error("当前jira号未获取到视频下载和Description链接,请检查数据是否存在")
        return mviz_link, case_link

    def mdi_link_finder(self, name,issue_car_plate):
        """
        highway和urban场景拉取mdi链接
        
        """
        client = pymdi.Client(token="ad86e83f-62d0-47e3-979b-164e906997a1")
        result = client.query(
            {
                "bool": {
                    "must": [
                        {"tag": "rawdata"},
                        {"tag": "from_dip"},
                        {"type": "bag"},
                        {"category": "msd"},
                        {"wildcard":
                            {"name": name}  # *_20211114-111124*
                        }
                    ]
                }
            }, limit=50
        )
        result_data = result["data"]   # [{'md5':'749a18a335856d5f0cb679f12be5af88'}]
        mdi_link = "None"
        try:
            # assert 1 == len(result_data)
            metas = client.get_meta([x["md5"] for x in result_data])
            search_str_list = ["event_manual_recording", "event_dbw_disabled", "event_rviz"]
            for meta in metas:
                if all(s not in meta["dxp"]["key"] for s in search_str_list) or issue_car_plate not in meta["dxp"]["key"]:
                    metas.remove(meta)
            if metas[0] is None:
                return
            meta = metas[0]
            mdi_link = ("mdi fetch -o " + meta["name"] + " " + meta["md5"])
            logger.info(f'mdi_link：{mdi_link}')
            # for meta in metas:
            #     mdi_link = ("mdi fetch -o " + meta["name"] + " " + meta["md5"])
            #     logger.info(f'mdi_link：{mdi_link}')
            #     break
        except:
            logger.error("当前jira号未获取到MDI下载链接,请检查数据是否存在")
        return mdi_link

    def pnp_mviz_link_finder(self, name):
        """
        PNP场景拉取mviz链接
        """
        client = pymdi.Client(token="ad86e83f-62d0-47e3-979b-164e906997a1")
        result = client.query(
            {
                "bool": {
                    "must": [
                        {"tag": "mviz_converted"},
                        {"tag": "from_dpp"},
                        {"type": "bag"},
                        {"category": "pnp"}, 
                        {"wildcard":
                            {"name": name}  # *_20220424-151901*
                        }
                    ]
                }
            }, limit=50
        )
        result_data = result["data"]
        mviz_link = "None"
        # mdi_link = "None"
        # case_link = "None"
        try:
            # assert len(result_data)== 1 
            metas = client.get_meta([x["md5"] for x in result_data])
            for meta in metas:
                if "mviz" not in meta:
                    continue
                mviz_meta = meta["mviz"]
                if "key" not in mviz_meta:
                    continue
                mviz_key = mviz_meta["key"]
                mviz_link = "https://mviz.momenta.works/player/v3/?user=MSD&format=multi_pbe_gz&path=%2F%2Fmviz-convert-prod-data-obs.obs.cn-east-3.myhuaweicloud.com%2F{}".format(
                    mviz_key.replace("/", "%2F"))

                # mdi_link = ("mdi fetch -o " + meta["name"] + " " + meta["md5"])

                # case_key = meta["dxp"]["key"]
                # case_link = 'aws --profile msquare-ro --endpoint=http://obs.cn-east-3.myhuaweicloud.com s3 cp s3://msquare-data-s3-obs/{} .'.format(
                #                     case_key)
                logger.info(f'mviz_link：{mviz_link}')
        except:
            logger.error("当前PNP场景的jira号未获取到视链接,请检查数据是否存在")
        return mviz_link

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

def db_call(sence):
    if 'urban' == sence:
        client = pymongo.MongoClient('mongodb://m4u_ro:tp1FOlQjZRjIvQ4dN93V@172.31.0.108:27017/m4u_production')
        db = client['m4u_production']        
        collection = db['proc_msquare']
    else:
        client = pymongo.MongoClient('mongodb://readonly:a6E3xpLmUunWwGJn@dds-2zeae3c6fe0584942.mongodb.rds.aliyuncs.com:3717/mpilot_highway_production?replicaSet=mgset-25763777')
        db = client['mpilot_highway_production']
        collection = db['proc_highway']
    return collection

def is_valid_key(key):
	if 'sensor' in key:
		return False
	else:
		if 'dbw_disabled' in key or 'manual_recording' in key:
			return True
		else:
			return False

def bag_link_appender():
    jira = JiraHelper()
    allfields = jira._jira_api.get_all_fields()
    namemap = {field['name']:field['id'] for field in allfields}
    # get_issues = jira.get_issues_info_by_jql("project = MAPRELEASE AND description ~ None AND labels = 测试内容：Devcar自闭环")
    get_issues = jira.get_issues_info_by_jql("project = MAPRELEASE AND description ~ None AND labels = 测试内容：Devcar自闭环 AND created >= -15d")
    # get_issues = jira.get_issues_info_by_jql("project = MAPRELEASE AND key = MAPRELEASE-31005")
    # get_issues = jira.get_issues_info_by_jql("project = MAPRELEASE AND key = MAPRELEASE-20686") # pnp 
    
    for issue in tqdm(get_issues):
        issue_key = issue["key"]  # MAPRELEASE-12894
        summary = issue["fields"]["summary"]  # 20220326 掉自动  接管（Devcar自闭环_苏州）
        logger.info(f"loading issue key: {issue_key},summary: {summary}")
        date = summary.strip()[:8]  # 20220326
        logger.info(f"date: {date}")
        record_time = ""
        car = ""
        sence = ""
        labels = issue["fields"]["labels"] # 对应Labels字段
        for l in labels:
            if l.startswith(u"发生时间"):
                record_time = l.strip()[-6:]
            if l.startswith(u'测试车辆'):
                car = l.strip()[-3:]
            if l.startswith(u'场景类型'):
                sence = l.strip()[5:]

        sence = issue["fields"][namemap['场景类型：']]

        if "" == car:
            car = issue["fields"][namemap['测试车辆']].strip()[-3:]
        issue_car_plate = car

        if not ('None' == issue["fields"]['description']
                or 'None' == issue["fields"][namemap['视频链接']]
                or 'None' == issue["fields"][namemap['MDI下载链接']]):
            logger.warning('issue: {} had been update.'.format(issue_key))
            continue
        if sence not in ['highway','urban','PNP']:
            continue
        else:
            name = "*_" + date + "-" + record_time + "*"
            # 在https://cla.momenta.works/cdi/categories/msd上输入name查看bag信息是否存在
            logger.info(f'name:{name}')
            if sence == 'highway' or sence == 'urban':
                mviz_link,case_link = jira.mviz_link_finder(name)
                mdi_link = jira.mdi_link_finder(name,issue_car_plate)
                f_dict = {
                    "description": case_link,
                    namemap['视频链接']: mviz_link,
                    namemap['MDI下载链接']: mdi_link
                }
            elif sence == 'PNP':
                mviz_link = jira.pnp_mviz_link_finder(name)
                f_dict = {
                    namemap['视频链接']: mviz_link,
                }
            jira.update_issue(issue_key, f_dict)
            # https://blog.csdn.net/whatday/article/details/109257348
            # 避免频繁请求服务器导致断开连接
            time.sleep(1)
if __name__ == "__main__":
    print("-- Update Jira --")
    bag_link_appender()
