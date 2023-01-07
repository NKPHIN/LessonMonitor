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
   IP: 140.210.222.111
   Port: 5000

4. 学生端从student_login.py中启动
   教师端从teacher_login.py中启动

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
