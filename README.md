# sql-lab

西安交大计算机数据库系统的lab作业

## Installation

在openEuler上部署openGauss, 需要遵循以下步骤:

1. 修改环境变量: 在`/etc/profile`中添加: `export LANG=zh_CN.UTF-8`
2. 安装openGauss: `yum install opengauss`
3. 切换到`opengauss`用户: `su - opengauss`
4. 使用`opengauss`用户打开opengauss数据库: `gsql -d postgres -p 7654 -r`. 这里的端口号是根据后文的配置文件`postgresql.conf`中的`port`参数来指定
5. 配置密码: `ALTER USER opengauss PASSWORD 'your_password';`. **注意, 单引号和分号都必不可少**
6. 配置远程: 在`opengauss`用户下, 打开`./data/postgresql.conf`文件, 将`listen_addresses = '127.0.0.1'`改为`listen_addresses = '*'`; 取消注释`local_bind_address = '0.0.0.0'`, 记住其中的`port`参数(默认为7654)

## Connection

要使得能远程连接到opengauss数据库, 需要进行如下配置:

1. 修改`postgresql.conf`, 使得`password_encryption_type=1`
2. 修改`pg_hba.conf`, 在访问控制表中新增一行: `host all all 192.168.1.0/24 sha256`, 其中IP地址可以自行选择, 最后一项为加密方式, 这里选择`sha256`
3. 创建一个新的用户, 因为opengauss禁止用初始用户远程连接: `CREATE USER <username> WITH SYSADMIN password 'your_password';`
4. 开放端口, 这里以openEuler为例: 在root用户下, 执行`firewall-cmd --add-port 7654/tcp`
