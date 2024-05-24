# Ubuntu

## 系统安装

在VMware中新建虚拟机

![20180620200651158](assets/20180620200651158.png)

![1555322379232](assets/1555322379232.png)



![1555322411473](assets/1555322411473.png)



指定当前虚拟机使用的系统镜像

![1555406823989](assets/1555406823989.png)





设置系统的登录账号密码，设置完成以后一定要记住。

![1555406875540](assets/1555406875540.png)



![1555322558054](assets/1555322558054.png)



![1555322574001](assets/1555322574001.png)



![1555322584853](assets/1555322584853.png)



![1555322605989](assets/1555322605989.png)



![1555322613074](assets/1555322613074.png)



![1555322619297](assets/1555322619297.png)



![1555322626102](assets/1555322626102.png)



![1555322643496](assets/1555322643496.png)



![1555322651420](assets/1555322651420.png)



![1555322658865](assets/1555322658865.png)





![1555322696354](assets/1555322696354.png)



![1555407034888](assets/1555407034888.png)



![1555407053476](assets/1555407053476.png)



一直等待，系统初始化安装，知道出现下方界面：

![1555407978602](assets/1555407978602.png)



输入前面设置的密码，点击Sign In

![1555408000095](assets/1555408000095.png)



点击右上角绿色按钮，一路next即可。

![1555408167496](assets/1555408167496.png)



点击Install Now，下载最新版本的ubuntu软件库。

![1555408927535](assets/1555408927535.png)



输入登录密码。

![1555409110692](assets/1555409110692.png)



![1555409235259](assets/1555409235259.png)



选择稍后重启 Restart Later

![1555409767922](assets/1555409767922.png)



## 更改系统语言为中文

点击屏幕右上角 设置按钮

![1555409861780](assets/1555409861780.png)



选择地区和语言设置 Region & Language

然后选择 语言安装管理 Manage Installed Languages 

![1555410041516](assets/1555410041516.png)



![1555410055056](assets/1555410055056.png)



点击Install ，下载安装语言包，必须联网。

下载安装语言包需要管理员授权，所以还是输入登录密码。

![1555410117339](assets/1555410117339.png)



![1555410182580](assets/1555410182580.png)



点击 install/remove language，安装语言包

![1555410217668](assets/1555410217668.png)



在弹出窗口中，找到chinese(simplified) 和English，勾选上再点击Apply

![1555410324956](assets/1555410324956.png)



等待下载完成。

![1555410343152](assets/1555410343152.png)



在已经下载完成的语言列表中找到汉语（中国），并把它拖到语言列表的最上方位置，并点选Apply System-Wide，最后点击Close关闭当前窗口。

![1555411260859](assets/1555411260859.png)



重启ubuntu

![1555411352862](assets/1555411352862.png)

![1555411390939](assets/1555411390939.png)



重启后的ubuntu，会弹出提示将标准文件夹更新到当前语言吗？选择 保留旧的名称 

如果使用的是centos7或以上版本，我会在下面的指令中进行提示。没有提示的就是cenots和Ubuntu通用的。



```bash
sudo tzselect
# 选项Asia  4  centos是5
# 选项China 9
# 选项beijing 1
# 选项Yes     1
```

![1559058496068](./assets/1559058496068.png)

![1559058552593](.\assets\1559058552593.png)

```bash
下面这些可以先忽略，安装centos时指定好了时区了
# 复制时区文件
sudo cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
# 安装ntp时间服务器
sudo apt install ntpdate
# 同步ntp时间服务器
sudo ntpdate time.windows.com
# 将系统时间与网络同步
ntpdate cn.pool.ntp.org
# 将时间写入硬件
hwclock --systohc

# 重启Ubuntu
```



## 安装基本使用软件

### Vim

```bash
ubuntu:
	sudo apt install vim
centos7:
	yum -y install vim  #如果报错，可能是你网络有问题，如果网络没问题，那么看下面网址的解决方案
	CentOS7用yum安装软件显示错误：cannot find a valid baseurl for repo: base/7/x86_64
	参考网址：https://blog.csdn.net/qq_37922264/article/details/81054673
	但是注意，安装完成之后，将里面的文件再改回来，不然安装其他软件的时候会有问题，执行下面的指令：
	mv  /etc/yum.repos.d/CentOS-Base.repo.bak    /etc/yum.repos.d/CentOS-Base.repo
```

![1555470919223](assets/1555470919223.png)



### chrome

#### Ubuntu下安装chrome

使用ubuntu内置的火狐浏览器打开谷歌浏览器的下载 地址：

<http://www.google.cn/intl/zh-CN/chrome/browser/desktop/index.html>

![1555466987568](assets/1555466987568.png)



选择Ubuntu版本

![1555467043282](assets/1555467043282.png)



点选 保存文件，默认会保存在用户家目录下的 Downloads目录下

![1555467087378](assets/1555467087378.png)



![1555471035561](assets/1555471035561.png)



![1555471112932](assets/1555471112932.png)



![1555471142332](assets/1555471142332.png)



![1555471162743](assets/1555471162743.png)



![1555471209936](assets/1555471209936.png)



可以选择把图标拉动到左侧收藏栏中，方便快速打开。

![1555467889227](assets/1555467889227.png)



![1555467966573](assets/1555467966573.png)



![1555467980106](assets/1555467980106.png)





#### centos7 安装chrome

1. 首先从Google官方网站下载google chrome安装包 http://www.google.cn/chrome/browser/desktop/index.html

![image-20200524140754282](assets/image-20200524140754282.png)



选择Linux系统，并下载google-chrome-stable_current_x86_64.rpm

然后点击下载，提示信息中勾选一个保存，默认会保存到我们的用户桌面/home/chao/Download里面

cd 进入到下载文件夹

然后执行下面的指令：

```
sudo yum localinstall google-chrome-stable_current_x86_64.
按照提示一路输入y然后回车就行了
```

提示安装完毕就看到下面的页面了：

![image-20200524141520374](assets/image-20200524141520374.png)



### 搜狗输入法

#### Ubuntu下安装

访问搜狗输入法For Linux

<https://pinyin.sogou.com/linux/?r=pinyin>

![1555471345709](assets/1555471345709.png)



![1555471416927](assets/1555471416927.png)



![1555471442196](assets/1555471442196.png)



![1555471709889](assets/1555471709889.png)



![1555471730863](assets/1555471730863.png)



![1555471759032](assets/1555471759032.png)



关闭窗口后，重启ubuntu。

![1555471781326](assets/1555471781326.png)



![1555472039635](assets/1555472039635.png)



#### centos7下安装

##### 我没装，哈哈，太麻烦。目前到了这里



### Pycharm

![1555472662852](assets/1555472662852.png)



![1555473218834](assets/1555473218834.png)



![1555474613731](assets/1555474613731.png)



![1555474739744](assets/1555474739744.png)



![1555469017912](assets/1555469017912.png)



![1555469066192](assets/1555469066192.png)

合理使用地址：<http://idea.lanyus.com/>

第一步 将：0.0.0.0 https://account.jetbrains.com:443加入hosts
第二步 打开终端，输入`sudo /etc/init.d/networking restart `，刷新dns缓存
第三步 在 Activation code 输入 lanyu 序列号

```python
56ZS5PQ1RF-eyJsaWNlbnNlSWQiOiI1NlpTNVBRMVJGIiwibGljZW5zZWVOYW1lIjoi5q2j54mI5o6I5p2DIC4iLCJhc3NpZ25lZU5hbWUiOiIiLCJhc3NpZ25lZUVtYWlsIjoiIiwibGljZW5zZVJlc3RyaWN0aW9uIjoiRm9yIGVkdWNhdGlvbmFsIHVzZSBvbmx5IiwiY2hlY2tDb25jdXJyZW50VXNlIjpmYWxzZSwicHJvZHVjdHMiOlt7ImNvZGUiOiJJSSIsInBhaWRVcFRvIjoiMjAyMC0wMy0xMCJ9LHsiY29kZSI6IkFDIiwicGFpZFVwVG8iOiIyMDIwLTAzLTEwIn0seyJjb2RlIjoiRFBOIiwicGFpZFVwVG8iOiIyMDIwLTAzLTEwIn0seyJjb2RlIjoiUFMiLCJwYWlkVXBUbyI6IjIwMjAtMDMtMTAifSx7ImNvZGUiOiJHTyIsInBhaWRVcFRvIjoiMjAyMC0wMy0xMCJ9LHsiY29kZSI6IkRNIiwicGFpZFVwVG8iOiIyMDIwLTAzLTEwIn0seyJjb2RlIjoiQ0wiLCJwYWlkVXBUbyI6IjIwMjAtMDMtMTAifSx7ImNvZGUiOiJSUzAiLCJwYWlkVXBUbyI6IjIwMjAtMDMtMTAifSx7ImNvZGUiOiJSQyIsInBhaWRVcFRvIjoiMjAyMC0wMy0xMCJ9LHsiY29kZSI6IlJEIiwicGFpZFVwVG8iOiIyMDIwLTAzLTEwIn0seyJjb2RlIjoiUEMiLCJwYWlkVXBUbyI6IjIwMjAtMDMtMTAifSx7ImNvZGUiOiJSTSIsInBhaWRVcFRvIjoiMjAyMC0wMy0xMCJ9LHsiY29kZSI6IldTIiwicGFpZFVwVG8iOiIyMDIwLTAzLTEwIn0seyJjb2RlIjoiREIiLCJwYWlkVXBUbyI6IjIwMjAtMDMtMTAifSx7ImNvZGUiOiJEQyIsInBhaWRVcFRvIjoiMjAyMC0wMy0xMCJ9LHsiY29kZSI6IlJTVSIsInBhaWRVcFRvIjoiMjAyMC0wMy0xMCJ9XSwiaGFzaCI6IjEyMjkxNDk4LzAiLCJncmFjZVBlcmlvZERheXMiOjAsImF1dG9Qcm9sb25nYXRlZCI6ZmFsc2UsImlzQXV0b1Byb2xvbmdhdGVkIjpmYWxzZX0=-SYSsDcgL1WJmHnsiGaHUWbaZLPIe2oI3QiIneDtaIbh/SZOqu63G7RGudSjf3ssPb1zxroMti/bK9II1ugHz/nTjw31Uah7D0HqeaCO7Zc0q9BeHysiWmBZ+8bABs5vr25GgIa5pO7CJhL7RitXQbWpAajrMBAeZ2En3wCgNwT6D6hNmiMlhXsWgwkw2OKnyHZ2dl8yEL+oV5SW14t7bdjYGKQrYjSd4+2zc4FnaX88yLnGNO9B3U6G+BuM37pxS5MjHrkHqMTK8W3I66mIj6IB6dYXD5nvKKO1OZREBAr6LV0BqRYSbuJKFhZ8nd6YDG20GvW6leimv0rHVBFmA0w==-MIIElTCCAn2gAwIBAgIBCTANBgkqhkiG9w0BAQsFADAYMRYwFAYDVQQDDA1KZXRQcm9maWxlIENBMB4XDTE4MTEwMTEyMjk0NloXDTIwMTEwMjEyMjk0NlowaDELMAkGA1UEBhMCQ1oxDjAMBgNVBAgMBU51c2xlMQ8wDQYDVQQHDAZQcmFndWUxGTAXBgNVBAoMEEpldEJyYWlucyBzLnIuby4xHTAbBgNVBAMMFHByb2QzeS1mcm9tLTIwMTgxMTAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxcQkq+zdxlR2mmRYBPzGbUNdMN6OaXiXzxIWtMEkrJMO/5oUfQJbLLuMSMK0QHFmaI37WShyxZcfRCidwXjot4zmNBKnlyHodDij/78TmVqFl8nOeD5+07B8VEaIu7c3E1N+e1doC6wht4I4+IEmtsPAdoaj5WCQVQbrI8KeT8M9VcBIWX7fD0fhexfg3ZRt0xqwMcXGNp3DdJHiO0rCdU+Itv7EmtnSVq9jBG1usMSFvMowR25mju2JcPFp1+I4ZI+FqgR8gyG8oiNDyNEoAbsR3lOpI7grUYSvkB/xVy/VoklPCK2h0f0GJxFjnye8NT1PAywoyl7RmiAVRE/EKwIDAQABo4GZMIGWMAkGA1UdEwQCMAAwHQYDVR0OBBYEFGEpG9oZGcfLMGNBkY7SgHiMGgTcMEgGA1UdIwRBMD+AFKOetkhnQhI2Qb1t4Lm0oFKLl/GzoRykGjAYMRYwFAYDVQQDDA1KZXRQcm9maWxlIENBggkA0myxg7KDeeEwEwYDVR0lBAwwCgYIKwYBBQUHAwEwCwYDVR0PBAQDAgWgMA0GCSqGSIb3DQEBCwUAA4ICAQAF8uc+YJOHHwOFcPzmbjcxNDuGoOUIP+2h1R75Lecswb7ru2LWWSUMtXVKQzChLNPn/72W0k+oI056tgiwuG7M49LXp4zQVlQnFmWU1wwGvVhq5R63Rpjx1zjGUhcXgayu7+9zMUW596Lbomsg8qVve6euqsrFicYkIIuUu4zYPndJwfe0YkS5nY72SHnNdbPhEnN8wcB2Kz+OIG0lih3yz5EqFhld03bGp222ZQCIghCTVL6QBNadGsiN/lWLl4JdR3lJkZzlpFdiHijoVRdWeSWqM4y0t23c92HXKrgppoSV18XMxrWVdoSM3nuMHwxGhFyde05OdDtLpCv+jlWf5REAHHA201pAU6bJSZINyHDUTB+Beo28rRXSwSh3OUIvYwKNVeoBY+KwOJ7WnuTCUq1meE6GkKc4D/cXmgpOyW/1SmBz3XjVIi/zprZ0zf3qH5mkphtg6ksjKgKjmx1cXfZAAX6wcDBNaCL+Ortep1Dh8xDUbqbBVNBL4jbiL3i3xsfNiyJgaZ5sX7i8tmStEpLbPwvHcByuf59qJhV/bZOl8KqJBETCDJcY6O2aqhTUy+9x93ThKs1GKrRPePrWPluud7ttlgtRveit/pcBrnQcXOl1rHq7ByB8CFAxNotRUYL9IF5n3wJOgkPojMy6jetQA5Ogc8Sm7RG6vg1yow==
```



### Sublimetext 3

![1555475630890](assets/1555475630890.png)



![1555475665216](assets/1555475665216.png)



![1555475772154](assets/1555475772154.png)



![1555475945674](assets/1555475945674.png)





### virtualenvs

默认情况下ubuntu18.04版本中已经内置了Python3.6.7了。但是没有内置pip。所以先安装pip。

```bash
sudo apt install python3-pip
```

![1555486869608](assets/1555486869608.png)



![1555486897199](assets/1555486897199.png)



安装虚拟环境

```
pip3 install virtualenv
pip3 install virtualenvwrapper
```

![1555492891577](assets/1555492891577.png)

安装完成了以后，接下来需要配置系统环境变量

```bash
mkdir $HOME/.virtualenvs
```

执行命令，打开并编辑 ~/.bashrc

```bash
vim  ~/.bashrc
```

![1555493308420](assets/1555493308420.png)



文件末尾添加以下几行代码，`:wq` 保存退出。

```shell
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source ~/.local/bin/virtualenvwrapper.sh
```

![1555495251155](assets/1555495251155.png)

刷新配置文件

```bash
source ~/.bashrc
```

![1555493352631](assets/1555493352631.png)



![1555495302952](assets/1555495302952.png)

最后测试是否安装成功

```
workon
mkvirtualenv
```

![1555495399898](assets/1555495399898.png)



如果出现上面的错误，是因为 virtualenv 这个基础依赖包被安装在默认 Python 目录下，做一个virtualenv 的软连接到/usr/bin中给python3调用即可。

首先还是用 find 找到 virtualenv 的位置

```
sudo find / -name "virtualenv"
```

![1555495562038](assets/1555495562038.png)

创建软连接

```bash
sudo ln -s /home/moluo/.local/bin/virtualenv /usr/bin/virtualenv
```

注意：`/home/moluo/.local/bin/virtualenv` 根据前面find查找出来的结果而定

解决上面问题以后，再次执行就成功了。

![1555495835948](assets/1555495835948.png)



### mysql

从官方提供的mysql-apt-config.deb包进行APT源设置

Mysql下载地址：https://dev.mysql.com/downloads/mysql/

![1555483227691](assets/1555483227691.png)



![1555483413283](assets/1555483413283.png)



![1555483481421](assets/1555483481421.png)

APT源下载地址：https://dev.mysql.com/downloads/repo/apt/

![1555483637964](assets/1555483637964.png)



![1555483666999](assets/1555483666999.png)



![1555483797479](assets/1555483797479.png)



下载完成以后，默认apt源保存在了Downloads目录下。

![1555484649053](assets/1555484649053.png)



通过终端切换目录到Downloads目录下执行一下命令：

```bash
cd Downloads/
sudo dpkg -i mysql-apt-config_0.8.12-1_all.deb 
```

![1555485036396](assets/1555485036396.png)



![1555485058132](assets/1555485058132.png)



![1555485093085](assets/1555485093085.png)



按下方向键选择OK回车即可

![1555496062646](assets/1555496062646.png)



完成后运行更新命令：

```
sudo apt-get update
```

![1555496477552](assets/1555496477552.png)



安装mysql

```
sudo apt-get install mysql-server
```

![1555496520217](assets/1555496520217.png)



设置root账号的登录密码：

![1555485497312](assets/1555485497312.png)

![1555496622098](assets/1555496622098.png)



经过上面操作，就完成了数据库的安装和配置。

![1555496747740](assets/1555496747740.png)



### navicat

从网盘上面下载navicat破解版压缩包到ubuntu

```bash
链接: https://pan.baidu.com/s/1VcrFp3dNgdiyGo4TFT6Wiw 
提取码: 39yt
```

![1555558869882](assets/1555558869882.png)



双击压缩包，并把内部文件拖放到桌面上

![1555558912918](assets/1555558912918.png)



进入navicat目录，在终端打开输入以下命令：

```
./start_navicat
```

![1555558990718](assets/1555558990718.png)



点击安装Mono和Gecko

![1555559056428](assets/1555559056428.png)

![1555559963030](assets/1555559963030.png)



把桌面上解压出来的navicat目录复制到/opt目录下。桌面的删除即可。

```
sudo cp ~/Desktop/navicat120_premium_cs_x64  /opt -r
```

![1555572438424](assets/1555572438424.png)



在`/usr/share/applications`目录下创建navicat的快捷方式文件，执行以下代码：

```bash
cd /usr/share/applications
sudo vim navicat.desktop
```



文件代码如下，`:wq`保存退出。

```bash
[Desktop Entry]
Encoding=UTF-8
Name=navicat
Comment=The Smarter Way to manage dadabase
Exec=/opt/navicat120_premium_cs_x64/start_navicat
Icon=/opt/navicat120_premium_cs_x64/navicat.png
Categories=Application;Database;MySQL;navicat
Version=1.0
Type=Application
Terminal=0
```

![1555572888816](assets/1555572888816.png)



接下来在应用程序中搜索`navicat`并设置到收藏列表中。

![1555573020937](assets/1555573020937.png)



### Postman

从官网下载Postman软件包，官网地址：[https://www.getpostman.com/downloads/](https://www.getpostman.com/downloads/)

![1555580716760](assets/1555580827498.png)



安装Postman运行的依赖包

```bash
sudo apt-get install libgconf-2-4
sudo apt-get install libcanberra-gtk-module
```

![1555581235664](assets/1555581235664.png)

![1555581250971](assets/1555581250971.png)



把下载回来的Postman从`Downloads`目录中解压并剪切到`/opt`目录下

```bash
cd ~/Downloads
sudo tar -zxf Postman-linux-x64-7.0.7.tar.gz
sudo mv Postman /opt
```

![1555582465252](assets/1555582465252.png)



把官方上面的logo图片下载回来，<img src="./assets/postman.svg" width="35">。并保存到软件目录`/opt/Postman`下。

![1555582656833](assets/1555582656833.png)



创建桌面快捷方式，创建快捷方式文件

```bash
sudo vim /usr/share/applications/postman.desktop
```

快捷方式文件代码如下，`:wq` 保存退出。

```bash
[Desktop Entry]
Encoding=UTF-8
Name=postman
Comment=用于接口测试的一个工具
Exec=/opt/Postman/Postman
Icon=/opt/Postman/postman.svg
Categories=Application;Web;MySQL;postman
Version=1.0
Type=Application
Terminal=0
```



在应用程序中搜索`postman`，并设置到收藏夹。

![1555582917726](assets/1555582917726.png)



### git

运行以下命令安装git

```bash
sudo apt-get install git
```

![1555583954368](assets/1555583954368.png)



安装完成了，可以查看下版本。

![1555584388674](assets/1555584388674.png)





### redis

使用以下命令安装redis

```bash
sudo apt-get install redis-server
```

![1555585333786](assets/1555585333786.png)

配置文件地址：`/etc/redis/redis.conf`



### nvm

由于node.js的版本一直处于不断更新中，所以我们需要一个版本管理器来更好的使用node.js。

nvm是一个开源的node版本管理器，通过它，你可以下载任意版本的node.js，还可以在不同版本之间切换使用。

**注意：安装nvm之前，要确保当前机子中不存在任何版本的node，如果有，则卸载掉。**

github：<https://github.com/creationix/nvm>

安装命令：

```bash
sudo apt-get update
sudo apt install curl
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
source ~/.bashrc
```

![1555898548578](assets/1555898548578.png)

![1555898571439](assets/1555898571439.png)



### node

使用nvm的相关命令安装node。

```python
# 查看官方提供的可安装node版本
nvm ls-remote

# 安装执行版本的node,例如：nvm install v10.15.2
nvm install <version>

# 卸载node版本，例如：nvm uninstall v10.15.2
nvm uninstall <version>

# 查看已安装的node列表
nvm ls

# 切换node版本，例如：nvm use v10.15.2
nvm use <version>

# 设置默认版本，如果没有设置，则开机时默认node是没有启动的。
nvm alias default v10.15.2

# 查看当前使用的版本
nvm current
```

![1555900488599](assets/1555900488599.png)

安装几个常用的LTS版本

```
nvm install v10.15.2
nvm alias default v10.15.2
```



![1555900526360](assets/1555900526360.png)



### npm

npm（node package manager）是nodejs的包管理器，用于node插件管理（包括安装、卸载、管理依赖等）。安装了node以后，就自动安装了npm[不一定是最新版本]

官方：[https://www.npmjs.com](https://www.npmjs.com/)

文档：[https://www.npmjs.com.cn/](https://www.npmjs.com.cn/)

```
npm --version
```





### cnpm

默认情况下，npm安装插件是从国外服务器下载，受网络影响大，可能出现网络异常。

通过淘宝镜像加速npm

[http://npm.taobao.org/](http://npm.taobao.org/)

```bash
# 打印默认的 registry 地址
npm config -g get registry

# 设置淘宝镜像
npm config -g set registry https://registry.npm.taobao.org
```

![1555910269500](assets/1555910269500.png)



### vue-cli

使用前面已经安装好的node版本，进行安装。注意一旦安装以后，以后这个vue-li最好契合当前node版本。也就是说，运行接下来安装的vue-cli时，最好运行的就是本次跑的node版本。如果回头切换到其他版本node来运行vue-cli，有可能因为版本不兼容出现不必要的bug。

文档：[https://cli.vuejs.org/zh/guide/installation.html](https://cli.vuejs.org/zh/guide/installation.html)

安装命令

```bash
npm install -g @vue/cli
npm install -g @vue/cli-init  # vue2.x版本需要安装桥接工具

# 安装完成可以查看版本
vue -V

# 搭建项目
# vue2.x
vue init webpack <项目目录名>

# vue3.x
vue create <项目目录名>
```

![1555908358615](assets/1555908358615.png)

![1555910720836](assets/1555910720836.png)



### nginx

安装命令：

```bash
sudo apt-get install nginx
```

![1555929756938](assets/1555929756938.png)



安装好的文件位置：

```cmd
/usr/sbin/nginx # 主程序目录

/etc/nginx # 存放配置文件目录

/usr/share/nginx # 存放静态文件目录

/etc/nginx/sites-available # 默认站点配置文件

/var/log/nginx # 存放日志目录

/var/www/html  # 默认站点根目录
```



相关操作

```bash
# 首次启动nginx服务器
sudo /usr/sbin/nginx

# 停止nginx服务器
sudo /usr/sbin/nginx -s stop

# 重启nginx
sudo /usr/sbin/nginx -s reload
```



### Docker

更新ubuntu的apt源,上面如果执行过可以忽略

```bash
sudo apt-get update
```

安装包允许apt通过HTTPS使用仓库

```bash
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```

![1559067730172](.\assets\1559067730172.png)



添加Docker官方GPG key，网络不好的话，会报错，多执行几次即可。

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

设置Docker稳定版仓库，网络不好的话，会报错，多执行几次即可。

```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

添加Docker仓库后，更新apt源索引,注意，这里更新的源是关于docker的。

```bash
sudo apt-get update
```

![1559068011503](assets\1559068011503.png)



安装最新版Docker CE（社区版）

```bash
sudo apt-get install docker-ce
```

![1559068087606](assets\1559068087606.png)



检查Docker CE是否安装正确,hello-world是一个打印字符串的测试镜像，docker会自动下载

```bash
sudo docker run hello-world
```

![1559068107255](assets\1559068107255.png)



### MongoDB

```bash
sudo apt-get install mongodb
```

![1559071678964](assets\1559071678964.png)

安装完成以后，mongodb是默认开机自启的。可以通过**mongdo**进入mongodb的控制台验证是否安装成功了。

```bash
mongo
```



启动和关闭mongodb命令

```
service mongodb start
service mongodb stop
```



### Golang

Github地址：https://github.com/golang/go

Golang官方网站：https://golang.org/

Golang中文官网：https://golang.google.cn/dl/

Golang安装包下载地址：https://dl.google.com/go/go1.12.5.linux-amd64.tar.gz



注意：apt-get也可以安装Golang，但是安装的版本相对较低，因为Golang本身更新速度问题，所以我们使用手动下载安装包的方式来完成安装。

![1559991495887](assets/1559991495887.png)



下载压缩包`go1.12.1.linux-amd64.tar.gz`，解压到`/usr/local/`目录下[这个目录是官方推荐的]。

```shell
cd ~/Downloads
wget https://dl.google.com/go/go1.12.5.linux-amd64.tar.gz
sudo tar -xzf go1.12.5.linux-amd64.tar.gz -C /usr/local
```

![1559993384933](assets/1559993384933.png)



直接在终端运行Golang执行文件，检查版本，看是否能正常使用。

```shell
/usr/local/go/bin/go version
```

效果如下，证明安装成功。

![1559993708840](assets/1559993708840.png)



接下来，在`~/.bashrc`文件中配置Golang相关的环境变量。

```shell
vim  ~/.bashrc
```

在文件末尾追加如下内容，`:wq`保存退出

```shell
export GOROOT=/usr/local/go
export PATH=$PATH:$GOROOT/bin
```

![1559994987016](assets/1559994987016.png)



刷新环境变量

```shell
source ~/.bashrc
```

![1559995017833](assets/1559995017833.png)



再使用`go version`检测环境变量是否生效。

![1559995062084](assets/1559995062084.png)



开发时，很多工具代码不会全部都是由我们自己编写，这样的话实在太累了， 所以我们往往需要加载第三方类库代码到项目中调用，所以我们必须配置`$GOPATH`，否则go命令不知道这些第三方代码要安装到什么位置。

`$GOPATH`目录约定有三个子目录，在我们配置了`$GOPATH`以后，go命令会在使用的时候自动帮我们生成。

-   `src`目录，存放源代码。
-   `pkg`目录，编译时生成的中间文件。
-   `bin`目录，编译后生成的可执行文件。

打开环境变量文件，进行配置。

```shell
vim  ~/.bashrc
```

把Golang相关配置信息，修改为：

```shell
export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
```

刷新环境变量

```shell
source ~/.bashrc
```



安装一个beego框架来测试一下：

```shell
go get github.com/astaxie/beego
go get github.com/beego/bee
```

![1560023751123](assets/1560023751123.png)

没有报错，我们可以到刚才设置的`$GOPATH`目录下，查看：

![1560024123309](assets/1560024123309.png)

左边是`$GOPATH`目录，右边是`src`目录，里面包含了`beego`框架的三个包。



### Goland

官网下载地址：https://www.jetbrains.com/go/download/#section=linux

![1560027047451](assets/1560027047451.png)



把下载回来的压缩包进行解压。

```shell
cd ~/Downloads
wget https://download.jetbrains.com/go/goland-2019.1.3.tar.gz
tar -zxvf goland-2019.1.3.tar.gz
```

![1560025682569](assets/1560025682569.png)

把解压出来的文件剪切到opt目录下，并切换工作目录到opt，启动goland。

```shell
sudo mv ~/Downloads/GoLand-2019.1.3 /opt
cd /opt/GoLand-2019.1.3/bin
sh goland.sh
```

![1560027163923](assets/1560027163923.png)

参考以下网址进行激活：

http://idea.lanyus.com/

![1560027337315](assets/1560027337315.png)

出现如下窗口，则表示激活成功！

![1560027395430](assets/1560027395430.png)

在`/etc/hosts`下屏蔽网址。

```shell
sudo vim /etc/hosts
```

追加内容：

```shell
0.0.0.0 account.jetbrains.com
0.0.0.0 www.jetbrains.com
```

![1560027576109](assets/1560027576109.png)



创建快捷方式，选择`Tools`，`Create Desktop Entry...`

![1560032506594](assets/1560032506594.png)



给所有用户创建快捷方式。

![1560032582257](assets/1560032582257.png)



在应用程序中搜索`Goland`，并鼠标右键设置到收藏夹。

![1560032672351](assets/1560032672351.png)



### GitLab

GitLab是一个用于仓库管理系统的开源项目，使用Git作为代码管理工具，并在此基础上搭建起来的web服务。

原版是英文的，我们这里安装中文汉化版。

GitLab 官方网站地址：https://gitlab.com/

GitLab 中文社区地址：https://gitlab.com/xhang/gitlab



```
cd ~/Downloads
wget https://gitlab.com/xhang/gitlab/-/archive/10-8-stable-zh/gitlab-10-8-stable-zh.tar.bz2
```



![1560094084889](assets/1560094084889.png)

