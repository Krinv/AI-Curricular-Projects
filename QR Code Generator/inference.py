import paddle
import gradio as gr
import qrcode
import os
import random
from PIL import Image
from paddlenlp.trainer import set_seed as seed_everything
from translation import translate
from ppdiffusers import (
    StableDiffusionPipeline,
    StableDiffusionXLControlNetPipeline,
    ControlNetModel,
)

qrcode_generator = qrcode.QRCode(
    version=1,
    error_correction=qrcode.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

controlnet = ControlNetModel.from_pretrained(
    "DionTimmer/controlnet_qrcode-control_v1p_sd15", paddle_dtype=paddle.float32
)

pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
   "stabilityai/stable-diffusion-xl-base-1.0",
    safety_checker=None,
    controlnet=controlnet,
    paddle_dtype=paddle.float16
)
pipe.enable_xformers_memory_efficient_attention()


def resize_for_condition_image(input_image: Image.Image, resolution: int):
    input_image = input_image.convert("RGB")
    W, H = input_image.size
    k = float(resolution) / min(H, W)
    H *= k
    W *= k
    H = int(round(H / 64.0)) * 64
    W = int(round(W / 64.0)) * 64
    img = input_image.resize((W, H), resample=Image.LANCZOS)
    return img

def inference(
    qr_code_content,
    prompt,
    negative_prompt,
    guidance_scale,
    controlnet_conditioning_scale,
    strength,
    seed,
    init_image,
    qrcode_image,
    use_qr_code_as_init_image,
    eta,
):
    if prompt is None or prompt == "":
        raise gr.Error("Prompt is required")

    prompt = translate(prompt)

    if qrcode_image is None and qr_code_content == "":
        raise gr.Error("QR Code Image or QR Code Content is required")
    
    if seed == -1:
        seed = random.randint(0, 65535000000)
    seed_everything(seed)

    if qr_code_content != "" or qrcode_image.size == (1, 1):
        print("Generating QR Code from content")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_content)
        qr.make(fit=True)

        qrcode_image = qr.make_image(fill_color="black", back_color="white")
        qrcode_image = resize_for_condition_image(qrcode_image, 768)
    else:
        print("Using QR Code Image")
        qrcode_image = resize_for_condition_image(qrcode_image, 768)

    init_image = qrcode_image

    out = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=qrcode_image,
        width=768,
        height=768,
        eta=eta,
        guidance_scale=float(guidance_scale),
        controlnet_conditioning_scale=float(controlnet_conditioning_scale),
        num_inference_steps=40,
    )
    return prompt, out.images[0]