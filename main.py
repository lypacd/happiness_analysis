import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly as py
import matplotlib.pyplot as plt
from pyecharts.charts import Bar, Map, Line, Page, Pie, Grid
from pyecharts import options as opts


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读入数据与数据处理，写你存数据的位置，这里是我本机存放文件的路径
s = r'C:\\Users\\acdji\\Desktop\\happiness_analysis\\data'
df_2020 = pd.read_csv(s+'/2020.csv', encoding='utf-8')
df_2021 = pd.read_csv(s+'/2021.csv', encoding='utf-8')
df_2022 = pd.read_csv(s+'/2022.csv', encoding='utf-8')
#去除前打印一下
# print(df_2022)
#观察到df_2022最后一行数据无效所以需要去除
df_2022.drop([len(df_2022)-1],inplace=True)

#去除最后一行后打印一下
# print(df_2022)
# 删除不必要的信息
df_2020= df_2020.iloc[:, :12]
columns = ['Standard error of ladder score', 'upperwhisker', 'lowerwhisker']
df_2020.drop(columns, axis=1, inplace=True)

# 数据信息
def data_info():
    print(df_2020.info())
    print(df_2020.describe())

# 幸福地图
def HappinessMap():
    x_data = df_2020['Country name'].tolist()
    y_data = df_2020['Ladder score'].round(2).tolist()

    # 地图
    map1 = Map()
    map1.add('', [list(z) for z in zip(x_data, y_data)], maptype='world',)
    map1.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    map1.set_global_opts(title_opts=opts.TitleOpts(title='Happiness Score'),
    visualmap_opts=opts.VisualMapOpts(max_=8, is_piecewise=True,
        pieces=[{'max': 3, 'min': 0, 'label': '0-3'},
                {'max': 4, 'min': 3.1,
                    'label': '3-4'},
                {'max': 5, 'min': 4.1,
                    'label': '4-5'},
                {'max': 6, 'min': 5.1,
                    'label': '5-6'},
                {'max': 7, 'min': 6.1,
                    'label': '6-7'},
                {'max': 8, 'min': 7.1, 'label': '7-8'}]
        ),
                        )
    map1.render("./produced_data/2020年幸福地图.html")

# 各大地区的平均幸福指数
def country_score_of_every_region():
    df_m = df_2020.groupby('Regional indicator')['Ladder score'].mean().sort_values()
    x_data = df_m .index.tolist()
    y_data = df_m .values.round(2).tolist()
    grid = Grid()
    bar1 = Bar()
    bar1.add_yaxis('',y_data)
    bar1.add_xaxis(x_data)
    bar1.set_global_opts(title_opts=opts.TitleOpts(title='Average Happiness Score by Regional Indicator of 2020'))
    bar1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='right'),
            markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")]))
    bar1.set_colors('CadetBlue')
    bar1.reversal_axis()

    grid.add(bar1, grid_opts=opts.GridOpts(pos_left="20%"))

    grid.render("./produced_data/2020年各大地区的平均幸福指数.html")

# 各幸福区间的百分比
def regions_country_pie():
    df2 = df_2020.iloc[:,:3]
    df2['score_group'] = pd.cut(x=df2['Ladder score'],bins=[0,1,2,3,4,5,6,7,8]).astype('str')
    c = (
        Pie()
        .add(
        '',
        [list(z) for z in zip(df2.groupby('score_group').score_group.count().index.tolist(),df2.groupby('score_group').score_group.count().values.tolist())],
            radius=["30%", "75%"],
            rosetype="area",
        label_opts = opts.LabelOpts(position='right'),
        )
        .set_global_opts(
        title_opts=opts.TitleOpts(title='Number of Countries by Happiness Score Categories of 2020'),
        legend_opts=opts.LegendOpts(is_show=False),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:\n {c} ({d}%)"))
    )
    c.render("./produced_data/2020年各幸福区间的百分比.html")

# 2022前10
def Top10_country_happiness_of2022():
    rank_top10 = df_2022.head(
        10)[['Country', 'Happiness score']]
    #列表逆置，要不然图片中数值的位置不符合人的感知
    rank_top10_co = list(reversed(rank_top10['Country']))
    rank_top_num= list(reversed(rank_top10['Happiness score']))
    trace = go.Bar(
        x=rank_top10_co,
        y=rank_top_num,
        name="世界幸福指数排名前十2022"
    )
    fig = go.Figure(data=[trace])
    pyplt = py.offline.plot
    pyplt(fig, filename='./produced_data/2022年世界幸福感排名前十的国家.html', auto_open=False)
    # 可改变一下点的形状
    print("输出2022年世界幸福感排名前十的国家.html成功")

#2022后10
def Bottom10_country_happiness_of2022():
    last_top10= df_2022.tail(
        10)[['Country', 'Happiness score']]
    # print(rank_top10)
    #最好不要用列表逆置，当想要用dataframe逆置的时候用data.iloc[::-1]
    last_top10= last_top10.iloc[::-1]
    trace = go.Bar(
        x=last_top10['Country'],
        y=last_top10['Happiness score'],
        name="世界幸福指数排名倒数十个国家或地区2022"
    )
    fig = go.Figure(data=[trace])
    pyplt = py.offline.plot
    pyplt(fig, filename='./produced_data/2022年世界幸福感排名倒数十名的国家.html', auto_open=False)
    # 可改变一下点的形状
    print("输出2022年世界幸福感排名倒数十名的国家.html成功")









#测试
data_info()
HappinessMap()
country_score_of_every_region()
regions_country_pie()
Top10_country_happiness_of2022()
Bottom10_country_happiness_of2022()
