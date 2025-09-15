import os

import gradio as gr
from inference import inference

with gr.Blocks() as blocks:
    gr.Markdown(
        """
# <center> AI艺术二维码生成器 </center>
## 💡 如何生成漂亮的二维码
<p>我们使用二维码图像作为初始图像和控制图像，这使您能够生成与您提供的提示非常自然地融合在一起的二维码。强度参数定义了二维码中添加的噪声量，然后通过Controlnet将噪声二维码引导至提示和二维码图像。使用介于0.8和0.95之间的高强度值，并选择介于0.6和2.0之间的调节比例。这种模式可以说实现了软件上最吸引人的二维码图像，但也需要对控制网调节比例和强度值进行更多调整。如果生成的图像看起来与原始二维码非常相似，请确保轻轻增加强度值并减少调节范围。还可以查看下面的示例。</p>
                """
    )

    with gr.Row():
        with gr.Column():
            qr_code_content = gr.Textbox(
                label="二维码内容",
                info="QR Code Content or URL",
                value="",
            )
            with gr.Accordion(label="QR Code Image (Optional)", open=False):
                qr_code_image = gr.Image(
                    label="QR Code Image (Optional). Leave blank to automatically generate QR code",
                    type="pil",
                )

            prompt = gr.Textbox(
                label="提示词",
                info="Prompt that guides the generation towards",
            )

            prompt_en = gr.Textbox(
                label="提示词_en",
                info="Prompt_en that guides the generation towards",
            )

            negative_prompt = gr.Textbox(
                label="消极提示",
                value="ugly, disfigured, low quality, blurry, nsfw",
            )
            use_qr_code_as_init_image = gr.Checkbox(label="是否原始", value=True, interactive=False, info="Whether init image should be QR code. Unclick to pass init image or generate init image with Stable Diffusion 2.1")

            with gr.Accordion(label="Init Images (Optional)", open=False, visible=False) as init_image_acc:
                init_image = gr.Image(label="Init Image (Optional). Leave blank to generate image with SD 2.1", type="pil")


            with gr.Accordion(
                label="Params: The generated QR Code functionality is largely influenced by the parameters detailed below",
                open=True,
            ):
                controlnet_conditioning_scale = gr.Slider(
                    minimum=0.0,
                    maximum=5.0,
                    step=0.01,
                    value=1.1,
                    label="调节器",
                )
                strength = gr.Slider(
                    minimum=0.0, maximum=1.0, step=0.01, value=0.9, label="强度"
                )
                guidance_scale = gr.Slider(
                    minimum=0.0,
                    maximum=50.0,
                    step=0.25,
                    value=7.5,
                    label="生成参数",
                )
                seed = gr.Slider(
                    minimum=-1,
                    maximum=9999999999,
                    step=1,
                    label="Seed",
                    randomize=True,
                )
                eta = gr.Number(label="eta (DDIM)", value=0.0)
            with gr.Row():
                run_btn = gr.Button("生成")
        with gr.Column():
            result_image = gr.Image(label="Result Image")
    run_btn.click(
        inference,
        inputs=[
            qr_code_content,
            prompt,
            negative_prompt,
            guidance_scale,
            controlnet_conditioning_scale,
            strength,
            seed,
            init_image,
            qr_code_image,
            use_qr_code_as_init_image,
            eta
        ],
        outputs=[prompt_en, result_image],
    )

    gr.Examples(
        examples=[
            [
                "https://aistudio.baidu.com/aistudio/usercenter",
                "沙漠中流动的五颜六色的湖泊和河流的鸟瞰图",
                "ugly, disfigured, low quality, blurry, nsfw",
                7.5,
                1.3,
                0.9,
                62500000,
                None,
                None,
                True,
                0.0
            ],
            [
                "https://aistudio.baidu.com/aistudio/usercenter",
                "明亮的阳光从潮湿的洞穴大石头墙的裂缝中射进来",
                "ugly, disfigured, low quality, blurry, nsfw",
                7.5,
                1.11,
                0.9,
                62500000,
                None,
                None,
                True,
                0.0
            ],
            [
                "https://aistudio.baidu.com/aistudio/usercenter",
                "天景高度美观，古希腊温泉浴场自然美丽",
                "ugly, disfigured, low quality, blurry, nsfw",
                7.5,
                1.5,
                0.9,
                62500000,
                None,
                None,
                True,
                0.0
            ],
        ],
        fn=inference,
        inputs=[
            qr_code_content,
            prompt,
            negative_prompt,
            guidance_scale,
            controlnet_conditioning_scale,
            strength,
            seed,
            init_image,
            qr_code_image,
            use_qr_code_as_init_image,
        ],
        outputs=[prompt_en, result_image],
        cache_examples=True,
    )

blocks.queue(concurrency_count=1, max_size=20)
blocks.launch(share=bool(os.environ.get("SHARE", False)))