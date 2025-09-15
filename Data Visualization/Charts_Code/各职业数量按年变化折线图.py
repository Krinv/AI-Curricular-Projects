#各职业的增长折线图
#按分页拼接
#x轴为年份，y轴为数量，不同颜色为不同地区

#库
import pandas as pd
from pyecharts import options as opts
#导入线图、标签
from pyecharts.charts import Line,Tab
from pyecharts.globals import ThemeType

#文件路径
data_path='C:/Users/22273/Desktop/数据可视化/Data.xls'

#创建标签
tab=Tab(page_title="各职业年变化图")

#读取数据
data=pd.read_excel(data_path,sheet_name="Sheet2",usecols="A:F",nrows=44)

#年份提取
years=sorted(data['数据统计时间'].unique())

#按职业循环创建
for career in data.columns[2:6].unique():
    line=Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    
    #str(year)将years中的每个元素转换为字符串类型
    line.add_xaxis([str(year) for year in years])

    #以地区循环
    for region in data['地区'].unique():
        
        #布尔索引出data['地区']等于region的值
        #.sort_values('数据统计时间')按数据统计时间列升序排序
        region_data=data[data['地区']==region].sort_values('数据统计时间')
        
        #分离出职业为career的部分
        y_data=region_data[career].tolist()
        
        line.add_yaxis(
            series_name=region,
            y_axis=y_data,
        )

    #线图全局设置
    line.set_global_opts(

        #f-string语法：将career与字符串"数量折线图"连接
        title_opts=opts.TitleOpts(title=f"{career}数量折线图"),
        xaxis_opts=opts.AxisOpts(name="年份"),
        yaxis_opts=opts.AxisOpts(name="数量(单位：人)"),
        #图例设置到右边
        legend_opts=opts.LegendOpts(
            #图例位置右边5%
            pos_right="5%",
            #图例排列方向垂直
            orient="vertical",
        ),
    )

    #加入到标签
    tab.add(line,career)

#渲染成html
tab.render("C:/Users/22273/Desktop/数据可视化/Charts_Code/Graphics/按职业标签的人数增长折线图.html")

