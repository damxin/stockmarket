# -*- coding:utf-8 -*-
'''
Created on 2019/09/13
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import os


class AlbumCover():

    def __init__(self):
        self.init_url = "https://music.163.com/#/artist/album?id=101988&limit=120&offset=0"  # 请求网址
        self.folder_path = "F:\\nfx\Python\\testcrawler\pic"  # 想要存放的文件目录

    def save_img(self, url, file_name):  ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name, '图片保存成功！')
        f.close()

    def request(self, url):  # 封装的requests 请求
        r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False

    def get_files(self, path):  # 获取文件夹中的文件名称列表
        pic_names = os.listdir(path)
        return pic_names

    def spider(self):
        print("Start!")

        '''
        webdriver.PhantomJS() 这段代码会报
        UserWarning: Selenium support for PhantomJS has been deprecated, please use headless versions of Chrome or Firefox instead
  warnings.warn('Selenium support for PhantomJS has been deprecated, please use headless '。
  但是最终结果还是能跑的出来
        '''
        # driver = webdriver.PhantomJS()
        # driver.get(self.init_url)
        # driver.switch_to.frame("g_iframe")
        # html = driver.page_source

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)  # headless访问
        driver.implicitly_wait(10)  # 等待十秒加载不出来就会抛出异常，10秒内加载出来正常返回
        driver.get(self.init_url)
        driver.switch_to.frame("g_iframe")  # 切换到g_iframe框架
        html = driver.page_source
        driver.close()

        self.mkdir(self.folder_path)  # 创建文件夹
        print('开始切换文件夹')
        os.chdir(self.folder_path)  # 切换路径至上面创建的文件夹

        file_names = self.get_files(self.folder_path)  # 获取文件夹中的所有文件名，类型是list

        all_li = BeautifulSoup(html, 'lxml').find(id='m-song-module').find_all('li')
        # print(type(all_li))

        for li in all_li:
            album_img = li.find('img')['src']
            album_name = li.find('p', class_='dec')['title']
            album_date = li.find('span', class_='s-fc3').get_text()
            end_pos = album_img.index('?')
            album_img_url = album_img[:end_pos]

            photo_name = album_date + ' - ' + album_name.replace('/', '').replace(':', ',') + '.jpg'
            print(album_img_url, photo_name)

            if photo_name in file_names:
                print('图片已经存在，不再重新下载')
            else:
                self.save_img(album_img_url, photo_name)
        print("图片下载结束")


if __name__ == "__main__":
    # https://www.cnblogs.com/Albert-Lee/p/6276847.html
    album_cover = AlbumCover()
    album_cover.spider()
