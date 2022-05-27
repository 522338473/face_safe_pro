# CSIA智能视图平台

CSIA智能视图平台 | 使用python3基于Django框架进行前后端不分离方式开发，以pipenv作为包管理工具
> 采用前后端不分离方式开发。前端扩展页面建议采用element-ui开发

## 本地安装&运行

### 本地安装

1. 安装pip3，python3
   ```bash
   建议安装3.8.x系列Python工具包
   ```

2. 安装pipenv
   ```bash
   pip3 install pipenv -i https://mirrors.aliyun.com/pypi/simple/
   ```

3. 进入项目根目录
   ```bash
   cd face_safe_pro
   ```

4. 安装项目依赖
   ```bash
   pipenv sync && pipenv install --dev
   ```

### 本地环境运行

1. 进入项目根目录
   ```bash
   cd face_safe_pro
   ```

2. 运行代码
   ```bash
   pipenv run python manage.py runserver 0.0.0.0:9999
   ```

3. 浏览器访问
   ```bash
   本地访问: http://127.0.0.1:9999/admin
   局域网访问: http://localip:9999/admin
   ```

4. 默认超级管理员账户账户
   ```bash
   用户名: admin
   密码: Admin!2345
   ```

---

> 默认列表页为: templates/admin/change_list.html 设备管理列表页: templates/admin/device/deviceinfo/change_list.html
>
> 如不配置用默认。如果配置用自己的


## 系统启动

相关配置文件修改为本地服务器ip之后，执行 `docker-compose up -d` 即可一键启动相关服务

```text
root@iZ7xvfilg50y49nj2t2jqdZ:~/face_safe_pro# docker-compose ps
                   Name                                  Command               State                                                           Ports
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
face_safe_cisa-live_1_a75eb2ca6037            ./run.sh                         Up      0.0.0.0:1935->1935/tcp,:::1935->1935/tcp, 0.0.0.0:3000->3000/tcp,:::3000->3000/tcp,
                                                                                       0.0.0.0:7001->7001/tcp,:::7001->7001/tcp
face_safe_face-safe-celery_1_345577226ad6     sh start.sh celery               Up
face_safe_face-safe-mq_image_1_cd61e88b0f62   sh start.sh mq_image             Up
face_safe_face-safe_1_d54810675be9            sh start.sh                      Up      0.0.0.0:8000->8000/tcp,:::8000->8000/tcp
face_safe_go-fastdfs_1_5ff166a19e25           fileserver server ${OPTS}        Up      0.0.0.0:8089->8080/tcp,:::8089->8080/tcp
face_safe_hwface_1_bb2ce04494f7               ./run.sh                         Up
face_safe_nginx_1_29041b3e81e6                /docker-entrypoint.sh ngin ...   Up      0.0.0.0:443->443/tcp,:::443->443/tcp, 0.0.0.0:80->80/tcp,:::80->80/tcp
face_safe_postgresql_1_708eaa8a6e67           docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp,:::5432->5432/tcp
face_safe_rabbitmq_1_efe5a0b385f0             docker-entrypoint.sh rabbi ...   Up      15671/tcp, 0.0.0.0:15672->15672/tcp,:::15672->15672/tcp, 15691/tcp, 15692/tcp, 25672/tcp, 4369/tcp, 5671/tcp,
                                                                                       0.0.0.0:5672->5672/tcp,:::5672->5672/tcp
face_safe_redis_1_665827c74752                docker-entrypoint.sh redis ...   Up      0.0.0.0:6379->6379/tcp,:::6379->6379/tcp
```


docker-compose基本命令(在compose.yml所在目录执行，否则需要-f指定)

```text
docker-compose  version                        # 查看docker-compose版本信息
docker-compose  images                         # 列出镜像
docker-compose  images -q                      # 列出镜像ID
docker-compose up -d nginx                     # 构建建启动nignx容器
docker-compose exec nginx bash                 # 登录到nginx容器中
docker-compose  exec nginx env                 # 在容器中运行命令
docker-compose down                            # 删除所有nginx容器,镜像
docker-compose ps                              # 显示所有容器
docker-compose restart nginx                   # 重新启动nginx容器
docker-compose build nginx                     # 构建镜像 。        
docker-compose build --no-cache nginx          # 不带缓存的构建。
docker-compose logs  nginx                     # 查看nginx的日志 
docker-compose logs -f nginx                   # 查看nginx的实时日志
docker-compose config  -q                      # 验证（docker-compose.yml）文件配置，当配置正确时，不输出任何内容，当文件配置错误，输出错误信息。 
docker-compose events --json nginx             # 以json的形式输出nginx的docker日志
docker-compose pause nginx                     # 暂停nignx容器
docker-compose unpause nginx                   # 恢复ningx容器
docker-compose rm nginx                        # 删除容器（删除前必须关闭容器）
docker-compose stop nginx                      # 停止nignx容器
docker-compose start nginx                     # 启动nignx容器
docker-compose  top                            # 显示运行进程
docker-compose  top nginx                      # 指定某一个service
```


部署注意事项: `程序初始化之后建议重启所有容器让配置重载`

```text
# arm64 版本部署续替换镜像标签 sudo sed -i 's#latest#arm64#g' docker-compose.yml
# arm64 docker-compose不可通过命令安装，自行百度安装，安装成功执行脚本

# 通用步骤
sudo rm -rf .env
sudo mv .env_dev .env
sudo sed -i 's#172.17.0.1#192.168.3.97#g' .env
sudo sed -i 's#172.17.0.1#192.168.3.97#g' docker-compose.yml
sudo sh setup.sh # 为了避免文件存储错误，建议第一次启动程序脚本！后续直接采用命令即可
```

`.env配置文件`

```text
DJANGO_DEBUG=1  # 生产环境debug需要关闭

DJANGO_DATABASE=pg  # 默认使用的数据库

DB_NAME=face_safe_pro  # 数据库名称
DB_USER=postgres  # 数据库用户
DB_PASSWORD=postgres  # 数据库密码
DB_HOST=192.168.2.89  # 数据库host
DB_PORT=5432  # 数据库port

FAST_DFS_HOST=http://192.168.2.89:8089  # 文件存储服务
SEARCH_SERVER_HOST=http://192.168.2.89:5000  # 搜索服务
SEARCH_REAL_TIME_HOST=http://192.168.2.84:8083  # 视频流转换服务
SEARCH_VIDEO_HOST=http://192.168.2.84:3000  # 视频回放服务
VIDEO_HOST=http://192.168.2.84:10081  # MP4视频服务

RABBITMQ_USERNAME=admin  # mq用户名
RABBITMQ_PASSWORD=admin  # mq密码
RABBITMQ_HOST=192.168.2.89  # mq_host
RABBITMQ_PORT=5672  # mq_port

REDIS_SERVER_HOST=192.168.2.89  # redis_host
REDIS_SERVER_PORT=6379  # redis_port
REDIS_CACHE_DB=1  # redis_db

BAIDU_SEARCH_APPID=test  # 私有化appid

DOUBLE_NETWORK=1  # 是否启用双网卡配置
D_REDIS_SERVER_HOST=192.168.2.89  # 双网卡

SSD_DIR=/mnt/data  # 数据盘
DEL_DAY=180  # 删除180天以前的数据
DEL_RATE=70  # 超过70%删除

BIG_SCREEN=1  # 是否开启大屏
PUSH_ROLL_CALL=0  # 大屏推送

```