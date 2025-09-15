#全省总数相关统计图
#各职业条形图，x轴为时间，y轴为数量，颜色为职业
#各职业数量变化折线，x轴为时间，y轴为数量,颜色为职业

#库
from pyecharts import options as opts
from pyecharts.charts import Bar,Line,Tab
import pandas as pd

#文件路径
data_path='C:/Users/22273/Desktop/数据可视化/Data.xls'
#读取数据
data=pd.read_excel(data_path,sheet_name="Sheet3",nrows=5)

#数据分离
#获取3到6列的列名，转换为列表
bar_x_data=list(data.columns[1:6])
years=sorted(data['数据统计时间'].tolist()) #注意升序排序

#创建一个year字典，每个键值为年份
#筛选出数据统计时间==year的行
#取出其中x_data包含的列
#转换为numpy数组、展平为1维数组、转为列表
bar_y_data={year:data[data["数据统计时间"]==year][bar_x_data].values.flatten().tolist() for year in years}

#柱状图
bar=Bar()
bar.add_xaxis(bar_x_data)
for year in years:
    bar.add_yaxis(str(year),bar_y_data[year])
#柱状图全局设置
bar.set_global_opts(
    title_opts=opts.TitleOpts(title="全省总数条形图"),
    xaxis_opts=opts.AxisOpts(name="职业"),
    yaxis_opts=opts.AxisOpts(name="数量(单位：人)")
)

#折线图绘制
# 创建数据
x_data = ["2018","2019","2020","2021"]
y1 = [190802,205625, 548024,579061]
y2=[486231,520251,217677,232661]
y3=[201514,219811,233067,250312]
y4=[32755,34126,34400,35120]

# 创建折线图对象
line = Line()

#绘图
line.add_xaxis(x_data)
line.add_yaxis("执业医师",y1)
line.add_yaxis("卫生技术人员",y2)
line.add_yaxis("注册护士",y3)
line.add_yaxis("机构",y4)

# 设置全局配置项
line.set_global_opts(
    title_opts=opts.TitleOpts(title="全省变化折线图"),
    yaxis_opts=opts.AxisOpts(name="数量(单位：人)"),
    xaxis_opts=opts.AxisOpts(name="年份")
)

#标签
tab=Tab(page_title="全省总数相关图")
tab.add(bar,"全省总数条形图")
tab.add(line,"全省变化折线图")

#输出
tab.render("C:/Users/22273/Desktop/数据可视化/Charts_Code/Graphics/全省总数相关.html")