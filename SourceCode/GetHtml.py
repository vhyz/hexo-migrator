# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests

class Article:

    def __init__(self):
        self.title=""
        self.time=""
        self.text=""
        self.category=""
        self.tag=[]

class GetHtml(object):

    def __init__(self,Url,Blog):
        '''
        Contrust a GetHtml object
        It will give you the html of the article and the text of the time and title
        :param Url: Blog_index
        :param Blog: Blog_type
        '''
        self.__url=Url
        self.__cnt=0
        self.__article_list=[]
        while self.__url!='':
            url_list=self.get_url_list(Blog)
            for url in url_list:
                self.get_article(url,Blog)

    def get_html(self,url):
        try:
            r=requests.get(url,timeout=30)
            r.raise_for_status()
            r.encoding=r.apparent_encoding
            return r.text
        except:
            print("获取链接"+url+"时失败")

    def get_url_list(self,Blog):
        '''
        :param Blog: Judge different blogs
        :return: The url of every article
        '''
        url_list=[]
        html=self.get_html(self.__url)
        soup=BeautifulSoup(html,'lxml')
        lista=[]
        '''
        if Blog == 'cnblogs':
            lista=soup.find_all('div',class_='postTitle')
            next_page=soup.find('a',text='下一页')
        else:
            lista=soup.find_all('span',class_='link_title')
            next_page = soup.find('a', rel='next')
        '''
        lista=soup.find_all(Blog['index_url']['tag'],attrs={Blog['index_url']['key']:Blog['index_url']['valve']})
        next_page=soup.find(Blog['next_page']['tag'],attrs={Blog['next_page']['key']:Blog['next_page']['valve'],},text=Blog['next_page']['text'])
        self.__url=''
        if not next_page is None:
            self.__url = next_page['href']
        for Url in lista:
            try:
                url_list.append(Url.a['href'])
                self.__cnt=self.__cnt+1
            except:
                print('获取单篇博客链接失败')
        return url_list

    def get_article(self,url,Blog):
        '''
        Get the html of the article,the text of the time and the head
        :param url: The url of the article
        :param Blog: Judge different blogs
        :return: None
        '''
        html=self.get_html(url)
        soup=BeautifulSoup(html,'lxml')
        article_html=soup.find(Blog['body']['tag'],attrs={Blog['body']['key']:Blog['body']['valve']})
        title=soup.find(Blog['title']['tag'],attrs={Blog['title']['key']:Blog['title']['valve']}).text
        time=soup.find(Blog['time']['tag'],attrs={Blog['time']['key']:Blog['time']['valve']}).text
        tag=[]
        category=''
        if Blog['name']=='cnblogs':
            BlogData_soup = soup.find_all('script', type='text/javascript')
            BlogData = str(BlogData_soup[0].text + BlogData_soup[2].text)
            currentBlogApp=self.get_string(BlogData,'currentBlogApp',4,"'")
            cb_blogId=self.get_string(BlogData, 'cb_blogId', 1, ",")
            cb_entryId=self.get_string(BlogData, 'cb_entryId', 1, ",")
            category,tag=self.get_categoris_cnblogs(currentBlogApp,cb_blogId,cb_entryId)
        else:
            category_soup=soup.find(Blog['category']['tag'],attrs={Blog['category']['key']:Blog['category']['valve']})
            if not category_soup is None:
                category=category_soup.contents[0]
            tag_soup=soup.find(Blog['tag']['tag'],attrs={Blog['tag']['key']:Blog['tag']['key']})
            tag_list=[]
            if not tag_soup is None:
                tag_list=tag_soup.find_all('a')
            for i in tag_list:
                tag.append(i.text)
        article=Article()
        article.text=article_html
        article.time=time
        article.category=category
        article.tag=tag
        article.title=title
        self.__article_list.append(article)

    def get_string(self,text, string_to_find_tag, length, end):
        tag_start = text.find(string_to_find_tag)
        string_to_find_start = tag_start + len(string_to_find_tag) + length
        string_to_find_back = text.find(end, string_to_find_start)
        string_to_find = text[string_to_find_start:string_to_find_back]
        return str(string_to_find)

    def get_categoris_cnblogs(self,blogApp,blogId,postId):
        get_data={'blogApp':blogApp,'blogId':blogId,'postId':postId}
        url = "http://www.cnblogs.com/mvc/blog/CategoriesTags.aspx"
        r=requests.get(url,data=get_data)
        r_json=r.json()
        category_soup=BeautifulSoup(r_json['Categories'],'lxml')
        tags_soup=BeautifulSoup(r_json['Tags'],'lxml')
        if category_soup.text!='':
            category=category_soup.a.text
        else:
            category=""
        tag_list=[]
        if tags_soup.text!='':
            tags=tags_soup.find_all('a')
            for i in tags:
                tag_list.append(i.text)
        return category,tag_list

    def get_article_list(self):
        return self.__article_list

    def get_cnt(self):
        return self.__cnt