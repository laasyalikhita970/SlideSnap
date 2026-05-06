from PIL import Image
import os

def images_to_pdf(folder="slides", output="slides.pdf"):
    images = []

    for file in sorted(os.listdir(folder)):
        if file.endswith(".jpg"):
            img_path = os.path.join(folder, file)
            img = Image.open(img_path).convert("RGB")
            images.append(img)

    if images:
        images[0].save(output, save_all=True, append_images=images[1:])
        print(f"PDF saved as {output}")
    else:
        print("No images found!")


if __name__ == "__main__":
    images_to_pdf()