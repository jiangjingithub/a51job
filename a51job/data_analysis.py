import pandas as pd 
from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
import pymongo
import numpy as np

mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.sans-serif'] = ['SimHei']
myfont = font_manager.FontProperties(fname="C:\Windows\Fonts\msyh.ttf") #微软雅黑字体位置

def process():
    """数据清洗及处理"""
    # 连接，创造客户端
    client=pymongo.MongoClient("localhost", 27017)
    # 获得数据库
    db = client.job
    data =  db.content
    columns = ["name","add","money",'date']
    df = pd.DataFrame([i for i in data.find()],columns=columns)
    # print(df.head(10))
    ked,ked2 = df["add"].str.split("-").str
    df["new_add"] = pd.DataFrame(ked)
    df["danwei"] = df["money"].str[-3:]
    df["money"] = df["money"].str.replace("千/月","").str.replace("万/月","")
    min_m,max_m = df["money"].str.split("-").str
    df["min_m"] = pd.DataFrame(min_m)
    df["min_m"] = pd.to_numeric(df["min_m"],errors="coerce")
    df["max_m"] = pd.DataFrame(max_m)
    df["max_m"] = pd.to_numeric(df["max_m"],errors="coerce")
    d,f = df["danwei"].str.split("/").str
    df["d"] = pd.DataFrame(d)
    df["d"] = df["d"].str.replace("千","1000").str.replace("万","10000")
    df["d"] = pd.to_numeric(df["d"],errors="coerce")
    df["f"] = pd.DataFrame(f)
    df["f"] = df["f"].str.replace("月","1").str.replace("年","12")
    df["f"] = pd.to_numeric(df["f"],errors="coerce")
    df["min_m"] = df.min_m*df.d/df.f
    df["max_m"] = df.max_m*df.d/df.f
    df.date = df.date.str.rjust(10,"-").str.replace("----","2019")
    df.date = pd.to_datetime(df.date,errors="coerce")
    df = df.drop(["add","money","danwei","d","f"],axis=1)
    df = df.dropna()
    df = df.set_index(df.date)
    return df
    # print(df.info())
    
def map_pie(data):
    """统计城市占全部招聘的比例，比例太少列为其他"""
    df1 = data.groupby(["new_add"]).count()["name"].sort_values(ascending=False)
    # print(df1)
    df1 = df1.drop(["异地招聘"])
    df = df1.iloc[:9]
    new_data = df1.iloc[:20].index.tolist()
    num = df1.iloc[9:].sum()
    # print(num)
    index = df.index.tolist()
    index.append("其他")
    df = df.reindex(index)
    df["其他"] = num
    # print(df)
    labels=df.index
    # print(lables)
    l = [0.1]+[0]*9
    # print(l)
    explode = tuple(l)
    sizes = df.values
    fig, ax =plt.subplots()
    ax.pie(sizes,labels=labels,explode=explode,autopct="%1.2f%%",shadow=True, startangle=90)
    # 等宽高比可确保将饼图绘制为圆。
    ax.axis('equal')
    # plt.show()
    ax.set_title("统计城市占全部招聘的比例",fontsize=20)
    plt.savefig("城市占比.png")   
    return new_data

def map_bar(data,city):
    """统计招聘次数前20位的城市平均工资"""
    # print(city)
    # print(data)
    # data["a_money"] = (data.min_m+data.max_m)/2
    # print(data)
    df = data.groupby("new_add").mean()["min_m"]
    # print(df)
    df = df.loc[city].apply(lambda x: int(x))
    # print(df)
    _x = df.index
    _y = df.values
    x = np.arange(len(_x))
    width = 0.8
    plt.figure(figsize=(22,8),dpi=80)
    result = plt.bar(x,_y,width,color="orange")
    plt.ylabel('金额/元',fontproperties=myfont,fontsize=26)
    plt.yticks(fontsize=20)
    plt.title("51job招聘数前20名的平均工资统计表",fontproperties=myfont,fontsize=30)
    plt.xticks(x,_x,fontproperties=myfont,fontsize=20)
    plt.xlabel("城市",fontproperties=myfont,fontsize=26)
    plt.xlim(-1,len(_x)+1)
    plt.ylim(0,max(_y)*1.2)
    plt.grid(alpha=0.4)
    for each in result:
        height = each.get_height()
        plt.annotate('{}'.format(height),
                        xy=(each.get_x() + each.get_width() / 2, height),
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom',fontsize=16,fontproperties=myfont)
    plt.savefig("全国招聘数前20名的平均工资统计表.png") 

if __name__ == "__main__":
    data = process()
    city = map_pie(data)
    map_bar(data,city)
