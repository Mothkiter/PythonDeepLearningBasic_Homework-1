from tkinter import simpledialog
import tkinter as tk
import requests
from bs4 import BeautifulSoup
import json


def get_pig_info_1( year=2022, month=1): #data form agriculture minister
    year = int(year)
    month = int(month)
    if month <= 12 and month >= 10:
        url_MA = f'http://www.moa.gov.cn/ztzl/szcpxx/jdsj/{year}/{year}{month}/'
    elif month <= 9 and month >= 1:
        url_MA = f'http://www.moa.gov.cn/ztzl/szcpxx/jdsj/{year}/{year}0{month}/'
    else:
        raise ValueError("请输入一个真正的月份")  
    response_MA = requests.get(url_MA)
    bs_MA = BeautifulSoup(response_MA.content, "lxml")
    
    i = -1
    l_name = []
    l_num = []
    l_1 = []
    l_2 = []
    for table in bs_MA.select('table.data_table_mobile.pcNone'):
        for td in table.select('td.right_data'):
            i = i + 1
            if i % 5 == 1:
                l_name.append(td.text.strip())
            if i % 5 == 2:
                l_num.append(td.text.strip())
            if i % 5 == 3:
                l_1.append(td.text.strip())
            if i % 5 == 4:
                l_2.append(td.text.strip())

    return {'名称': l_name, '数值': l_num, '环比': l_1, '同比': l_2} 


def get_pig_info_2(area='全国'): #datd form a web about pork price
    area = str(area)
    dict = {'全国':'','安徽':'/areapriceinfo-340000.shtml','合肥':'/areapriceinfo-340100.shtml',
            '瑶海区':'/areapriceinfo-340102.shtml','庐阳区':'/areapriceinfo-340103.shtml','蜀山区':'/areapriceinfo-340104.shtml',
            '包河区':'/areapriceinfo-340111.shtml','长丰县':'/areapriceinfo-340121.shtml','肥东县':'/areapriceinfo-340122.shtml',
            '肥西县':'/areapriceinfo-340123.shtml','庐江县':'/areapriceinfo-340124.shtml','巢湖市':'areapriceinfo-340181.shtml'}
    url_ZW = 'https://zhujia.zhuwang.cc/areapriceinfo-340181.shtml' + str(dict[area])

    if area not in dict.keys():
            raise ValueError("请输入以下选项之一：全国，安徽，合肥或者合肥各下属区以及巢湖市")

    response_ZW = requests.get(url_ZW)
    bs_ZW = BeautifulSoup(response_ZW.content,"html.parser")

    def info_1():
        node = bs_ZW.find("ul", class_="zhujia-hd clear")
        name = node.select('img')
        data = node.select('b',class_ = "green")
        l_name = []
        l_num = []
        for i in range(len(data)-1):
            l_name.append(name[i].get('alt'))
            l_num.append(str(data[i].contents[0]))

        l_name.append('猪粮比')
        l_num.append(data[len(data)-1].contents[0])
        return({'项目':l_name,'数据':l_num})


    def info_2():
        node = bs_ZW.find("ul", class_="live-hogs clear")
        name = node.select('li')

        data = node.select('p')
        l_time = []
        l_name = []
        l_num = []

        for n in range(len(name)):
            l_time.append(data[3*n].contents[0])
            l_name.append(data[3*n+1].contents[0])
            l_num.append(data[3*n+2].text.strip())

        return({'日期':l_time,'项目':l_name,'数据':l_num})

    return info_1(),info_2()


def get_pig_crtic(year, month, day): #get critic about price
    day = int(day)
    if int(month) < 1 or int(month) > 12:
        raise ValueError("请输入一个真正的月份")

    url_critic = f"https://hqb.nxin.com/nongbo/daily/dailyView-{year}-{month}.shtml"

    cookies = {
        'JSESSIONID': '224ECDD1D0700CABB6C0A6D7AA38A425',
        'Hm_lvt_93cec007f6c8372841c5c4b4fdc80aa7': '1681031994',
        'Hm_lvt_552dc469f41a8cdde31652fba0e1a1ed': '1681031994',
        'NX_LOG': '73db2ad7b29e421f9adee11fbfa3b93f',
        'historyAreaCookie': '"10393,10215,100000,"',
        'Hm_lpvt_93cec007f6c8372841c5c4b4fdc80aa7': '1681032646',
        'Hm_lpvt_552dc469f41a8cdde31652fba0e1a1ed': '1681032646',
        'nxin_stat_ss': 'VL6CDB1ZBU_5_1681032645682',
    }

    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'https://hqb.nxin.com/nongbo/daily.shtml',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(url_critic, cookies=cookies, headers=headers)
    bs_critic = BeautifulSoup(response.content, "html.parser")

    text = bs_critic.find_all('p')
    return {
        '评论': text[day-1].text
    }


def get_pig_info_change(id=1, t=7): #获得猪肉以及饲料价格走势图
    if int(id) in [1,3,4] :
        url = 'https://hqb.nxin.com/hqb/chq.shtml?type=0&date=0&queryPriceVo.goodsId='+str(id)+'&queryPriceVo.areaId=10393&queryPriceVo.whatTime='+str(365)
    else:
        raise ValueError("对应关系如下；猪肉 id = 1；玉米 id = 3； 豆粕 id = 4。时间t范围直到去年年初")  
    
    t = int(t)

    response_change = requests.get(url)
    bs_change = BeautifulSoup(response_change.content,"lxml")

    dict_obj = json.loads(bs_change.p.text.encode('utf-8-sig'))

    l_num = []
    l_name = []
    
    num = len(dict_obj['pig'][0]['data1'])
    if t<=num:
        l_name = dict_obj['pig'][0]['date'][num-t:num]
        for i in range(num-t,num):
            if type(dict_obj['pig'][0]['data1'][i])==dict:
                l_num.append(dict_obj['pig'][0]['data1'][i]['y'])
            else:       
                l_num.append(dict_obj['pig'][0]['data1'][i])

    else:
        l_name = dict_obj['pig'][0]['date'][num+365-t:365]+dict_obj['pig'][0]['date'][0:num]
        for i in range(num+365-t,365):
            if type(dict_obj['pig'][0]['data2'][i])==dict:
                l_num.append(dict_obj['pig'][0]['data2'][i]['y'])
            else:       
                l_num.append(dict_obj['pig'][0]['data2'][i])
        for i in range(0,num):
            if type(dict_obj['pig'][0]['data1'][i])==dict:
                l_num.append(dict_obj['pig'][0]['data1'][i]['y'])
            else:       
                l_num.append(dict_obj['pig'][0]['data1'][i])

    return {'name':l_name,'num':l_num,'id':id,'t':t}

# 运行应用程序
class MyApp_main:
    def __init__(self):
        self.app = tk.Tk()#create the beginning page

        #set title
        self.title = tk.Label(self.app, text='( ￣(00)￣ ) 哼~', font=('Arial', 20))
        self.title.pack(fill='both', expand=True, padx=50, pady=50)

        # create 4 button for 4 kinds of data
        self.button1 = tk.Button(self.app, text='查询农业部数据', command=lambda: self.show_data_1())
        self.button2 = tk.Button(self.app, text='查询全国，安徽或者合肥各地区今日数据', command=lambda: self.show_data_2())
        self.button3 = tk.Button(self.app, text='查看猪价评论', command=lambda: self.show_data_3())
        self.button4 = tk.Button(self.app, text='获得价格走势图', command=lambda: self.show_data_4())

        self.button1.pack(fill='both', expand=True, padx=50, pady=50)
        self.button2.pack(fill='both', expand=True, padx=50, pady=50)
        self.button3.pack(fill='both', expand=True, padx=50, pady=50)
        self.button4.pack(fill='both', expand=True, padx=50, pady=50)

        self.dict = {}
        self.dict2 = {}#avaliable when show the second kinds of data
        

    def show_data_1(self):
        #get input
        input_str = simpledialog.askstring('Input','输入：年份,月份')
        if input_str:
            input_list = input_str.split(',')
            if len(input_list) == 1:
                input_list = l=input_list[0].split(' ')
            self.dict = get_pig_info_1(*input_list)
        new_window = tk.Toplevel()
        # create a table with dict
        for key in self.dict:
            name = key
            break
        row_text = ''
        for key in self.dict:
            row_text += key + ' '
            tk.Label(new_window, text=key).grid(row=0, column=list(self.dict.keys()).index(key))
        for n in range(len(self.dict[name])):
            row_text = ''
            for key in self.dict:
                row_text += str(self.dict[key][n]) + ' '
                tk.Label(new_window, text=str(self.dict[key][n])).grid(row=n+1, column=list(self.dict.keys()).index(key))

        self.dict = {}


    def show_data_2(self):
        input_str = simpledialog.askstring('Input','请输入:以下选项之一：全国，安徽，合肥或者合肥各下属区以及巢湖市')
        if input_str:
            input_list = input_str.split(',')
            if len(input_list) == 1:
                input_list = l=input_list[0].split(' ')
            self.dict,self.dict2 = get_pig_info_2(*input_list)
        new_window = tk.Toplevel()

        # create a table with dict
        for key in self.dict:
            name = key
            break
        row_text = ''
        for key in self.dict:
            row_text += key + ' '
            tk.Label(new_window, text=key).grid(row=0, column=list(self.dict.keys()).index(key))
        for n in range(len(self.dict[name])):
            row_text = ''
            for key in self.dict:
                row_text += str(self.dict[key][n]) + '  '
                tk.Label(new_window, text=str(self.dict[key][n])).grid(row=n+1, column=list(self.dict.keys()).index(key))
        tk.Label(new_window, text='').grid(row=len(self.dict[name])+1, column=0)

        # create a table with dict2
        for key in self.dict2:
            name2 = key
            break
        row_text = ''
        for key in self.dict2:
            row_text += key + ' '
            tk.Label(new_window, text=key).grid(row=len(self.dict[name])+3, column=list(self.dict2.keys()).index(key))
        for n in range(len(self.dict2[name2])):
            row_text = ''
            for key in self.dict2:
                row_text += str(self.dict2[key][n]) + '  '
                tk.Label(new_window, text=str(self.dict2[key][n])).grid(row=len(self.dict[name])+n+4, column=list(self.dict2.keys()).index(key))

        self.dict = {}
        self.dict2 = {}



    def show_data_3(self):
        input_str = simpledialog.askstring('Input','输入：年份,月份,日')
        if input_str:
            input_list = input_str.split(',')
            if len(input_list) == 1:
                input_list = l=input_list[0].split(' ')
            self.dict = get_pig_crtic(*input_list)
        new_window = tk.Toplevel()
        # show the critic
        for key in self.dict:
            name = key
            break
        text_label = tk.Label(new_window, text=self.dict[name], font=('Arial', 13), wraplength=900, pady=5)
        text_label.pack()

        self.dict = {}


    def show_data_4(self):
        input_str = simpledialog.askstring('Input','输入：id,时间尺度(天)；对应关系如下；猪肉 id = 1；玉米 id = 3； 豆粕 id = 4。时间只到去年年初')
        if input_str:
            input_list = input_str.split(',')
            if len(input_list) == 1:
                input_list = l=input_list[0].split(' ')
            self.dict = get_pig_info_change(*input_list)
        new_window = tk.Toplevel()
        # draw a pic to show the change of price
        canvas = tk.Canvas(new_window, width=1020, height=520)
        canvas.pack()
        data = self.dict['num']
        day = self.dict['name']
        #set name and unit
        if int(self.dict['id']) == 1:
            unit = '元/公斤'
            name = '猪肉'
        elif int(self.dict['id']) == 3:
            unit = '元/吨'
            name = '玉米'
        else:
            unit = '元/吨'
            name = '豆粕'
        
        max_value = max(data)
        min_value = min(data)
        x_scale = 950 / len(data)
        y_scale = 450 / (max_value - min_value)

        points = []
        if int(self.dict['t'])<15:#if less than 30 data every point will be shown
            for i in range(len(data)):
                x = i * x_scale + 25
                y = (max_value - data[i]) * y_scale + 45
                points.append((x, y))
                canvas.create_text(x, y+1, text='*',fill='red')
                canvas.create_text(x+10, y-15, text=str(data[i]))
                canvas.create_text(x, 510, text=day[i])                    
            for i in range(len(points) - 1):
                canvas.create_line(points[i], points[i+1])
        else:#if more than 20 data every point will be shown
            n = int(len(data)/15)
            for i in range(len(data)):
                x = i * x_scale + 25
                y = (max_value - data[i]) * y_scale + 45
                points.append((x, y))
                if i%n==0:
                    canvas.create_text(x, y+1, text='*',fill='red')
                    canvas.create_text(x+10, y-15, text=str(data[i]))
                    canvas.create_text(x, 510, text=day[i],font=('Arial', 8))
            for i in range(len(points) - 1):
                canvas.create_line(points[i], points[i+1])

        canvas.create_text(500, 10, text=name+'价格走势图(单位：'+unit+')')
        canvas.create_text(750, 20, text='最大值：'+str(max_value),font=('Arial', 15))
        canvas.create_text(750, 40, text='最小值：'+str(min_value),font=('Arial', 15))

        canvas.create_line(25, 25, 25, 500, width=2)  # y-axis
        canvas.create_line(25, 500, 1000, 500, width=2)  # x-axis

        self.dict = {}


    def run(self):
        self.app.mainloop()
        return(self.dict)





