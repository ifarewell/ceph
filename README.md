# vod平台

平台本地运行步骤：
```shell
# 创建python虚拟环境
python -m venv vodvenv

# 激活虚拟环境
# linux
source ./vodvenv/bin/activate

# windows
.\vodvenv\Scripts\activate.bat

# 安装所需包
pip install -r requirements.txt

# 初始化bucket
flask initdb --drop

# 创建视频数据
flask forge

# 启动调试
flask run

# 服务器部署
python wsgi.py
```

