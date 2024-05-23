# sql-lab

西安交大计算机数据库系统的lab作业

## Installation

在openEuler上部署openGauss, 需要遵循以下步骤:

1. 修改环境变量: 在`/etc/profile`中添加: `export LANG=zh_CN.UTF-8`
2. 安装openGauss: `yum install opengauss`
3. 切换到`opengauss`用户: `su - opengauss`
4. 使用`opengauss`用户打开opengauss数据库: `gsql -d postgres -p 7654 -r`. 这里的端口号是根据后文的配置文件`postgresql.conf`中的`port`参数来制定
5. 配置密码: `ALTER USER opengauss PASSWORD 'your_password';`. **注意, 单引号和分号都必不可少**
6. 配置远程: 在`opengauss`用户下, 打开`./data/postgresql.conf`文件, 将`listen_addresses = '127.0.0.1'`改为`listen_addresses = '*'`; 取消注释`local_bind_address = '0.0.0.0'`, 记住其中的`port`参数(默认为7654)
