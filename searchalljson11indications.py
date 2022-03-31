
from dataclasses import replace
import os
import json
import nltk
import csv
import numpy
import tiaoci
#from nltk.book import *
from nltk import ne_chunk, pos_tag,  word_tokenize
 

def get_filelist(dir):#依次遍历.json文件
 
    Filelist = []
 
    for home, dirs, files in os.walk(path):
 
        for filename in files:
 
            # 文件名列表，包含完整路径
            #Filelist.append(os.path.join(home, filename))
            # # 文件名列表，只包含文件名
            Filelist.append( filename)
    return Filelist
 
def bigger(x,y):#比较大小，进行indications标注的可还原统计
    if(x>y):
        return x
    else:
        return y
        
class searchalljson():
    def __init__(self,filelist,text0,text1,label0,label1) -> None:
        self.filelist=filelist
        self.text0=text0
        self.text1=text1
        self.label0=label0
        self.label1=label1
        pass
    def getinf(path,title1,title2):
    #读取json中的数据，包括文本和标注
        with open(path,'r',encoding='utf8')as fp:
            json_data=json.load(fp)
            #print('这是文件中的json数据：',json_data)
            #print('这是读取到文件数据的数据类型：', type(json_data))
            #读入各段text[]
            
            if(title1=='text'):#如果是要读入文本，直接将标题与文本拼接起来
                text={}
                
                dic0={}
                dic0=json_data.get('_pm_abstract')
                
                for i in range(0,len(dic0)+1):
                    if(i==0):
                        text[i]=json_data.get('_pm_title')
                    else:
                        text[i]=dic0[i-1].get('text')
            else:
                if(title1=='indications'):#读入indications，直接将下面的属性标签都拼起来
                    text={}
                    dic0={}
                    dic0=json_data.get('indications')
                    
                
                    for i in range(0,len(dic0)):
                        dict1=[]                       
                        dict1.append(dic0[i].get('ct_disease'))
                        
                        dict1.append(dic0[i].get('name_en'))
                       
                        dict1.append(dic0[i].get('name_short'))
                       
                        dict1.append(dic0[i].get('name_synonyms'))
                      
                        text[i]=dict1
                        
                else:
            
                    #print(text)
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

    def searchnumber(label1,text0, label0):
        #计数并且定位功能底层（单段，单个label）
        #返回单段中的匹配数number1和匹配位置[（位置，'匹配词'）]
        
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
        
        
        #整篇拼接
        tokenstr=[]
        for i in range(0,s-x+1):
            longword=''
            for j in range(0,x):
                longword+=lines[i+j].lower()
            tokenstr.append(longword)

        starts = []  # 每个tokenstr起始段在句子中的位置
        ends=[]# 每个tokenstr终止端在句子中的位置
        ii = 0
        for i in range(0,len(lines)):
            while ii < len(text0):
                if(lines[i]=='``' or lines[i]=="''"):
                    lines[i]='"'
        
                if text0[ii:ii + len(lines[i])]== lines[i]:
                        starts.append(ii)
                        ends.append(ii+len(lines[i]))
                        #print(lines[i])
                        ii += len(lines[i])
                    
                        break
                else:
                    ii += 1

        #比对标签个数,并且记录在段落中的位置
        number1=0
        local0=[]
        for j in range(0,len(searchlabel)):
            
            for i in range(0,len(tokenstr)):
                
                if(tokenstr[i]==searchlabel[j]):
                    number1+=1
                    str1=(starts[i],text0[starts[i]:ends[i+x-1]])#记录文中位置和文中匹配词
                    local0.append(str1)
    
            

        return number1,local0#number1对应的是匹配成功的总次数，local0中包含匹配的文中end-index以及对应文中的词[（145，'文中标注'）]


    def _searchword(label1,_text,_label):
    #进行label的计数和定位
    #返回label在各段text中总的匹配数number和在各段的位置（0，[（145,'文中标注'）]）
        if(_text=={0: None} or _text=={0: None}  or _text==None or _text=='' or _label=={0: None}  or _label==None or _label==''or _label==[]):
            
            localf=[]
            b=0
            #print('Nothing')
        else:

            a0=0
            localf=[]
            b=0
            for j in range(0,len(_label)):
                if(_label[j]!=None and _label[j]!={0: None} and _label[j]!='' and _label!=[]):
                    [a0,a1]=searchalljson.searchnumber(label1,_text,_label[j])
                    if(a0>0):
                        b+=a0
                    if(a1!=[] and a1!=None and a1!='' and a1!={0: None}):
                        if isinstance(a1,list):
                            localf.append(a1[0])
            
            #localf是标签依次在各个段落出现的位置
        
        return b,localf

    def getresult(label1,text,name_en):
        #把name_en整合成一个个label组成的list
        #把text整合成一个个组成的list
        #返回各个label依次在各段的位置localall[（0，[（145,'文中标注'）]）]
     
        localall=[]   
          
        #把text都去除dict格式，都搞成list或者单个str 
        if isinstance(text,dict):

            if isinstance(text[0],list):
                _text=text
                text=text[0]
            else:
                _text=text
                text=[]
                text.append(_text[0])

            for i in range(1,len(_text)):
                if isinstance(_text[i],list):
                    text+=_text[i]
                else:
                    text.append('')
                    text[len(text)-1]=_text[i]
        #采用每段中依次出现每个标注的方式来划定位置，得到localall
        if isinstance(text,list):
            for i in range(0,len(text)):
                [n,l]=searchalljson._searchword(label1,text[i],name_en)
                if(n>0):
                    str6=(i,l)
                    localall.append(str6)
        else:
            [n,l]=searchalljson._searchword(label1,text,name_en)
            if(n>0):
                str6=(i,l)
                localall.append(str6)
            
        return localall


    def _search(self):
        #输入路径和要匹配的关键词
        #每个文件中的标签在各个文件各个段落出现的位置用xl3表示
        he=[]
        
        with open('indications3.tsv','w',newline='')as f:
            for i in range(0,len(self.filelist)):
                _path='/home/zjg/code1/result/'+self.filelist[i]

                self.text=searchalljson.getinf(_path,self.text0,self.text1)
                self.label=searchalljson.getinf(_path,self.label0,self.label1)
                #indications的按照每出现一次整个一套indications为可匹配一次
                #print(self.text,self.label)
                if(self.label0=='indications'):
                    name_en=self.label
                    if isinstance(name_en,dict):
                        if isinstance(name_en[0],list):
                            _name_en=name_en
                            name_en=name_en[0]
                        else:
                            _name_en=name_en
                            name_en=[]
                            name_en.append(_name_en[0])

                        for ii in range(1,len(_name_en)):
                            if isinstance(_name_en[ii],list):
                                name_en+=_name_en[ii]
                            else:
                                name_en.append('')
                                name_en[len(name_en)-1]=_name_en[ii]
                    
                    labres=[]
                    for p in range(0,len(name_en)):
                        if isinstance(name_en[p],list):
                            z=name_en[p]
                            for j in range(0,len(name_en[p])):
                                labres.append(z[j])
                        else:
                            labres.append(name_en[p])
                    for pp in range(0,len(labres)):
                        if isinstance(labres[pp],str):
                            labres[pp]=labres[pp].lower()
                    
                    labres=tiaoci._tiaocichongfu(labres)#去重
                    xl3=searchalljson.getresult(self.label1,self.text,labres)
                        
                #除去indications的其他标注按照每出现包含的每个单词记为可匹配一次
                else:
                   xl3=searchalljson.getresult(self.label1,self.text,self.label)#xl3是[（段落，[（位置，'匹配词'）])]   
                #将label排列成list,以便于统计数量以及显示在文中出现的位置
                
                f.write('%s\t%s\n' %(self.filelist[i].replace('.json', ''), json.dumps(xl3)))
                he.append(xl3)
        return he
    
 
path ='/home/zjg/code1/result/'
Filelist = get_filelist(dir)

a1=searchalljson(Filelist,'text','','indications','')
aa1=a1._search()

 


