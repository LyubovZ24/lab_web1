import os.path

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def perform_image_processing(filename, frame_width, frame_color):
    image = Image.open(filename)

    image_with_frame = add_frame_to_image(image, frame_width, frame_color)
    graphic = plot_graphic(image)

    filename_without_directory = filename.split("\\")[1]
    new_filename = os.path.join('static\\photos', 'with_frame', filename_without_directory)
    image_with_frame.save(new_filename)

    graphic_name = os.path.join("static\\graphics",
                                '.'.join(filename_without_directory.split('.')[:-1]) + "_graphic.png")
    graphic.savefig(graphic_name)

    return new_filename, graphic_name


def add_frame_to_image(image, frame_width, frame_color):
    img_width, img_height, = image.size

    base_image = Image.new("RGB",
                           (img_width + 2 * frame_width, img_height + 2 * frame_width),
                           color=frame_color)

    base_image.paste(image, (frame_width, frame_width))
    return base_image


def plot_graphic(image):
    image_array = np.array(image)

    red_values = image_array[:, :, 0].ravel()
    green_values = image_array[:, :, 1].ravel()
    blue_values = image_array[:, :, 2].ravel()

    plt.figure(figsize=(10, 6))

    plt.hist(red_values, bins=256, color='red', alpha=0.5, label='Красный')
    plt.hist(green_values, bins=256, color='green', alpha=0.5, label='Зелёный')
    plt.hist(blue_values, bins=256, color='blue', alpha=0.5, label='Синий')

    plt.xlabel('Значение цвета')
    plt.ylabel('Частота')
    plt.title('Распределение цветов на графике')
    plt.legend()

    return plt

