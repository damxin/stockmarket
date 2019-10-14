# -*- coding:utf-8 -*-
'''
Created on 2019/09/13
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''
from selenium import webdriver  # 导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  # 导入Keys


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


if __name__ == "__main__":
    driver = webdriver.Chrome()
    # m-song-module > li:nth-child(1) > div > img
    all_li = BeautifulSoup(html, 'lxml').find(id='m-song-module').find_all('li')
    for li in all_li:
        album_img = li.find('img')['src']
        album_name = li.find('p', class_='dec')['title']
        album_date = li.find('span', class_='s-fc3').get_text()
        end_pos = album_img.index('?')  # 找到问号的位置
        album_img_url = album_img[:end_pos]  # 截取问号之前的内容
        photo_name = album_date + ' - ' + album_name.replace('/', '').replace(':', ',') + '.jpg'
