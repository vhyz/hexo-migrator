# -*- coding:utf-8 -*-
class HtmlToMarkdown:

    def __init__(self,tags):
        self.__quote=0
        self.__markdown_string=""
        self.dfs(tags)

    def dfs(self, tags):
        for tag in tags:
            if tag == '\n':
               continue
            elif tag.name is None:
                self.__markdown_string += tag
            elif tag.name[0] == 'h':
                title_string = ''
                for i in range(1, 7):
                    title_string += '#'
                    if tag.name == 'h' + str(i):
                        self.__markdown_string += "\n"+title_string + " " + tag.text + "\n"
                        break
            elif tag.name == 'p':
                self.__markdown_string = self.__markdown_string + "\n"
                self.dfs(tag)
                self.__markdown_string = self.__markdown_string + "\n"
            elif tag.name == 'blockquote':
                self.__quote += 1
                quote_string=""
                for i in range(0,self.__quote):
                    quote_string+='>'
                self.__markdown_string = self.__markdown_string + "\n"+quote_string
                self.dfs(tag)
            elif tag.name == 'code':
                try:
                    language=tag['class'][1]
                except:
                    language=""
                self.__markdown_string+="\n"+"```"+language+"\n"+tag.text+"\n"+"```"+"\n"
            elif tag.name == 'a':
                title=""
                if not tag.get('title') is None:
                    title=tag['title']
                self.__markdown_string+='['+tag.text+']'+'('+tag['href']+title+')'
            elif tag.name == 'br':
                self.__markdown_string+="\n"
            elif tag.name == 'ol':
                li_cnt=0
                ol="\n"
                for li in tag:
                    if li =='\n':
                        continue
                    li_cnt+=1
                    ol+=str(li_cnt)+".  "+li.text+"\n"
                self.__markdown_string+=ol
            elif tag.name == 'ul':
                ul="\n"
                for li in tag:
                    if li == '\n':
                        continue
                    ul+="*  "+li.text+"\n"
                self.__markdown_string+=ul
            elif tag.nmae == 'hr':
                self.__markdown_string+="\n"+"******"+"\n"
            elif tag.name == 'em':
                self.__markdown_string+="\n"+"*"+tag.text+"*"+"\n"
            elif tag.name == 'strong':
                self.__markdown_string+="\n"+"**"+tag.text+"**"+"\n"
            elif tag.name == 'img':
                title,alt="",""
                if not tag.get('title')is None:
                    title=tag['title']
                if not tag.get('alt') is None:
                    title = tag['alt']
                img="!"+"["+alt+"]"+"("+tag['src']+' "'+title+'"'+")"
                self.__markdown_string+=img
            else:
                self.dfs(tag)

    def get_string(self):
        return self.__markdown_string