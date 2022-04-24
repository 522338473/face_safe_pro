"""
人脸搜索相关
"""
import logging
import json
import datetime
import requests

from django.conf import settings

from rest_framework.exceptions import ParseError

from utils.hasher import Hasher
from utils.job_queue import redis_cache
from utils.search_status import search_status

logger_info = logging.getLogger('server.default')
logger_error = logging.getLogger('server.error')


class FaceDiscern:
    """人脸搜索类"""

    def __init__(self):
        self.image_type = 'BASE64'
        self.margin = 0.5
        self.s_margin = 60
        self.TIMEOUT = 3
        self.face_focus_add_url = ''.join([settings.SEARCH_SERVER_HOST, '/focus_add'])  # 关注人员新增
        self.face_focus_del_url = ''.join([settings.SEARCH_SERVER_HOST, '/focus_del'])  # 关注人员删除
        self.face_focus_search_url = ''.join([settings.SEARCH_SERVER_HOST, '/focus_trace'])  # 关注人员搜索
        self.face_archive_add_url = ''.join([settings.SEARCH_SERVER_HOST, '/archive_add'])  # 人员档案新增
        self.face_archive_del_url = ''.join([settings.SEARCH_SERVER_HOST, '/archive_del'])  # 人员档案删除
        self.face_search_url = ''.join([settings.SEARCH_SERVER_HOST, '/archive_search'])  # 人员档案搜索
        self.face_warning_add_url = ''.join([settings.SEARCH_SERVER_HOST, '/warning_add'])  # 重点人员新增
        self.face_warning_del_url = ''.join([settings.SEARCH_SERVER_HOST, '/warning_del'])  # 重点人员删除
        self.face_history_search_url = ''.join([settings.SEARCH_SERVER_HOST, '/search'])  # 以图搜图

    @staticmethod
    def search_result(result_list):
        """过滤在某个时间段的数据"""
        check_id_list = []
        for item in result_list:
            for i in item:
                check_id_list.append([Hasher.to_object_pk(i.pop(0)), i.pop(-1)])
        return check_id_list

    @staticmethod
    def date_pkl_gen(start_date, end_date):
        start_date = datetime.date(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:8]))
        end_date = datetime.date(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:8]))

        d = end_date
        delta = datetime.timedelta(days=1)
        date_pkl = []
        i = 0
        while d >= start_date:
            st_date = d.strftime("%Y%m%d")
            date_pkl.append(st_date)
            d -= delta
            if i == 6:
                break
            i += 1
        return date_pkl

    def face_detect(self, image):
        """返回人脸token等基本属性"""
        payload = {
            "image": image,
            "image_type": "BASE64",
            "face_field": "face_shape,quality,face_type,race",
            "get_feature": "YES",
            "max_face_num": 1
        }
        data = requests.post(url=self.face_detect_url, json=payload, timeout=self.TIMEOUT).json()
        face_list = data['result']['face_list'][0]
        race = face_list['race']['type']
        face_token = face_list['face_token']
        return face_token, race

    def search_history_data(self, face_token, bd_margin, start_date, end_date):
        """搜索历史数据"""
        payload = {
            "image": face_token,
            "image_type": "FACE_TOKEN",
            "group_id_list": None,
            "quality_control": "NONE",
            "liveness_control": "NONE",
            "max_user_num": 50
        }
        term = self.date_pkl_gen(start_date=start_date, end_date=end_date)
        resp = []
        try:
            search_status.status = False
            for g in term:
                payload['group_id_list'] = g
                result = requests.post(url=self.face_search_url, json=payload, timeout=self.TIMEOUT).json()
                race = result.get('race', 'black')
                if result['error_code'] == 0 and result['result'] is not None:
                    face_list = result['result']['user_list']
                    for user_list in face_list:
                        if user_list['score'] > bd_margin:
                            resp.append([user_list['user_id'], round(user_list['score'], 2)])
            search_status.status = True
        except Exception as e:
            logger_error.error('{}face search error: {}'.format(datetime.datetime.now(), e))
        finally:
            search_status.status = True
        return [resp], len(resp), race

    def search_record(self, image, identification=None, start_date=None, end_date=None, margin=None, s_margin=None,
                      search_type=None, timeout=3600):
        """
        :param timeout: 缓存时间
        :param search_type:
        :以图识图搜索
        :param identification: 唯一id
        :param image:
        :param margin
        :param s_margin
        :param start_date:开始时间
        :param end_date:结束时间
        :return:返回搜索结果[(x, y), (x, y), (x, y)]
        """
        data = {
            "image": image,
            "image_type": self.image_type,
            "margin": margin,
            "smargin": s_margin,
            "startdate": start_date,
            "enddate": end_date,
            "search_type": search_type
        }
        try:
            search_status.status = False
            result = requests.post(url=self.face_history_search_url, json=data, timeout=self.TIMEOUT).json()
            if result.get('error') == 0:
                check_id_list = self.search_result(result.get('result', []))
                if result.get('race') == 'black':
                    # 如果返回有黑人，则进行以下处理
                    check_id_list = list(filter(lambda x: x[1] > int(settings.BLACK_THRESHOLD), check_id_list))
                check_id_list.sort(key=lambda x: x[0])  # 对查询到的结果进行排序
                redis_cache.redis_set_cache(identification, check_id_list, timeout)
                # status: True 表示搜索结束
                search_status.status = True
                return {'results': check_id_list, 'code': 0}
            search_status.status = True
            return {'results': [], 'code': 1}
        except Exception as e:
            logger_error.info("face search error: ", e)
            return {'results': [], 'code': -1}
        finally:
            search_status.status = True

    def face_add(self, image, user_id):
        """人员档案新增"""
        data = {
            "image": image,
            "image_type": self.image_type,
            "name": user_id
        }
        result = requests.post(url=self.face_archive_add_url, json=data, timeout=self.TIMEOUT).json()
        logger_info.info(result)
        return result

    def face_search(self, image):
        """人员档案搜索"""
        data = {
            "image": image,
            "image_type": self.image_type
        }
        result = requests.post(url=self.face_search_url, json=data, timeout=self.TIMEOUT).json()
        logger_info.info(result)
        if result.get('error') == 0:
            face_list = [item for item in result.get("result") if item[1] > 70]
            # [[id , 50], []]
            check_id_list = []
            for item in face_list:
                check_id_list.append([Hasher.to_object_pk(item[0]), item[1]])
            check_id_list.sort(key=lambda x: x[0])
            return check_id_list
        else:
            raise ParseError('没有找到相似的人脸!')

    def face_del(self, user_id):
        """人员档案删除"""
        data = {
            'name': user_id
        }
        result = requests.post(url=self.face_archive_del_url, json=data, timeout=self.TIMEOUT).json()
        logger_info.info(result)
        return result

    def get_face_color(self, image):
        """
        返回人脸颜色属性：yellow，black，white
        {
             "error_code": 0,
             "error_msg": "SUCCESS",
             "log_id": 1234567890123,
             "timestamp": 1533094400,
             "cached": 0,
             "result": {
                 "face_num": 1,
                 "face_list": [
                     {
                         "face_token": "35235asfas21421fakghktyfdgh68bio",
                         "race": {
                             "type": "yellow",
                             "probability": 0.99999976158142
                         },
                     }
                 ]
             }
        }
        """
        face_token, race_info = self.face_detect(image=image)
        data = {
            'image_type': 'FACE_TOKEN',
            'image': face_token
        }
        result = requests.post(url=self.face_detect_url, data=data, timeout=self.TIMEOUT)
        result = json.loads(result.text)
        if result.get('error_msg') == 'SUCCESS' and result.get('error_code') == 0:
            race = result.get('result')[0]
            if race.get('race'):
                return race['race']['type']

    def face_warning_add(self, image, user_id, margin=60):
        """重点人员新增"""
        data = {
            "image": image,
            "image_type": self.image_type,
            "name": user_id,
            "margin": margin,
        }
        result = requests.post(url=self.face_warning_add_url, json=data, timeout=self.TIMEOUT).json()
        logger_info.info(result)
        return result

    def face_warning_detect(self, user_id):
        """重点人员删除"""
        data = {
            "name": user_id
        }
        result = requests.post(url=self.face_warning_del_url, json=data, timeout=self.TIMEOUT).json()
        logger_info.info(result)
        return result

    def face_focus_add(self, image, user_id, margin=60):
        """关注人员新增"""
        data = {
            "image": image,
            "image_type": self.image_type,
            "name": user_id,
            "margin": margin,
        }
        result = requests.post(url=self.face_focus_add_url, json=data, timeout=self.TIMEOUT).json()
        logger_info.info(result)
        return result

    def face_focus_del(self, user_id):
        """关注人员删除"""
        data = {
            "name": user_id
        }
        result = requests.post(url=self.face_focus_del_url, json=data, timeout=self.TIMEOUT).json()
        logger_info.info(result)
        return result

    def face_focus_trace(self, user_id, date):
        """关注人员搜索"""
        data = {
            "name": user_id,
            "date": date  # 20210728
        }
        result = requests.post(url=self.face_focus_search_url, json=data, timeout=self.TIMEOUT).json()
        logger_info.info(result)
        check_id_list = []
        if result.get('error') == 0:
            for item in result.get('result'):
                check_id_list.append([Hasher.to_object_pk(item[0]), item[1]])
        check_id_list.sort(key=lambda x: x[0])
        return check_id_list


face_discern = FaceDiscern()
