# encoding=utf8
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver

# 前台开启浏览器模式
def openChrome():
    try:
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        driver = webdriver.Chrome(chrome_options=option)
        # driver.maximize_window()  # 最大化浏览器
        return driver
    except:
        print("有错误发生，驱动程序缺失或浏览器版本不匹配，或环境变量未配置")
        time.sleep(5)
        exit()

def Open_w(w_num):
    base_url = "http://finance.eastmoney.com/a/cdfsd_{page}.html"
    num = 1  # 文章计数
    page = 1  # 页数计数
    articles = []
    for i in range(1, w_num+1):
        url = base_url.format(page=i)
        try:
            driver.get(url)
            # lxml解析器 速度快 文档纠错能力强 需要安装C语言库
            time.sleep(2)  # 缓冲
            titles = BeautifulSoup(driver.page_source, 'lxml').find_all('div', {'class': 'text'})
            if titles:
                print("||||||------------第{0}页爬取内容已获得------------||||||".format(page))
                for title in titles:
                    id = num
                    new_title = title.find('a').get_text().replace(' ', '').strip('\n')
                    new_summ = title.find('p', {'class': 'info'}).get_text().replace(' ', '').strip('\n')
                    new_time = title.find('p', {'class': 'time'}).get_text().replace(' ', '').strip('\n')
                    articles.append([id, new_title, new_summ, new_time])
                    num = num + 1
                print("||||||------------第{0}页爬取完毕！！！------------||||||".format(page))
                page = page + 1
            else:
                print("请检查网页结构是否发生变化")
                time.sleep(5)
                exit()
        except:
            print("请更换ip或增加代理池，预防黑名单")
            time.sleep(5)
            exit()
    save_data(articles)

def save_data(articles):
    try:
        with open('save.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['文章id', '文章标题', '文章摘要', '发表时间'])
            try:
                for row in articles:
                    writer.writerow(row)
                print("保存完毕！！！随时停止")
            except ValueError:
                print("文件写入发生异常，请检查数据！！！")
                time.sleep(5)
                exit()
    except IOError:
        print("文件发生异常，请检查文件！！！")
        f.close()
        time.sleep(5)
        exit()

if __name__ == '__main__':
    w_num = int(input("请输入爬取页面数量: "))
    driver = openChrome()
    while 1:
        result = EC.alert_is_present()(driver)
        if result:
            print("alert 存在弹窗，处理后再试验")
        else:
            print("alert 未弹出！")
            break
    Open_w(w_num)
    # content = driver.page_source.encode('utf-8')
    confirm = input("数据已成功爬取并存储，是否查看？Y（查看文件）|N（关闭进程）：")
    if confirm == 'Y' or confirm == 'y':
        import os
        os.system("start save.csv")
        driver.close()
    else:
        driver.close()