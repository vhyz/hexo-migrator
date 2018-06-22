# -*- coding:utf-8 -*-

import GetHtml
import HtmlToMarkdown
import os
import json


def get_article(Blog,url):
    html = GetHtml.GetHtml(url, Blog)
    print(html.get_cnt())
    article_list = html.get_article_list()
    try:
        os.mkdir('source')
    except:
        pass
    for article in article_list:
        with open('source/' + article.title + '.md', 'w', encoding='utf-8') as w:
            text = "---\n" + 'title: ' + article.title + "\n" + 'date: ' + article.time + "\n"
            if article.category != '':
                text += 'categories:\n- ' + article.category + "\n"
            if article.tag != []:
                text += 'tags:\n'
                for t in article.tag:
                    text += '- ' + t + "\n"
            text += "---\n"
            Markdown = HtmlToMarkdown.HtmlToMarkdown(article.text)
            text += Markdown.get_string()
            w.write(text)

def main():
    with open('Setting/Setting.json','r',encoding='utf-8')as f:
        blog_list=json.load(f)
    while True:
        print('Please input the number of your Blog')
        for i in range(len(blog_list)):
            print(str(i)+'. '+blog_list[i],end='   ')
        print()
        blog_type=int(input())
        if blog_type>=0 and blog_type<len(blog_list):
            blog_json_name=blog_list[blog_type]
            break
    with open('Setting/'+blog_json_name+'Setting.json','r',encoding='utf-8')as f:
        Blog=json.load(f)
    print('Please input the href of your Blog')
    url=input()
    print('Running......')
    get_article(Blog,url)


if __name__ == '__main__':
    main()