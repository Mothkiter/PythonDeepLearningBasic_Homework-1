# Define a class named Pig
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog
import tkinter as tk
import requests
from bs4 import BeautifulSoup
import json



def get_pig_info_1( year=2022, month=1): #农业部数据
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

    


def get_pig_info_2(area='全国'): #猪价网数据
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
        return({'name':l_name,'num':l_num})


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

        return({'time':l_time,'name':l_name,'num':l_num})

    return info_1(),info_2()






def get_pig_crtic(year, month, day): #获得猪价评论
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
    if int(id) in [1,3,4] and int(t) in [7,30,180,365]:
        url = 'https://hqb.nxin.com/hqb/chq.shtml?type=0&date=0&queryPriceVo.goodsId='+str(id)+'&queryPriceVo.areaId=10393&queryPriceVo.whatTime='+str(t)
    else:
        raise ValueError("对应关系如下；猪肉 id = 1；玉米 id = 3； 豆粕 id = 4。时间t只能取7 30 180 365")  
    
    response_change = requests.get(url)
    bs_change = BeautifulSoup(response_change.content,"lxml")

    dict_obj = json.loads(bs_change.p.text.encode('utf-8-sig'))

    l_name = dict_obj['pig'][0]['date']
    l_num = []

    for i in range(0,len(dict_obj['pig'][0]['date'])):
        if type(dict_obj['pig'][0]['data'][i])==dict:
            l_num.append(dict_obj['pig'][0]['data'][i]['y'])
        else:       
            l_num.append(dict_obj['pig'][0]['data'][i])

    return {'name':l_name,'num':l_num}





# 运行应用程序
class MyApp_main:
    def __init__(self):
        self.app = tk.Tk()

        # create button
        self.button1 = tk.Button(self.app, text='1', command=lambda: self.set_value(1))
        self.button2 = tk.Button(self.app, text='2', command=lambda: self.set_value(2))
        self.button3 = tk.Button(self.app, text='3', command=lambda: self.set_value(3))
        self.button4 = tk.Button(self.app, text='4', command=lambda: self.set_value(4))

        # show button
        self.button1.pack(fill='both', expand=True, padx=50, pady=50)
        self.button2.pack(fill='both', expand=True, padx=50, pady=50)
        self.button3.pack(fill='both', expand=True, padx=50, pady=50)
        self.button4.pack(fill='both', expand=True, padx=50, pady=50)

        self.i = 0
        self.dict = {}
        self.dict2 = {}
        

    # 创建一个函数，用于设置元素i的值
    def set_value(self, value):
        self.i = value
        if self.i==1: 
            input_str = simpledialog.askstring('Input','输入：年份,月份')
  
            if input_str:
                
                input_list = input_str.split(',')
               
            self.dict = get_pig_info_1(*input_list)

        elif self.i==2: 
            input_str = simpledialog.askstring('Input','请输入:以下选项之一：全国，安徽，合肥或者合肥各下属区以及巢湖市')
  
            if input_str:
                
                input_list = input_str.split(',')
               
            self.dict,self.dict2 = get_pig_info_2(*input_list)

        elif self.i==3: 
            input_str = simpledialog.askstring('Input','输入：年份,月份,日')

            if input_str:
                
                input_list = input_str.split(',')
                if len(input_list) == 1:
                    input_list = l=input_list[0].split('，')

                
            self.dict = get_pig_crtic(*input_list)
        
        

        else :
            input_str = simpledialog.askstring('Input','输入：id,时间尺度；对应关系如下；猪肉 id = 1；玉米 id = 3； 豆粕 id = 4。时间t只能取7 30 180 365')

            if input_str:
                input_list = input_str.split(',')
                if len(input_list) == 1:
                    input_list = l=input_list[0].split('，')

                
            self.dict = get_pig_info_change(*input_list)

        
        new_window = tk.Toplevel()

        # create a table with dict
        if self.i ==3:

            for key in self.dict:
                name = key
                break

            text_label = tk.Label(new_window, text=self.dict[name])

            # # display the label on the page
            text_label.pack()


        elif self.i == 2:
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

        else:
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

        # for n in range(len(self.dict[name])):
        #     row_text = ''
        #     for key in self.dict:
        #         row_text += str(self.dict[key][n]) + ' '
        #         tk.Label(new_window, text=str(self.dict[key][n])).grid(row=n, column=list(self.dict.keys()).index(key))
        # if self.i == 4:
        #     key =list(self.dict.keys())
        #     fig, ax = plt.subplots()
        #     ax.plot(self.dict[key[0]], self.dict[key[1]])
        #     ax.set_xlabel(key[0])
        #     ax.set_ylabel(key[1])
        #     ax.set_title('Plot of {} vs {}'.format(key[0], key[1]))

        #     # display the plot on the page
        #     canvas = FigureCanvasTkAgg(fig, master=new_window)
        #     canvas.draw()
        #     canvas.get_tk_widget().pack()




    def run(self):
        self.app.mainloop()
        return(self.i,self.dict)


