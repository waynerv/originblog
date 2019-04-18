import os
from urllib.parse import urlparse, urljoin

import requests
from flask import request, redirect, url_for
from mongoengine import DoesNotExist


def redirect_back(default='blog.index', **kwargs):
    """跳转到请求中指定的地址（或发送请求的页面）

    尝试从当前请求的next查询参数以及Referer首部字段中获取要跳转的页面地址，
    并对改地址进行安全性校验，next查询参数需要在发送请求时传入。
    :param default: 默认的跳转端点
    :param kwargs: 跳转到默认端点时添加的关键字参数
    """
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        elif is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    """校验跳转的目标url是否安全以防止开放重定向攻击

    判断方法是对比目标url与当前请求url的主机地址是否相同，避免将用户跳转到另一站点

    解释：开放重定向出现在应用接受参数并将用户重定向到该参数值，并且没有对该值进行任何校验的时候。
    该参数是可被添加修改的，假设用户点击了一个信任站点的登录链接，但链接中添加了恶意网站地址作为跳转参数（例如next查询参数）
    用户登录后即可能被重定向到恶意站点，并误认为该恶意站点是可信任的（尤其是该恶意站点伪装成信任站点的时候）
    :param target: 要检查的目标url
    :return: 布尔值
    """
    ref_url = urlparse(request.host_url)  # 将请求的主机地址（含协议）解析为6元组(scheme, netloc, path, params, query, fragment)
    test_url = urlparse(urljoin(request.host_url, target))  # 合并baseurl和url， 优先保留url中的地址（因为target可能是相对地址）
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc  # 对比网址的主机地址


def submit_url_to_baidu(baidu_url, url):
    """使用request手动提交文章链接到百度站长平台"""
    result = requests.post(baidu_url, data=url)
    return result


def reply_filter(comment, flag=True):
    """在模板中捕获回复的原评论被删除时引发的异常"""
    try:
        return comment.reply_to
    except DoesNotExist:
        return flag

def get_boolean_from_env(key, default=''):
    """从环境变量中获取布尔值"""
    return os.getenv(key, default).lower() not in ('false', '0', 'no')


def get_int_from_env(key, default=0):
    """从环境变量中获取整型"""
    try:
        return int(os.getenv(key, default))
    except ValueError:
        return default

