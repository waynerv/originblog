from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app
from itsdangerous import BadTimeSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from originblog.extensions import db
from originblog.settings import Operations


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


def generate_token(user, operation, expire_in=None, **kwargs):
    """生成私密操作所需要的验证token

    使用itsdangerous提供的jws序列化器将用户信息、操作类型等序列化成token
    :param user: 用户对象
    :param operation: 操作类型 Operations 类属性
    :param expire_in: 过期时间（秒），默认值None时为一个小时
    :param kwargs: 其他需要序列化的关键字参数（如新的邮箱地址）
    :return: 序列化生成的token
    """
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)  # 接收密钥和过期时间（秒）参数实例化一个JWS序列化器对象
    data = {
        'username': user.username,
        'operation': operation
    }
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, token, operation, new_password=None):
    """验证token，并根据token携带的数据执行相应操作

    :param user: 用户对象
    :param token: token字符串
    :param operation: 要验证的操作类型（确认邮箱、重置密码或修改邮箱）
    :param new_password: 若操作类型为重置密码可将新密码作为参数传入
    :return: 布尔值
    """
    s = Serializer(current_app.config['SECRET_KEY'])

    # 尝试获取token中被序列化的信息，token不一定合法，应使用try...except语句
    try:
        data = s.loads(token)
    except (BadTimeSignature, SignatureExpired):
        return False

    # 验证token携带的用户名和操作类型是否相符
    if operation != data.get('operation') or user.username != data.get('username'):
        return False

    # 根据不同的操作类型执行对应操作
    if operation == Operations.CONFIRM:
        user.email_confirmed = True
    elif operation == Operations.RESET_PASSWORD:
        user.set_password(new_password)
    elif operation == Operations.CHANGE_EMAIL:
        user.email = data.get('new_email')
    else:
        return False

    db.save()
    return True