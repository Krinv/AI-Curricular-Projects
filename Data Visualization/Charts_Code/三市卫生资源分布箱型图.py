import pandas as pd;
from pyecharts.charts import Boxplot;
from pyecharts import options as opts;

data_w=[45841,78080,33373,33488,5880]
data_h=[90754,142341,55013,63044,5633]
data_n=[45181,83163,34274,35490,4787]

data=[data_h,data_n,data_w]

box=Boxplot()
box.add_xaxis(["杭州","宁波","温州"])
#处理成箱型图可接受数据
box.add_yaxis("2021年",box.prepare_data(data))

box.set_global_opts(title_opts=opts.TitleOpts(title="2021年三市卫生资源分布箱型图"))

box.render("C:/Users/22273/Desktop/数据可视化/Charts_Code/Graphics/2021三市卫生资源分散箱型图.html")

