import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Radar
from pyecharts.globals import ThemeType

# 文件路径
data_path = 'C:/Users/22273/Desktop/数据可视化/Data.xls'

# 读取数据
data = pd.read_excel(data_path, sheet_name="Sheet5", usecols='A,D,E,F,G,K')

# 数据分离
area_list = data["地区"].tolist()

# 定义颜色列表
colors = [
    "#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#A833FF", "#33FFF7", 
    "#FFBF33", "#FF3380", "#80FF33", "#3380FF", "#FF8333", "#FF338A"
]

# 创建雷达图
radar = (
    Radar()
    #设置雷达图指标和样式
    .add_schema(
        schema=[
            opts.RadarIndicatorItem(name="床位", max_=8,min_=4.7),
            opts.RadarIndicatorItem(name="执业医师", max_=4.6,min_=3.1),
            opts.RadarIndicatorItem(name="卫生技术人员", max_=11.7,min_=7.5),
            opts.RadarIndicatorItem(name="注册护士", max_=5.2,min_=3.1),
        ],
        #设置雷达图分割区域
        splitarea_opt=opts.SplitAreaOpts(
            is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
        ),
        textstyle_opts=opts.TextStyleOpts(color="black"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各市卫生资源雷达图"),
        legend_opts=opts.LegendOpts(
            orient="vertical",
            pos_right=True
        )
    )
)

# 循环插入数据并分配颜色
for i, area in enumerate(area_list):
    radar.add(
        series_name=area,
        data=[data.iloc[i, 1:].tolist()],
        linestyle_opts=opts.LineStyleOpts(color=colors[i % len(colors)]),
        label_opts=opts.LabelOpts(is_show=False),
    )

# 渲染生成 HTML 文件
radar.render("C:/Users/22273/Desktop/数据可视化/Charts_Code/Graphics/各省卫生资源雷达图.html")
