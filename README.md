汽车之家网站的汽车图片抓去

https://car.autohome.com.cn/pic/index.html


项目启动文件：start.py

```
Master端：

redis-cli > lpush carpic:start_urls https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=2%20&brandId=0%20&fctId=0%20&seriesId=0

```

--------------------------------------------------------------------------------------------

ProxyPool 来源于静觅大神

删除了从公开网站收集ip的代码，我的ip代理购买于讯代理，通过修改crawler.py和setting.py文件，实现ip代理。

如果要使用，请先修改好迅代理的接口，crawler.py和setting文件。
