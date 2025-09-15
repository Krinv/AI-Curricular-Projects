#使用3D地图展示数值地理分布性
#堆叠柱状图显示医疗配备分布

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map3D,Tab
#该库是用于指定不同图表的枚举类，内含多种图表
from pyecharts.globals import ChartType

#数据框
df=pd.read_excel('C:/Users/22273/Desktop/数据可视化/data.xls',sheet_name='Sheet5')

#数据分离：提取row行中对应属性对应的元素，重组列表
data_bed=[
    (row['地区'],[row['经度'],row['维度'],row['千人床位数']])

    #循环，定义两个变量，index接收行索引，row接收行数据
    #使用pandas中函数iterrows遍历dataframe的每一行，返回行索引和包含含数据的series对象
    for index, row in df.iterrows()
]
data_doctor=[
    (row['地区'],[row['经度'],row['维度'],row['千人执业医师数']])
    for index, row in df.iterrows()
]
data_surgeon=[
    (row['地区'],[row['经度'],row['维度'],row['千人卫生技术人员数']])
    for index, row in df.iterrows()
]
data_nurse=[
    (row['地区'],[row['经度'],row['维度'],row['千人注册护士数']])
    for index, row in df.iterrows()
]

#3d地图绘制
map=Map3D()
#地图配置方案
map.add_schema(
        maptype="浙江",
        #y轴的高度重定义，实现小数值显示较高的柱状条
        box_height=20,
        #地图高度
        region_height=1,
        #配置图元样式
        itemstyle_opts=opts.ItemStyleOpts(
            color="white",
            opacity=1,#图元透明度，1为完全不透明
            border_width=0.8,#图元边框粗细
            border_color="rgb(62,215,213)", #边框颜色
        ),
        #3D光照
        light_opts=opts.Map3DLightOpts(
            #主光源颜色：白
            main_color="#fff",
            #光强
            main_intensity=1.2,
            #阴影质量
            main_shadow_quality="high",
            #主光源阴影
            is_main_shadow=False,
            #主光源方位角
            main_beta=10,
            #环境光强度
            ambient_intensity=0.3,
        ),
        #标签：这里为地名
        map3d_label=opts.Map3DLabelOpts(
            is_show=True
        )
    )
#添加3d柱状图
#由于堆叠实现不理想，因此平铺实现，所以每个柱子间需要错开
#依次更新图标经度
t=0.05
data_bed = [(city, [longitude-t*2,latitude, value]) for city, (longitude, latitude, value) in data_bed]
data_doctor = [(city, [longitude-t, latitude, value]) for city, (longitude, latitude, value) in data_doctor]
data_nurse = [(city, [longitude+t, latitude, value]) for city, (longitude, latitude, value) in data_nurse]

#添加到3d地图
map.add(
    series_name="千人均床位数",
    data_pair=data_bed,
    type_=ChartType.BAR3D,
    bar_size=1,
)
map.add(
    series_name="千人均医师数",
    data_pair=data_doctor,
    type_=ChartType.BAR3D,
    bar_size=1,
)
map.add(
    series_name="千人均卫生技术人员数",
    data_pair=data_surgeon,
    type_=ChartType.BAR3D,
    bar_size=1,
)
map.add(
    series_name="千人均注册医师数",
    data_pair=data_nurse,
    type_=ChartType.BAR3D,
    bar_size=1,
)
map.set_global_opts(
    title_opts=opts.TitleOpts(title="千人均地区分布图"),
)

#总数图
#数据
#数据分离
datas_bed=[
    (row['地区'],[row['经度'],row['维度'],row['床位']])
    for index, row in df.iterrows()
]
datas_doctor=[
    (row['地区'],[row['经度'],row['维度'],row['执业医师']])
    for index, row in df.iterrows()
]
datas_surgeon=[
    (row['地区'],[row['经度'],row['维度'],row['卫生技术人员']])
    for index, row in df.iterrows()
]
datas_nurse=[
    (row['地区'],[row['经度'],row['维度'],row['注册护士']])
    for index, row in df.iterrows()
]
#数据更新
t=0.05
datas_bed = [(city, [longitude-t*2,latitude, value]) for city, (longitude, latitude, value) in datas_bed]
datas_doctor = [(city, [longitude-t, latitude, value]) for city, (longitude, latitude, value) in datas_doctor]
datas_nurse = [(city, [longitude+t, latitude, value]) for city, (longitude, latitude, value) in datas_nurse]

maps=Map3D()
#地图配置方案
maps.add_schema(
        maptype="浙江",
        box_height=40,
        region_height=1,
        emphasis_label_opts=opts.EmphasisOpts(is_disabled=1),
        itemstyle_opts=opts.ItemStyleOpts(
            color="white",
            opacity=1,
            border_width=0.8,
            border_color="rgb(62,215,213)",
        ),
        light_opts=opts.Map3DLightOpts(
            main_color="#fff",
            main_intensity=1.2,
            main_shadow_quality="high",
            is_main_shadow=False,
            main_beta=10,
            ambient_intensity=0.3,
        ),
        map3d_label=opts.Map3DLabelOpts(
            is_show=True,
        )
    )
#添加到3d地图
maps.add(
    series_name="床位数",
    data_pair=datas_bed,
    type_=ChartType.BAR3D,
    bar_size=1,
)

maps.add(
    series_name="医师数",
    data_pair=datas_doctor,
    type_=ChartType.BAR3D,
    bar_size=1,
)
maps.add(
    series_name="卫生技术人员数",
    data_pair=datas_surgeon,
    type_=ChartType.BAR3D,
    bar_size=1,
)
maps.add(
    series_name="注册医师数",
    data_pair=datas_nurse,
    type_=ChartType.BAR3D,
    bar_size=1,
)
maps.set_global_opts(
    title_opts=opts.TitleOpts(title="总数分布图"),
)

#添加入标签
tab=Tab(page_title="3D分布图")
tab.add(maps,"总数")
tab.add(map,"千人均")

tab.render("C:/Users/22273/Desktop/数据可视化/Charts_Code/Graphics/3D分布柱状图.html")