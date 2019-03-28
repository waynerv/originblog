from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for



def redirect_back(default='index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        elif is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)  # 将请求的主机地址（含协议）解析为6元组(scheme, netloc, path, params, query, fragment)
    test_url = urlparse(urljoin(request.host_url, target))  # 合并baseurl和url， 优先保留url中的地址
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc  # 对比网址的主机地址
