#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect,render
import time, datetime
from CMDB import settings
from web.models import AccessLog


class AccessTimesLimitMiddleware(MiddlewareMixin):
    """
    定义访问频率限制的中间件
    """
    def process_request(self, request):
        if request.path.__contains__("login") and request.method == "POST":

            access_time = settings.ACCESS_TIME if hasattr(settings, 'ACCESS_TIME') else 60
            ip = request.META.get('REMOTE_ADDR')
            request_path = request.path
            # 查询该IP的访问记录
            ip_access_log = AccessLog.objects.filter(remote_ip=ip)
            now = time.time()
            if ip_access_log:

                # 按照ID升序排序，ID大的是最新插入进去的，所以第一条是最旧的记录
                last_access_log = ip_access_log.order_by('id').first()
                # print("=========================", last_access_log.access_time)

                first_access_time = last_access_log.access_time.timestamp()
            else:
                # 如果该访问IP不在访问记录中，就设置第一次访问时间为当前时间
                first_access_time = now
            # 时间间隔过了设置的access_time，用户就可以重新访问了，重新获得访问次数
            if float(now)-first_access_time > access_time:
                ip_access_log.delete()

            access_limit = settings.ACCESS_LIMIT if hasattr(settings, 'ACCESS_LIMIT') else 5
            if ip_access_log.count() >= access_limit:
                # 多少秒后访问
                wait_second = round(access_time-(float(now)-first_access_time), 2)
                # "%s 秒内只允许访问%s次" % (access_time, access_limit)
                return HttpResponse("%s 秒内只允许访问%s次，请%s 秒后尝试" % (access_time, access_limit, wait_second))

            AccessLog.objects.create(remote_ip=ip, request_path=request_path)
