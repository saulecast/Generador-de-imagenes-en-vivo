import torch

device = 'cuda'

generator = torch.Generator(device).manual_seed(1024)

# 

from huggingface_hub import notebook_login
notebook_login()

#

model_id = "runwayml/stable-diffusion-v1-5"

#

from diffusers import StableDiffusionPipeline

#

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16", use_auth_token=True)
pipe = pipe.to(device)

#



prompt = "a whirlwind inside the metaverse, guy, male, man, hologram, half body, neurochip, android, cyborg, cyberpunk face, by loish, d & d, fantasy, intricate, elegant, highly detailed, colorful, digital painting, artstation, concept art, art by artgerm and greg rutkowski and alphonse mucha "
image = pipe(prompt).images[0]  
    
image.save("sd_img.png")

image