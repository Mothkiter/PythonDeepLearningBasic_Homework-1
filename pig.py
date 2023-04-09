# Define a class named Pig
# Define a class named Pig


import requests
from bs4 import BeautifulSoup
import json



class Pig_MA:
    def __init__(self, year, month):
        self.year = int(year)
        self.month = int(month)
        if  month<= 12 and month>=10:
            self.url_MA = 'http://www.moa.gov.cn/ztzl/szcpxx/jdsj/'+str(year)+'/'+str(year)+str(month)+'/'
        elif month<=9 and month>=1:
            self.url_MA = 'http://www.moa.gov.cn/ztzl/szcpxx/jdsj/'+str(year)+'/'+str(year)+'0'+str(month)+'/'
        else:
            raise ValueError("请输入一个真正的月份")  
        response_MA = requests.get(self.url_MA)
        self.bs_MA = BeautifulSoup(response_MA.content,'features="lxml"')
        
    def printInfo_MA(self):
        i = -1
        n = 1
        for table in self.bs_MA.select('table.data_table_mobile.pcNone'):
            for td in table.select('td.right_data'):
                i = i+1
                if i %5==0:
                    print( n,end='. ')
                    n = n+1
                if i %5==1:
                    print( td.text.strip(),end=':')
                if i %5==2:
                    print( td.text.strip(),end='[数值] ')
                if i %5==3:
                    print( td.text.strip(),end='[环比] ')
                if i %5==4:
                    print( td.text.strip(),end='[同比] \n')
        

    

class Pig_ZW:
    def __init__(self, area='全国'):
        self.area = str(area)
        dict = {'全国':'','安徽':'/areapriceinfo-340000.shtml','合肥':'/areapriceinfo-340100.shtml',
                '瑶海区':'/areapriceinfo-340102.shtml','庐阳区':'/areapriceinfo-340103.shtml','蜀山区':'/areapriceinfo-340104.shtml',
                '包河区':'/areapriceinfo-340111.shtml','长丰县':'/areapriceinfo-340121.shtml','肥东县':'/areapriceinfo-340122.shtml',
                '肥西县':'/areapriceinfo-340123.shtml','庐江县':'/areapriceinfo-340124.shtml','巢湖市':'areapriceinfo-340181.shtml'}
        self.url_ZW = 'https://zhujia.zhuwang.cc/areapriceinfo-340181.shtml' + str(dict[area])

        response_ZW = requests.get(self.url_ZW)
        self.bs_ZW = BeautifulSoup(response_ZW.content,"html.parser")

    def todayInfo(self):
        node = self.bs_ZW.find("ul", class_="zhujia-hd clear")
        name = node.select('img')
        data = node.select('b',class_ = "green")
        output = []
        for i in range(len(data)-1):
            print(name[i].get('alt'),end=':')
            print(data[i].contents[0])
            output.append( name[i].get('alt')+':'+str(data[i].contents[0]))

        print('猪粮比',end=':')
        print(data[len(data)-1].contents[0])
        output.append( '猪粮比'+':'+str(data[len(data)-1].contents[0]))

        return(output)


    def countryInfo(self):
        node = self.bs_ZW.find("ul", class_="live-hogs clear")
        name = node.select('li')

        data = node.select('p')
        output = []

        for n in range(len(name)):
            print(data[3*n].contents[0])
            print(data[3*n+1].contents[0],end=':')
            print(data[3*n+2].text.strip())
            output.append( str(data[3*n].contents[0])+' '+str(data[3*n+1].contents[0])+':'+data[3*n+2].text.strip())

        return(output)




class Pig_critic:
    def __init__(self, year,month,day):
        self.day = int(day)
        if  month>=1 and month<=12:
            url_critic = 'https://hqb.nxin.com/nongbo/daily/dailyView-'+str(year)+'-'+str(month)+'.shtml'
        else:
            raise ValueError("请输入一个真正的月份")  
        


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
            # 'Cookie': 'JSESSIONID=224ECDD1D0700CABB6C0A6D7AA38A425; Hm_lvt_93cec007f6c8372841c5c4b4fdc80aa7=1681031994; Hm_lvt_552dc469f41a8cdde31652fba0e1a1ed=1681031994; NX_LOG=73db2ad7b29e421f9adee11fbfa3b93f; historyAreaCookie="10393,10215,100000,"; Hm_lpvt_93cec007f6c8372841c5c4b4fdc80aa7=1681032646; Hm_lpvt_552dc469f41a8cdde31652fba0e1a1ed=1681032646; nxin_stat_ss=VL6CDB1ZBU_5_1681032645682',
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
        self.bs_critic = BeautifulSoup(response.content,"html.parser")

    def crtic(self):
        num = self.bs_critic.find_all('li')
        text = self.bs_critic.find_all('p')
        return({'猪价(元/公斤)':num[3*(self.day-1)].select('span')[0].contents[0],'玉米(元/吨)':num[3*(self.day-1)+1].select('span')[0].contents[0],'猪粮比':num[3*(self.day-1)+2].select('span')[0].contents[0],'评论':text[self.day-1].text})



class Pig_change:
    def __init__(self,id = 1, t=7):
        if id in [1,3,4] and t in [7,30,180,365]:
            url = 'https://hqb.nxin.com/hqb/chq.shtml?type=0&date=0&queryPriceVo.goodsId='+str(id)+'&queryPriceVo.areaId=10393&queryPriceVo.whatTime='+str(t)
        else:
            raise ValueError("对应关系如下；猪肉 id = 1；玉米 id = 3； 豆粕 id = 4。时间t只能取7 30 180 365")  
        
        response_change = requests.get(url)
        self.bs_change = BeautifulSoup(response_change.content,"lxml")

    def changeInfo(self):
        dict_obj = json.loads(self.bs_change.p.text.encode('utf-8-sig'))

        l_name = dict_obj['pig'][0]['date']
        l_num = []

        for i in range(0,len(dict_obj['pig'][0]['date'])):
            if type(dict_obj['pig'][0]['data'][i])==dict:
                l_num.append(dict_obj['pig'][0]['data'][i]['y'])
            else:       
                l_num.append(dict_obj['pig'][0]['data'][i])

        return({'name':l_name,'num':l_num})

