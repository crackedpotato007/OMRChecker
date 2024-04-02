from dataclasses import dataclass

import cv2
from screeninfo import get_monitors

from src.utils.image import ImageUtils
from src.utils.logger import logger

monitor_window = get_monitors()[0]


@dataclass
class ImageMetrics:
    # TODO: Move TEXT_SIZE, etc here and find a better class name
    window_width, window_height = monitor_window.width, monitor_window.height
    # for positioning image windows
    window_x, window_y = 0, 0
    reset_pos = [0, 0]


class InteractionUtils:
    """Perform primary functions such as displaying images and reading responses"""

    image_metrics = ImageMetrics()

    @staticmethod
    def show(name, image, pause=1, resize=False, reset_pos=None, config=None):
        image_metrics = InteractionUtils.image_metrics
        if image is None:
            logger.info(f"'{name}' - NoneType image to show!")
            if pause:
                cv2.destroyAllWindows()
            return
        if resize:
            if not config:
                raise Exception("config not provided for resizing the image to show")
            _display_height, display_width = config.dimensions.display_image_shape
            image_to_show = ImageUtils.resize_util(image, display_width)
        else:
            image_to_show = image

        cv2.imshow(name, image_to_show)

        if reset_pos:
            image_metrics.window_x = reset_pos[0]
            image_metrics.window_y = reset_pos[1]

        cv2.moveWindow(
            name,
            image_metrics.window_x,
            image_metrics.window_y,
        )

        h, w = image_to_show.shape[:2]

        # Set next window position
        margin = 25
        h += margin
        w += margin

        # TODO: get ppi for correct positioning?
        adjustment_ratio = 3
        h, w = h // adjustment_ratio, w // adjustment_ratio
        if image_metrics.window_x + w > image_metrics.window_width:
            image_metrics.window_x = 0
            if image_metrics.window_y + h > image_metrics.window_height:
                image_metrics.window_y = 0
            else:
                image_metrics.window_y += h
        else:
            image_metrics.window_x += w

        if pause:
            logger.info(
                f"Showing '{name}'\n\t Press Q on image to continue. Press Ctrl + C in terminal to exit"
            )

            wait_q()
            InteractionUtils.image_metrics.window_x = 0
            InteractionUtils.image_metrics.window_y = 0


class Stats:
    # TODO Fill these for stats
    # Move qbox_vals here?
    # badThresholds = []
    # veryBadPoints = []
    files_moved = 0
    files_not_moved = 0


def wait_q():
    esc_key = 27
    while cv2.waitKey(1) & 0xFF not in [ord("q"), esc_key]:
        pass
    cv2.destroyAllWindows()
