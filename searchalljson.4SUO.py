
import os
import json
import nltk

import numpy
#from nltk.book import *
from nltk import ne_chunk, pos_tag,  word_tokenize
 

def get_filelist(dir):
 
    Filelist = []
 
    for home, dirs, files in os.walk(path):
 
        for filename in files:
 
            # 文件名列表，包含完整路径
            #Filelist.append(os.path.join(home, filename))
            # # 文件名列表，只包含文件名
            Filelist.append( filename)
    return Filelist
 
class searchalljson():
    def __init__(self,filelist,text0,text1,label0,label1) -> None:
        self.filelist=filelist
        self.text0=text0
        self.text1=text1
        self.label0=label0
        self.label1=label1
        pass
    def getinf(path,title1,title2):
    #读取json中的分词后的文本和个数(text数组长度)
        with open(path,'r',encoding='utf8')as fp:
            json_data=json.load(fp)
            #print('这是文件中的json数据：',json_data)
            #print('这是读取到文件数据的数据类型：', type(json_data))
            #读入各段text[]
            if(title2!=''):
                dic0={}
                dic0=json_data.get(title1)
                text={}
                for i in range(0,len(dic0)):
                    text[i]=dic0[i].get(title2)
            else:
                text={}
                text=json_data.get(title1)
    

            return text

    def searchnumber(text0, label0):
        #计数并且定位功能底层（单段，单个label）
        #返回单段中的匹配数number1和匹配位置[2,3]
        
        #标签分词
        lines0=nltk.word_tokenize(label0)
        #print(lines0)

        #整篇分词
        lines=nltk.word_tokenize(text0)
        #print(lines)

        #合成对应标签长度的list
        x=len(lines0)
        s=len(lines)
        #print(x,s)
        q=0
        #标签拼接
        searchlabel=['']
        for i in range(0,x):
            searchlabel[0]+=lines0[i].lower()
        #在任意一个词加上复数
        for i in range(0,x):
            searchlabel.append('')
            for j in range(0,x):    
                if(i != j):
                    searchlabel[i+1]+=lines0[j].lower()
                else:
                    searchlabel[i+1]+=lines0[j].lower()+'s'
        #检查是否有缩写
        for i in range(0,x):
            if(lines0[i] == '('):
                searchlabel.append('')
                searchlabel[len(searchlabel)-1]=lines0[i+1]
                #缩写保持大写
                q=1
                #只包含缩写的放在倒数第二位
                #去除缩写的标签放在最后一位
                searchlabel.append('')
                for j in range(0,i):
                    searchlabel[len(searchlabel)-1]+=lines0[j].lower()
                    snlongword=i



        #整篇拼接
        tokenstr=[]
        for i in range(0,s-x+1):
            longword=''
            for j in range(0,x):
                longword+=lines[i+j].lower()
            tokenstr.append(longword)
            
        #print(tokenstr)
        #print(searchlabel)  

        #比对标签个数,并且记录在段落中的位置
        number1=0
        local0=[]
        for j in range(0,len(searchlabel)):
            for i in range(0,len(tokenstr)):
                if(tokenstr[i]==searchlabel[j]):
                    number1+=1
                    local0.append(0)
                    local0[number1-1]=i
        #比对缩写个数和去除缩写后标签的个数            
        if(q==1):
            #比对缩写个数
            for i in range(0,len(lines)):
                if(lines[i]==searchlabel[len(searchlabel)-2]):
                    number1+=1
                    local0.append(0)
                    local0[number1-1]=i
            #比对去除缩写后的标签个数
            stokenstr=[]
            for i in range(0,s-snlongword+1):
                slongword=''
                for j in range(0,snlongword):
                    slongword+=lines[i+j].lower()
                stokenstr.append(slongword)
            for i in range(0,len(stokenstr)):
                if(stokenstr[i]==searchlabel[len(searchlabel)-1]):
                    number1+=1
                    local0.append(0)
                    local0[number1-1]=i
            

        return number1,local0


    def _searchword(_text,_label):
    #进行单个label的计数和定位
    #返回单个label在各段text中总的匹配数number和在各段的位置[2,3][1][][]
        if(_text=={0: None} or _text=={0: None}  or _text==None or _text=='' or _label=={0: None}  or _label==None or _label==''or _label==[]):
            number=0
            localf=[]
            #print('Nothing')
        else:

            a0=0
            localf=[]
            b=0

            for j in range(0,len(_text)):
                [a0,a1]=searchalljson.searchnumber(_text[j],_label)
                b+=a0
                #print(j+1,_label[i],a0,a1)
                #print(a1)
                localf.append(a1)
                #输出位置首单词
                """for i in range(0,len(a1)):
                    print(nltk.word_tokenize(_text[j])[a1[i]])"""
            number=b
            #localf是标签依次在各个段落出现的位置
            #print(number,localf)
        return number,localf

    def getresult(text,name_en):
        #把name_en整合成一个个label组成的list，依次放到text中去找。
        #返回总的匹配数num，和各个label依次在各段的位置[ [[2,3][1][][]] [[1][][][]] ]
        num=0
        localall=[]           
        if isinstance(name_en,dict):

            if isinstance(name_en[0],list):
                _name_en=name_en
                name_en=name_en[0]
            else:
                _name_en=name_en
                name_en=[]
                name_en.append(_name_en[0])

            for i in range(1,len(_name_en)):
                if isinstance(_name_en[i],list):
                    name_en+=_name_en[i]
                else:
                    name_en.append('')
                    name_en[len(name_en)-1]=_name_en[i]

        if isinstance(name_en,list):
            for i in range(0,len(name_en)):
                [n,l]=searchalljson._searchword(text,name_en[i])
                num+=n
                localall.append([])
                localall[i]=l
        else:
            [n,l]=searchalljson._searchword(text,name_en)
            num+=n
            localall.append([])
            localall=l
        return num


    def _search(self):
        #输入路径和要匹配的关键词
        #返回所有json文件总的标签匹配数
        y=0
        for i in range(0,len(self.filelist)):
            _path='C:\\Users\\yangx\\desktop\\1\\result\\'+self.filelist[i]

            self.text=searchalljson.getinf(_path,self.text0,self.text1)
            self.label=searchalljson.getinf(_path,self.label0,self.label1)

            x=searchalljson.getresult(self.text,self.label)
            y+=x

        print(self.label0,self.label1,y)
        return y
    
 
path ='C:\\Users\\yangx\\desktop\\1\\result'
Filelist = get_filelist(dir)

a1=searchalljson(Filelist,'_pm_abstract','text','indications','ct_disease')
a2=searchalljson(Filelist,'_pm_abstract','text','indications','name_en')
a3=searchalljson(Filelist,'_pm_abstract','text','indications','name_short')
a4=searchalljson(Filelist,'_pm_abstract','text','indications','name_synonyms')
b1=searchalljson(Filelist,'_pm_abstract','text','disease_labels_en','')
b2=searchalljson(Filelist,'_pm_abstract','text','bio_labels_en','')
b3=searchalljson(Filelist,'_pm_abstract','text','patient_labels_en','')
b4=searchalljson(Filelist,'_pm_abstract','text','therapy_labels_en','')

aa1=a1._search()
aa2=a2._search()
aa3=a3._search()
aa4=a4._search()
print('indications',aa1+aa2+aa3+aa4)
b1._search()
b2._search()
b3._search()
b4._search()
