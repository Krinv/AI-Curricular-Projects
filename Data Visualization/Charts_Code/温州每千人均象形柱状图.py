#温州市和全省千人均象形柱状图对比

#库
import pandas as pd
from pyecharts import options as opts
#象形柱状图
from pyecharts.charts import PictorialBar

# 数据
categories = ["千人床位数", "千人执业医师数", "千人卫生技术人员数", "千人注册护士数"]
#四年千人均平均数
data_Wenzhou = [4.66, 3.26, 7.65, 3.21]
data_Province = [5.76, 3.44, 8.67, 3.68]

# 象形条形图绘制
pictorialbar = PictorialBar(init_opts=opts.InitOpts(page_title="象形条形图"))
pictorialbar.add_xaxis(categories)

pictorialbar.add_yaxis(
    "温州千人均",
    [
        {"value": 4.66, "symbol": "image://C:/Users/22273/Desktop/数据可视化/Icon/BedW.png"},
        {"value": 3.26, "symbol": "image://C:/Users/22273/Desktop/数据可视化/Icon/DoctorW.png"},
        {"value": 7.65, "symbol": "image://C:/Users/22273/Desktop/数据可视化/Icon/SurgeonW.png"},
        {"value": 3.21, "symbol": "image://C:/Users/22273/Desktop/数据可视化/Icon/NurseW.png"},
    ],
    #展示数值标签
    label_opts=opts.LabelOpts(is_show=True,position="insideTopRight",color="blue"),
    symbol_size=40,
    #图标偏移量：x移动0，y移动-23（向上）
    symbol_offset=[0,-23],
    #设定为根据数值固定重复
    symbol_repeat="fixed",
    #图标间距
    symbol_margin="45%",
    #是否裁剪图标
    is_symbol_clip=True,
)

pictorialbar.add_yaxis(
    "全省千人均",
    [
        {"value": 5.76, "symbol": "image://C:/Users/22273/Desktop/数据可视化/Icon/Bed.png"},
        {"value": 3.44, "symbol": "image://C:/Users/22273/Desktop/数据可视化/Icon/Doctor.png"},
        {"value": 8.67, "symbol": "image://C:/Users/22273/Desktop/数据可视化/Icon/Surgeon.png"},
        {"value": 3.68, "symbol": "image://C:/Users/22273/Desktop/数据可视化/Icon/Nurse.png"},
    ],
    label_opts=opts.LabelOpts(is_show=True,position="insideBottomRight",color="green"),
    symbol_size=40,
    symbol_offset=[0,23],
    symbol_margin="50%",
    symbol_repeat="fixed",
    is_symbol_clip=True,
)

# 全局设置
pictorialbar.set_global_opts(
    title_opts=opts.TitleOpts(title="温州和全省每千人均相关数据的象形柱状图"),
    xaxis_opts=opts.AxisOpts(
        name="人数(单位：人)",
        is_show=True,
        #网格线设置
        splitline_opts=opts.SplitLineOpts(
            is_show=True,
            #网格线条设置
            linestyle_opts=opts.LineStyleOpts(color="black"),
        )
        ),
    yaxis_opts=opts.AxisOpts(
        is_show=True,
            splitline_opts=opts.SplitLineOpts(
                is_show=True,
                linestyle_opts=opts.LineStyleOpts(color="black")
            ),
        ),
    legend_opts=opts.LegendOpts(is_show=True),
)

# 反转轴使条形图横向显示
pictorialbar.reversal_axis()

# 渲染图表到 Notebook
pictorialbar.render("C:/Users/22273/Desktop/数据可视化/Charts_Code/Graphics/千人均.html")
