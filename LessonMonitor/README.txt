-- 目录结构

.
├── README.txt
├── detect                    识别算法
│   ├── Absence.py
│   ├── Pry.py
│   ├── Sleep.py
│   ├── Talk.py
│   └── detect.py
├── server                    后端、数据库连接
│   ├── config.py
│   ├── database.py
│   └── server.py
├── sql                       sql脚本
│   └── ddl.sql
├── img                       点位编号
│   ├── landmark_line.png
│   └── landmarks.png
├── student                   本地客户端(学生端)
│   ├── background.png
│   ├── client.py
│   ├── config.py
│   ├── student_login.py
│   ├── student_register.py
│   └── window.py
├── teacher                   本地客户端(教师端)
│   ├── client.py
│   ├── config.py
│   ├── teacher_login.py
│   └── teacher_windows.py
└── ui                         ui辅助文件
    ├── student_login.ui
    ├── student_register.ui
    └── window.ui


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
   IP: 140.210.222.111
   Port: 5000

4. 学生端从student_login.py中启动
   教师端从teacher_login.py中启动


NKPHIN
2023-01-07
