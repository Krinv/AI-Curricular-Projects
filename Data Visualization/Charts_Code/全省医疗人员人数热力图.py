import pandas as pd
from pyecharts.charts import HeatMap
from pyecharts import options as opts

professions = ['执业医师', '卫生技术人员', '注册护士']
time=["2018","2019","2020","2021"]

heatmap_data = [
    [0, 3, 579061],
    [0, 2, 548024],
    [0, 1, 205625],
    [0, 0, 190802],
    [1, 3, 232661],
    [1, 2, 217677],
    [1, 1, 520251],
    [1, 0, 486231],
    [2, 3, 250312],
    [2, 2, 233067],
    [2, 1, 219811],
    [2, 0, 201514],
]

# 创建热力图
heatmap = (
    HeatMap()
    .add_xaxis(professions)
    .add_yaxis("职业人数",time,heatmap_data)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各职业数量随时间变化的热力图"),
        #颜色显示范围自定义
        visualmap_opts=opts.VisualMapOpts(
            max_=600000,
            min_=190000,
        ),
        xaxis_opts=opts.AxisOpts(name="职业"),
        yaxis_opts=opts.AxisOpts(name="时间")
    )
)

heatmap.render("C:/Users/22273/Desktop/数据可视化/Charts_Code/Graphics/全省各职业数量随时间变化热力图.html")
