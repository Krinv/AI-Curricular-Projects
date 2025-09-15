#按地区分的总数图
#x轴为床位数量、执业医师数量、卫生技术人员数量、注册护士数量、机构数量

#库
#options模块包含图表外观和行为的各种配置选项
from pyecharts import options as opts
#导入条形图和时间线图表
from pyecharts.charts import Bar,Timeline
#允许在python代码中插入JavaScript代码，对于自定义图表交互性功能（自定义提示框内容、设置图表动态行为）特别有用
from pyecharts.commons.utils import JsCode

#读取excel的库
import pandas as pd

#文件路径
data_path='C:/Users/22273/Desktop/数据可视化/Data.xls'

#每年的行数
#1~45步长为4的序列,excel中索引从0开始，因此要减1
rows_2021=list(range(1,42,4)) 

#前面插入一个0索引，保证把首行读进来
rows_2021.insert(0,0)  
rows_2020=list(range(2,44,4))
rows_2020.insert(0,0)
rows_2019=list(range(3,45,4))
rows_2019.insert(0,0)
rows_2018=list(range(4,46,4))
rows_2018.insert(0,0)

#lambda函数检查x是否在rows中，否则跳过
data_2021=pd.read_excel(data_path,sheet_name='Sheet2',skiprows=lambda x:x not in rows_2021)
data_2020=pd.read_excel(data_path,sheet_name='Sheet2',skiprows=lambda x:x not in rows_2020)
data_2019=pd.read_excel(data_path,sheet_name='Sheet2',skiprows=lambda x:x not in rows_2019)
data_2018=pd.read_excel(data_path,sheet_name='Sheet2',skiprows=lambda x:x not in rows_2018)

#创建时间线
timeline=Timeline(init_opts=opts.InitOpts(page_title="各市医疗人员总数图"))

#定义创建每年柱状图函数
def create_bar(data,year):
    bar=Bar()
    bar.add_xaxis(data.iloc[:,0].tolist())
    bar.add_yaxis("执业医师",data.iloc[:,2].tolist())
    bar.add_yaxis("卫生技术人员",data.iloc[:,3].tolist())
    bar.add_yaxis("注册护士",data.iloc[:,4].tolist())
    bar.add_yaxis("机构数量",data.iloc[:,5].tolist())
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=f"{year}各地区医疗人员总数"),
        xaxis_opts=opts.AxisOpts(name="地区"),
        yaxis_opts=opts.AxisOpts(name="人员数量(单位：人)"),
    )
    return bar

#为每年柱状图添加时间线
timeline.add(create_bar(data_2018,2018),"2018")
timeline.add(create_bar(data_2019,2019),"2019")
timeline.add(create_bar(data_2020,2020),"2020")
timeline.add(create_bar(data_2021,2021),"2021")

#设置时间线全局选项
timeline.add_schema(
    play_interval=2000, #播放间隔
    is_timeline_show=True, #时间线显示
    is_auto_play=False, #自动播放
    is_loop_play=False, #循环播放
)

#渲染HTML文件
timeline.render("C:/Users/22273/Desktop/数据可视化/Charts_Code/Graphics/各市区医疗人员总数.html")

    

