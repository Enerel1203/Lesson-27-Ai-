import os, io, time, requests
from datetime import datetime
from PIL import Image
from config import HF_API_KEY

MODEL = "stabilityai/stable-diffusion-2-inpainting"
API = f"https://router.huggingface.co/hf-inference/models/{MODEL}"

ALLOWED = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
MAX_MB = 8

def ask_image():
    while True:
        p = input("Vintage photo path: ").strip().strip('"').strip("'")
        if not os.path.isfile(p):
            print("Not found")
            continue
        if os.path.splitext(p)[1].lower() not in ALLOWED:
            print("Unsupported type")
            continue
        if os.path.getsize(p) > MAX_MB * 1024 * 1024:
            print("Too large")
            continue
        return p

def ask_mask():
    while True:
        p = input("Mask image path: ").strip().strip('"').strip("'")
        if not os.path.isfile(p):
            print("Not found")
            continue
        return p

def restore(image_path, mask_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    with open(mask_path, "rb") as f:
        mask_bytes = f.read()

    prompt = (
        "restore damaged areas of a vintage photograph, "
        "natural facial features, realistic textures, "
        "historical photo restoration, high quality"
    )

    response = requests.post(
        API,
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        files={
            "image": image_bytes,
            "mask": mask_bytes
        },
        data={"prompt": prompt},
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(response.text)

    return response.content

def main():
    image_path = ask_image()
    mask_path = ask_mask()

    try:
        restored = restore(image_path, mask_path)

        out = f"restored_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        with open(out, "wb") as f:
            f.write(restored)

        print("Saved:", out)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()