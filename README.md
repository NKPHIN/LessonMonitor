# LessonMonitor

#### 介绍
基于mediapipe的上课行为监测软件

#### 调试与部署
-- 本地调试指南

1. 创建pycharm项目和虚拟环境

2. 从Pycharm中导入
   Flask
   PyMySQL
   gevent
   requests
   PyQt5
   mediapipe
   按默认版本号即可

3. 分别修改server、student、teacher
   三个文件夹中的config.py配置文件
   IP: 127.0.0.1
   Port: 8080
   数据库连接须先执行ddl.sql文件
   再进行配置

4. 服务器从server.py文件中启动
   学生端从student_login.py中启动
   教师端从teacher_login.py中启动

-- 在线调试指南

1. 创建pycharm项目和虚拟环境

2. 进入虚拟环境并执行命令
   pip install -r requirements.txt
   从requirements文件中导入相应模块

3. 分别修改student、teacher
   两个文件夹中的config.py配置文件
   IP和Port见飞书云文档中部署方案

4. 学生端从student_login.py中启动
   教师端从teacher_login.py中启动
