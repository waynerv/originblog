# OriginBlog

[OriginBlog](https://github.com/flyhigher139/OctBlog) 是一个由 [Flask](http://flask.pocoo.org/) 和 [MongoDB](https://www.mongodb.org/) 驱动的博客系统。

OriginBlog的目标是打造一个轻量、美观且易扩展的博客系统，它具有以下特性：

- 支持多用户
- 基于角色的权限访问控制，可自定义角色
- 文章、个人页面、分类、标签、首页组件等博客功能
- 以 Markdown 作为主要内容编辑格式
- 可对所有资源进行编辑的后台管理页面
- 使用 Restful 风格 API 管理后台资源
- 通过配置文件与环境变量即可修改博客基本设置
- 支持自定义首页插件
- 自动根据文章内容生成目录
- 支持通过权重排序或隐藏文章
- 支持 Docker 快速部署

## Demo

[Origin Blog](shallwecode.top)

## 运行

### 从源码运行

1. 切换到项目根目录下的 `app` 文件夹。
2. 根据 `Pipfile` 或 `requirements.txt` 创建虚拟环境并安装依赖（推荐使用 pipenv）。
3. （可选）在当前目录创建 `.env` 配置文件，根据 `./originblog/settings.py` 文件中的配置项修改应用配置。
4. 安装 MongoDB 并启动服务器实例。
5. 在虚拟环境下，运行 `flask run` 命令以调试模式启动应用。


### 通过 docker 运行（推荐）

推荐使用 docker 运行项目，项目中还包括了 MongoDB、Nginx 和 gunicorn 等部署环境下的配置文件，通过 docker 可以做到自动化快速部署。

使用前请确保你已经正确安装 docker 与 docker-compose 。（建议配置国内的加速镜像源）

#### 首次运行

**1\. 获取 OriginBlog 镜像**

在命令行中切换到项目根目录，运行以下命令构建 OriginBlog 镜像：

```bash
$ (sudo) docker build app/ -t originblog:0.1 
# 该命令将根据 app/ 文件夹下的 Dockerfile 构建镜像
```

默认的 gunicorn 运行参数可在 Dockerfile 中修改，然后重新构建镜像。

你也可以直接从 DockerHub 拉取已构建好的镜像（视网络状况）：

```bash
$ (sudo) docker pull waynerv/octblog:0.1
```

**2\. 修改运行容器的配置文件（可跳过）**

- 修改 `docker-compose.yml`

切换到项目根目录下的 `compose` 文件夹。出于安全考虑，你需要对文件夹中 `docker-compose.yml` 文件中的环境变量进行适当修改（开发环境也可直接运行），以下是修改项：

- `MONGODB_ADMINUSERNAME`：应用程序连接 MongoDB 的用户名
- `MONGODB_ADMINPASSWORD`：应用程序连接 MongoDB 的密码
- `MONGO_INITDB_ROOT_USERNAME`：MongoDB 的用户管理员用户名
- `MONGO_INITDB_ROOT_PASSWORD`：MongoDB 的用户管理员密码

后两项配置为开启 MongoDB 验证机制所需参数，创建**用户管理员**后才可以启用验证并为数据库创建用户和分配权限。

- 修改 MongoDB 运行脚本

若修改了以上配置，还需要对根目录下 `mongodb/entrypoint/init_user.sh` 脚本文件中对应的共4项用户名和密码进行修改，该数据库脚本为应用程序创建专门的用户。

以上敏感配置项在部署环境下应在使用后删除。MongoDB 容器与应用间的通讯与外部请求隔离在不同的网络环境，但建议仍然开启 MongoDB 的验证机制以提高安全性。

- 修改 Nginx 配置

部署环境下还需要修改项目根目录下 `nginx/project.conf` 文件，对 Nginx 的映射域名进行修改：

```bash
server_name localhost;
# localhost 改成映射的域名
```

**3\. 运行容器**

切换到根目录下的 `compose` 文件夹，运行以下命令：

```bash
$ (sudo) docker-compose up -d
```

容器首次启动需要30秒左右，然后你就可以在浏览器中通过 `http://localhost:80` 访问OriginBlog 了。

除了数据库用户密码以外，应用程序使用的环境变量都可以在 `docker.env` 文件中修改。

示例:

```
# MongoDB的连接配置，谨慎修改
MONGO_HOST=mongo 
MONGO_PORT=27017
DB_NAME=originblog

# Flask使用的密钥，应使用随机生成值
SECRET_KEY=random_value1231

# 应用邮件服务器的配置
MAIL_SERVER=xxxx
MAIL_USERNAME=xxxx
MAIL_PASSWORD=xxxx
MAIL_USE_TLS=True
MAIL_PORT=xxxx

# 以此邮箱注册将赋予管理员角色
ORIGINBLOG_ADMIN_EMAIL=xxxx

# SEO相关配置
baidu_submit_url=xxxx
baidu_site_verificatio=xxxx

# 博客内容配置
name=Waynerv's Blog
subtitle=Concentration and Perseverance matter.
description=Origin Blog Description
keywords=python,flask,web,MongoDB
owner=Waynerv
```

更多配置项参见 `./originblog/settings.py` 。

**4. 进入 OriginBlog 容器**

如果你想进入 OriginBlog 应用容器的内部，可执行以下命令:

```bash
$ (sudo) docker exec -it blog ash
# orginblog 运行在alpine(一个极简linux)环境中,ash=alpine shell
```

#### 首次运行后

- 关闭 OriginBlog

```bash
$ (sudo) docker-compose stop
```

- 启动 OriginBlog

```bash
$ (sudo) docker-compose start
```

- 删除 OriginBlog

```bash
$ (sudo) docker-compose down
```

`docker-compose` 命令应在切换到根目录下 `compose/` 文件夹中时执行。

容器运行时产生的数据包括数据库文件可通过 `docker volume` 进行删除、备份等操作。

### 使用 OriginBlog

#### 1\. 创建管理员账户

以 `ORIGINBLOG_ADMIN_EMAIL` 环境配置值为邮箱注册的用户将成为管理员。

开发环境下可使用 `Role` 模型的 `init` 方法重置角色权限，然后运行 `flask init` 注册管理员用户。

#### 2\. 进入博客后台

登录后通过首页右上角 `USER` 下拉菜单的 `Dashboard` 即可进入管理后台。

在博客后台可执行发布文章、审核评论、添加用户、增加首页组件、查看统计数据等管理功能。

#### 3\. 创建专用页面

专用页面是指博客的介绍、捐赠页面等具有专门作用的页面，该页面将在首页上方的导航栏拥有入口。

创建专用页面首先需要设置 `settings.py` 文件中`BLOG_META` 的 `index_nav` 参数（默认最多同时展示两个），然后在后台点击 `New Page` 创建与 `index_nav` 同名的文章即可。

#### 4\. 修改更多默认配置

你可以通过修改 `app/originblog/settings.py` 文件，修改 `.env` 文件或者直接添加环境参数来修改博客的各项配置。

注意 `docker.env` 配置文件仅在使用 docker-compose 运行容器时生效。

## 解释

权重用于排序文章，每篇文章的默认权重为10，如果文章的权重大于10则优先显示，如果权重为负，则文章不会显示在首页。

配置文件

MongoDB的验证

## 依赖

### 后端

- Flask
  - flask-login
  - flask-mail
  - Flask-WTF
  - bootstrap-flask
  - flask-mongoengine
  - flask-moment
- WTForms
- mongoengine
- markdown2
- bleach

### 前端

- jQuery(3.4.0)
  - jquery.easing
  - jquery.toc
- BootStrap(4.3.1)
  - [Clean Blog](https://startbootstrap.com/themes/clean-blog/)
  - [SB Admin 2](https://startbootstrap.com/themes/sb-admin-2/)
- Font Awesome(5.8.1)
- [EasyMDE](https://github.com/Ionaru/easy-markdown-editor)
- highlight.js

## 许可证

MIT

## 更新计划
