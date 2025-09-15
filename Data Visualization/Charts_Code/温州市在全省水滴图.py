import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Liquid, Grid
from pyecharts.commons.utils import JsCode

# 数据
data = pd.read_excel("C:/Users/22273/Desktop/数据可视化/Data.xls", sheet_name="Sheet6")

# 数据分离
data_bed = data.iloc[:, 1].tolist()  # [:,1]选择所有行和索引为1列（第二列）
data_doctor = data.iloc[:, 2].tolist()
data_surgeon = data.iloc[:, 3].tolist()
data_nurse = data.iloc[:, 4].tolist()

# 水滴图绘制
lbed = (
    Liquid(init_opts=opts.InitOpts(width="500px", height="500px"))
    .add(
        "床位数占比",
        [round(data_bed[0] / data_bed[1], 4)],
        center=["58%", "70%"],
        label_opts=opts.LabelOpts(
            formatter=JsCode(
                """function(param){
                return (Math.floor(param.value * 10000) / 100) + '%';
                }"""
            ),
            position="inside",
        ),
    )
    .set_global_opts(title_opts=opts.TitleOpts(
        title="床位数",
        pos_top="75%",
        pos_left="54%",
    ))
)

ldoctor = (
    Liquid(init_opts=opts.InitOpts(width="500px", height="500px"))
    .add(
        "执业医生数占比",
        [round(data_doctor[0] / data_doctor[1], 4)],
        center=["40%", "27%"],
        label_opts=opts.LabelOpts(
            formatter=JsCode(
                """function(param){
                return (Math.floor(param.value * 10000) / 100) + '%';
                }"""
            ),
            position="inside",
        ),
    )
    .set_global_opts(title_opts=opts.TitleOpts(
        title="医生数",
        pos_left="36%",
        pos_top="33%",
    ))
)

lsurgeon = (
    Liquid(init_opts=opts.InitOpts(width="500px", height="500px"))
    .add(
        "卫生技术员数占比",
        [round(data_surgeon[0] / data_surgeon[1], 4)],
        center=["75%", "27%"],
        label_opts=opts.LabelOpts(
            formatter=JsCode(
                """function(param){
                return (Math.floor(param.value * 10000) / 100) + '%';
                }"""
            ),
            position="inside",
        ),
    )
    .set_global_opts(title_opts=opts.TitleOpts(
        title="卫生技术员数",
        pos_left="68%",
        pos_top="33%",
    ))
)

lnurse = (
    Liquid(init_opts=opts.InitOpts(width="300px", height="300px"))
    .add(
        "注册护士数占比",
        [round(data_nurse[0] / data_nurse[1], 4)],
        center=["25%", "73%"],
        label_opts=opts.LabelOpts(
            formatter=JsCode(
                """function(param){
                return (Math.floor(param.value * 10000) / 100) + '%';
                }"""
            ),
            is_show=True,
            position="inside",
        ),
    )
    .set_global_opts(title_opts=opts.TitleOpts(
        title="护士数",
        pos_left="21%",
        pos_top="78%",
    ))
)

# 合并水滴图
grid = Grid(init_opts=opts.InitOpts(page_title="水滴图"))
grid.add(lbed, grid_opts=opts.GridOpts(pos_left="10%", pos_top="10%"))
grid.add(ldoctor, grid_opts=opts.GridOpts(pos_left="55%", pos_top="5%"))
grid.add(lsurgeon, grid_opts=opts.GridOpts(pos_left="5%", pos_top="55%"))
grid.add(lnurse, grid_opts=opts.GridOpts(pos_left="55%", pos_top="55%"))

# 渲染图表到 HTML 文件
grid.render("C:/Users/22273/Desktop/数据可视化/Charts_Code/Graphics/温州各总数在全省占比.html")
