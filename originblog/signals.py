from threading import Thread

from blinker import Namespace
from flask import request, url_for
from mongoengine import DoesNotExist

from originblog.models import Tracker, PostStatistic
from originblog.settings import BlogSettings
from originblog.utils import submit_url_to_baidu

# 创建信号
app_signals = Namespace()
post_visited = app_signals.signal('post-visited')
post_published = app_signals.signal('post-published')


# 创建信号订阅者
@post_visited.connect
def on_post_visited(sender, post, **kwargs):
    """更新文章统计数据与浏览记录

    文章被浏览后，获取浏览者信息并更新文章统计数据
    """
    tracker = Tracker(post=post)
    # 获取请求来源ip与用户代理
    proxy_list = request.headers.getlist('X-Forwarded-For')
    tracker.ip = proxy_list[0] if proxy_list else request.remote_addr
    tracker.user_agent = request.headers.get('User-Agent')
    tracker.save()

    # 获取该文章的统计数据，若不存在则创建并初始化
    try:
        post_statistic = PostStatistic.objects.get(post=post)
    except DoesNotExist:
        post_statistic = PostStatistic(post=post, post_type=post.type)
        from random import randint
        post_statistic.verbose_count_base = randint(500, 5000)
        post_statistic.save()

    post_statistic.modify(inc__visit_count=1)


@post_published.connect
def on_post_published(sender, post):
    """对文章进行SEO优化

    文章发布后，将链接地址提交到百度站长平台，以被收录进搜索结果
    """
    post_type = post.type
    endpoints = {
        'post': 'blog.show_post',
        'page': 'blog.show_page'
    }
    post_url = url_for(endpoints[post_type], slug=post.slug, _external=True)
    baidu_url = BlogSettings.SEARCH_ENGINE_SUBMIT_URLS['baidu']
    if baidu_url:
        # 异步发送网络请求
        thr = Thread(target=submit_url_to_baidu, args=(baidu_url, post_url))
        thr.start()
        return thr
    else:
        print('Not ready to submit urls yet')
