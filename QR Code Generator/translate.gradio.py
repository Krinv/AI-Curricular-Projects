import gradio as gr
from translation import translate

# def quickstart(name):
#     return "欢迎使用BML CodeLab应用创建工具Gradio, " + name + "!!!"
demo = gr.Interface(fn=translate, inputs="text", outputs="text")

demo.launch()
