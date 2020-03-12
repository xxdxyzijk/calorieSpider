import csv
import requests
from bs4 import BeautifulSoup


class CalorieSpider:
    def __init__(self):
        self.calorie_url = 'http://www.**.com/index.htm#1'
        self.csv_title = [
            'id',
            'Groups',
            'GroupsId',
            'shoummName',
            'calorie',
            'edible']
        self.food_line = ['豆腐脑', '面西胡瓜', '白兰瓜', '鸡血', '鸭蛋白', '海参(水浸)', '果味奶', '胡麻油', '豆汁(生)',
                          '蜂蜜', '北京6度特制啤酒', '猴头菇(罐装)']
        self.food_id = 1
        self.food_sort = ['五谷类,豆类的食物热量表', '蔬菜类的食物热量表', '水果类的食物热量表', '肉类的食物热量表',
                          '蛋类的食物热量表', '水产类的食物热量表', '奶类的食物热量表', '油脂类的食物热量表', '糕点小吃的食物热量表',
                          '糖类的食物热量表', '饮料类的食物热量表', '茵藻类的食物热量表', '其它食品的食物热量表']
        self.id_sort = 1
        # 样式不统一，造成基围虾后面丢失金线鱼名称，故补充
        self.defect_pre = '基围虾'
        self.defect_food = '金线鱼'
        self.file = open(r'calorieData.csv', 'a', newline='', encoding='utf-8')
        self.file_write = csv.writer(self.file)

    def get_html(self):
        html = requests.get(self.calorie_url).text
        html_text = html.encode(
            'ISO-8859-1').decode(requests.utils.get_encodings_from_content(html)[0])
        return html_text

    def use_bs4_analysis(self, html):
        html_soup = BeautifulSoup(html, "html.parser")
        a_list = html_soup.find_all('tr')
        a_td = a_list[0].td
        a_div = a_td.find_all('div', attrs={'align': 'center'})[2:]
        name_dict = []
        num_dict = []
        for i in a_div:
            name_font = i.find_all('font', attrs={'color': '#000000'})
            num_font = i.find_all('font', attrs={'color': '#cc0099'})
            # 除杂
            for name_info in name_font:
                if '食品名称' in str(name_info) or '减肥' in str(name_info):
                    pass
                else:
                    name_str = \
                        str(name_info).split('<font color="#000000" style="font-size: 14px">')[1].split('</font>')[
                            0].replace(' ', '').replace('\r', '').replace('\n', '')
                    name_array = name_str.split('<br/>')
                    name_dict.extend(name_array)

            for num_info in num_font:
                num_str = str(num_info).split('<font color="#cc0099" style="font-size: 14px">')[1].split('</font>')[
                    0].replace(
                    ' ', '').replace('\r', '').replace('\n', '')
                num_array = num_str.split('<br/>')
                num_dict.extend(num_array)

        new_num_list = []
        for i in num_dict:
            if i and i != '　' and i != ' ':
                new_num_list.append(i)

        new_name_list = []
        for k in name_dict:
            if k and k != '　' and k != ' ':
                new_name_list.append(k)
                # 样式不统一，造成基围虾后面丢失金线鱼名称，故补充
                if k == self.defect_pre:
                    new_name_list.append(self.defect_food)

        for n in range(885):
            self.save_csv_content([self.food_id, self.food_sort[0], self.id_sort, new_name_list[n],
                                   new_num_list[n].split('/')[0], new_num_list[n].split('/')[1]])
            self.food_id += 1
            if new_name_list[n] == self.food_line[0]:
                self.id_sort += 1
                if len(self.food_sort):
                    del self.food_sort[0]
                if len(self.food_line) > 1:
                    del self.food_line[0]

    def save_csv_title(self):
        self.file_write.writerow(self.csv_title)

    def save_csv_content(self, data):
        self.file_write.writerow(data)

    def run_spider(self):
        self.save_csv_title()
        html_text = self.get_html()
        self.use_bs4_analysis(html_text)


if __name__ == '__main__':
    spider = CalorieSpider()
    spider.run_spider()
