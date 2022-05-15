import imageio as iio
from pathlib import Path

def create_gif_from_pngs(folder):
    gif_file = "animation.gif"

    images = list()
    for file in Path(folder).iterdir():
        print(file)
        if not file.is_file():
            continue
        images.append(iio.imread(file))

    iio.mimwrite(gif_file, images, format=".gif", fps=3)

if __name__ == "__main__":
    create_gif_from_pngs("png")