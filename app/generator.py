from app.config import USE_COLAB
from PIL import Image
import random

pipe = None  # global model

def load_model():
    global pipe
    if pipe is not None:
        return pipe

    from diffusers import StableDiffusionPipeline
    import torch

    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    )
    pipe = pipe.to("cuda")

    return pipe


def generate_image(prompt):
    if not USE_COLAB:
        # Mock mode (local)
        return Image.new(
            'RGB',
            (512, 512),
            color=(random.randint(0,255), 120, 180)
        )

    model = load_model()
    image = model(prompt).images[0]
    return image