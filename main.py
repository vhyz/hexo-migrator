# -*- coding:utf-8 -*-

import GetHtml
import HtmlToMarkdown
import os

def deploy(mk):
    os.chdir(mk)
    os.system('hexo g')
    os.system('hexo d')

def get_article(Blog,url,mk):
    html = GetHtml.GeHtml(url, Blog)
    print(html.get_cnt())
    article_list = html.get_article_list()
    for article in article_list:
        with open(mk + '\source\_posts\\' + article.title + '.md', 'w', encoding='utf-8') as w:
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
    print('Please input the type of your Blog,such as cnblogs,csdn_old,csdn_new')
    Blog=input()
    print('Please input the href of your Blog')
    url=input()
    print('Please input the load of your hexo Blog,such as E:\\hexo\\blog')
    mk=input()
    get_article(Blog,url,mk)
    deploy(mk)


if __name__ == '__main__':
    main()