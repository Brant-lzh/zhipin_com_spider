import time
class Action():
    def __init__(self,device):
        self.d = device
        self.Width = device.info.get("displayWidth")
        self.Height = device.info.get("displayHeight")

    def getDevice(self):
        return self.d
    # 向上翻页
    def ToUp(self):
        self.d(scrollable=True).scroll.vert.forward()

    # 向右翻页
    def ToRight(self):
        self.d.swipe(self.Width * 0.93, self.Width * 0.93, self.Height * 0.05, self.Height * 0.56)

    # 点击
    def ToClick(self):
        self.d.click(self.Width * 0.45, self.Height * 0.18)


    # 找不到就循环向上滑动
    def whileToUp(self, resourceId):
        while (not self.d(className="android.widget.TextView", resourceId=resourceId).exists(2)):
            self.ToUp()


    def init(self,keyword):
        self.d(text="BOSS直聘").click()
        time.sleep(5)
        self.d.click(self.Width * 0.9, self.Height * 0.08)
        et_search = self.d(resourceId="com.hpbr.bosszhipin:id/et_search")
        if et_search.exists(5):
            et_search.set_text(keyword)
        else:
            return "爬虫搜索出现错误"
        self.d.click(self.Width * 0.93, self.Height * 0.95)
        time.sleep(2)
        self.d.click(self.Width * 0.5, self.Height * 0.28)