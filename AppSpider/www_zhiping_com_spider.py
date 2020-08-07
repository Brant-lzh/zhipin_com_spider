import uiautomator2 as us2
from AppSpider.mongodb_client import Mongo
import time
from AppSpider.action import Action

#拼接字符串
def SplitString(resourceId):
    return "//android.widget.TextView[@resource-id ='{}']".format(resourceId)

#爬取
def spider(action):
    result = {}

    d = action.getDevice()
    #工资
    result['salary'] = d.xpath(SplitString('com.hpbr.bosszhipin:id/tv_job_salary')).get_text()

    #工作地点
    result['location'] = d.xpath(SplitString('com.hpbr.bosszhipin:id/tv_required_location')).get_text()

    #工作经验
    result['work_exp'] = d.xpath(SplitString('com.hpbr.bosszhipin:id/tv_required_work_exp')).get_text()

    #学历
    result['degree'] = d.xpath(SplitString('com.hpbr.bosszhipin:id/tv_required_degree')).get_text()

    #职位名称
    result['job_name'] = d.xpath(SplitString('com.hpbr.bosszhipin:id/tv_job_name')).get_text()

    #职位标签
    xpath_tags = d(className="android.view.ViewGroup", resourceId="com.hpbr.bosszhipin:id/flexboxLayout")
    tag_list = []
    index = 0
    while (True):
        try:
            tag = xpath_tags.child(index=str(index), className="android.widget.TextView").get_text(2)
        except:
            break
        tag_list.append(tag)
        index = index + 1
    result['tag_list'] = tag_list

    action.whileToUp("com.hpbr.bosszhipin:id/tv_description")
    #职位描述
    description =d.xpath(SplitString('com.hpbr.bosszhipin:id/tv_description')).get_text()
    if "查看全部" in description:
        action.ToUp()
        time.sleep(1)
        action.ToClick()
        description = d.xpath(SplitString('com.hpbr.bosszhipin:id/tv_description')).get_text()
    result['description'] = description

    action.whileToUp("com.hpbr.bosszhipin:id/tv_com_name")
    #公司名称
    result['com_name'] = d.xpath(SplitString('com.hpbr.bosszhipin:id/tv_com_name')).get_text()

    action.whileToUp("com.hpbr.bosszhipin:id/tv_com_info")
    #公司规模
    result['com_info'] = d.xpath(SplitString('com.hpbr.bosszhipin:id/tv_com_info')).get_text()

    action.whileToUp("com.hpbr.bosszhipin:id/tv_location")
    #公司位置
    result['tv_location'] = d.xpath(SplitString('com.hpbr.bosszhipin:id/tv_location')).get_text()

    return result

def start():
    keyword = input("请输入爬取的关键词：")
    client = "mongodb://localhost:27017/"
    db = "spider_data"
    col = keyword
    mongo = Mongo(client, db, col)
    device = us2.connect()
    action = Action(device)
    action.init(keyword)
    num = 1
    while(True):
        try:
            result = spider(action)
        except:
            break
        mongo.insert_one(result)
        print("已爬取到：{}条数据".format(str(num)))
        num += 1
        time.sleep(2)
        action.ToRight()
        time.sleep(1)
    print("爬虫终止，共爬取"+str(num)+"条数据！！！")

if __name__ == "__main__":
    start()
