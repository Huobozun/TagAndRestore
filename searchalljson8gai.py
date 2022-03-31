
from dataclasses import replace
import os
import json
import nltk
import csv
import numpy
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

    def searchnumber(text0, label0):
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
            if(lines0[i] == '(' and i+1<x and lines0[i+1].isalpha()==True):
                
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

        starts = []  # 每个tokenstr起始段在句子中的位置
        ends=[]# 每个tokenstr终止端在句子中的位置
        ii = 0
        #print(len(lines))
        for i in range(0,len(lines)):
            while ii <= len(text0):
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
        #print(len(starts),len(ends))

        #比对标签个数,并且记录在段落中的位置
        number1=0
        local0=[]
        for j in range(0,len(searchlabel)):
            
            for i in range(0,len(tokenstr)):
            
                if(tokenstr[i]==searchlabel[j]):
                    number1+=1
                    
                    str1=(starts[i],text0[starts[i]:ends[i+x-1]])#记录文中位置和文中匹配词
                    local0.append(str1)
        #比对缩写个数和去除缩写后标签的个数            
        if(q==1):
            #比对缩写个数
            
            for i in range(0,len(lines)):
                
                if(lines[i]==searchlabel[len(searchlabel)-2]):
                    number1+=1
                    
                    str1=(starts[i],text0[starts[i]:ends[i]])#记录文中位置和文中匹配词
                    local0.append(str1)
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
                    #print(stokenstr[i])
                    str1=(starts[i],text0[starts[i]:ends[i+snlongword-1]])#记录文中位置和文中匹配词
                    local0.append(str1)
        #print(local0)
            

        return number1,local0#number1对应的是匹配成功的总次数，local0中包含匹配的文中end-index以及对应文中的词[（145，'文中标注'）]


    def _searchword(zhishi,_text,_label):
    #进行label的计数和定位
    #返回label在各段text中总的匹配数number和在各段的位置（0，[（145,'文中标注'）]）
        if(_text=={0: None} or _text=={0: None}  or _text==None or _text=='' or _label=={0: None}  or _label==None or _label==''or _label==[]):
            number=0
            numberz=0
            localf=[]
            #print('Nothing')
        else:

            a0=0
            localf=[]
            b=0
            if(zhishi=='0'):   #用一段查找各个标注来确定位置
                for j in range(0,len(_label)):
                    if(_label[j]!=None and _label[j]!={0: None} and _label[j]!='' and _label!=[]):
                        [a0,a1]=searchalljson.searchnumber(_text,_label[j])
                        if(a0>0):
                            b+=a0
                        #print(j+1,_label,a0,a1)
                        #print(a1)
                        if(a1!=[] and a1!=None and a1!='' and a1!={0: None}):
                            if isinstance(a1,list):
                                localf.append(a1[0])
            else:   #用一个标注查找各个段来确定数量
                for j in range(0,len(_text)):
                    if(_text[j]!=None and _text[j]!={0: None} and _text[j]!='' and _text!=[]):
                        [a0,a1]=searchalljson.searchnumber(_text[j],_label)
                        b+=a0
                        #print(j+1,_label,a0,a1)
                        #print(a1)
                        if(a1!=[] and a1!=None and a1!='' and a1!={0: None}):
                            str2=(j,a1)
                            localf.append(str2)
            number=b
            #localf是标签依次在各个段落出现的位置
            #print(_label,number,localf)
        return number,localf

    def getresult(text,name_en):
        #把name_en整合成一个个label组成的list
        #把text整合成一个个组成的list
        #返回总的匹配数num，可还原标注数量nlabel,和各个label依次在各段的位置localall[（0，[（145,'文中标注'）]）]
        num=0
        localall=[]   
        localnum=[] 
        #把name_en都去除dict格式，都搞成list或者单个str       
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
        nlabel=0
        #采用每段中依次出现每个标注的方式来划定位置，得到localall
        if isinstance(text,list):
            for i in range(0,len(text)):
                [n,l]=searchalljson._searchword('0',text[i],name_en)
                if(n>0):
                    str6=(i,l)
                    localall.append(str6)
        else:
            [n,l]=searchalljson._searchword('0',text,name_en)
            if(n>0):
                str6=(i,l)
                localall.append(str6)
            
        #采用各个标注依次在每段的出现数量来统计数量，得到num,nlabel
        if isinstance(name_en,list):
            for i in range(0,len(name_en)):
                [n,l]=searchalljson._searchword('1',text,name_en[i])
                if(n>0):
                    nlabel+=1
                num+=n
        else:
            [n,l]=searchalljson._searchword('1',text,name_en)
            if(n>0):
                    nlabel+=1
            num+=n
        return num,nlabel,localall


    def _search(self):
        #输入路径和要匹配的关键词
        #返回所有json文件总的标签匹配数在文章中的数量y
        #返回所有json文件标签匹配数量bnumcount
        #每个文件中的标签在各个文件各个段落出现的位置用xl3表示
        y=0
        bnumcount=0
        bnum=[]
        nlabel=1
        llabel=[]
        with open(self.label0+self.label1+'.tsv','w',newline='')as f:
            for i in range(0,len(self.filelist)):
                _path='/home/zjg/code1/result/'+self.filelist[i]

                self.text=searchalljson.getinf(_path,self.text0,self.text1)
                self.label=searchalljson.getinf(_path,self.label0,self.label1)
                #indications的按照每出现一次整个一套indications为可匹配一次
                #print(self.label)
                if(self.label0=='indications'):
                    bnum.append(0)
                    if isinstance(self.label,dict):
                        nlabel=len(self.label)
                        for j in range(0,nlabel):
                            llabel=self.label[j]
                            if isinstance(llabel,str):
                                xllabel=[]
                                xllabel.append(llabel)
                            else:
                                xllabel=llabel
                            [x,x2,xl3]=searchalljson.getresult(self.text,xllabel)
                            if(x>0):
                                bnum[i]+=1
                                bnumcount+=1#indications是每个里面的出现就记为一个     
                            y+=x
                    else:
                        [x,x2,xl3]=searchalljson.getresult(self.text,self.label)
                        if(x>0):
                            bnum[i]+=1
                            bnumcount+=1#indications是每个里面的出现就记为一个
                        y+=x
                #除去indications的其他标注按照每出现包含的每个单词记为可匹配一次
                else:
                    bnum.append(0)
                    [x,x2,xl3]=searchalljson.getresult(self.text,self.label)#x是每次可还原标注在文中匹配量，x2是可还原标注量，xl3是[（段落，[（位置，'匹配词'）])]
                    if(x>0):
                        bnum[i]+=x2
                        bnumcount+=x2#其余标注是里面的每个词出现都记为一个
                    y+=x
                #将label排列成list,以便于统计数量以及显示在文中出现的位置
                
                f.write('%s\t%s\n' %(self.filelist[i].replace('.json', ''), json.dumps(xl3)))
                """tsv_w=csv.writer(f,delimiter=' ')
                #tsv_w=csv.writer(f)
                str5=[]
                for j in range(0,3):
                    if(j==0):  
                        str5.append(self.filelist[i].replace('.json', '')) 
                    if(j==1):
                        str5.append('\t\t')   
                    if(j==2):   
                        str5.append(xl3)
                #print(str5)
                tsv_w.writerow(json.dumps(str5))#写入tsv文件,str5的格式是'34905388   "[(0,[145,'文中标注'])]"'"""
               
        print(self.label0,self.label1,y,bnumcount)#输出前两个标题，y是可还原标注在文中出现的数量，bnumcount是可还原标注的数量
        return y,bnum
    
 
path ='/home/zjg/code1/result/'
Filelist = get_filelist(dir)



a1=searchalljson(Filelist,'text','','indications','ct_disease')
a2=searchalljson(Filelist,'text','','indications','name_en')
a3=searchalljson(Filelist,'text','','indications','name_short')
a4=searchalljson(Filelist,'text','','indications','name_synonyms')
b1=searchalljson(Filelist,'text','','disease_labels_en','')
b2=searchalljson(Filelist,'text','','bio_labels_en','')
b3=searchalljson(Filelist,'text','','patient_labels_en','')
b4=searchalljson(Filelist,'text','','therapy_labels_en','')


[aa1,anum1]=a1._search()
[aa2,anum2]=a2._search()
[aa3,anum3]=a3._search()
[aa4,anum4]=a4._search()
print('indications',aa1+aa2+aa3+aa4)
allnum=0
for i in range(0,len(Filelist)):
    ax1=bigger(anum1[i],anum2[i])
    ax2=bigger(ax1,anum3[i])
    ax3=bigger(ax2,anum4[i])
    allnum+=ax3
print(allnum)
[bb1,bnum1]=b1._search()
[bb2,bnum2]=b2._search()
[bb3,bnum3]=b3._search()
[bb4,bnum4]=b4._search()

