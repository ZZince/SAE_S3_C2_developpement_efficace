import numpy as np
import cv2
import time


def seach_points(image_gray: np.ndarray, threshold: int = 128, num_columns: int = 70):
    """Seach points without stars on the loaded image
    Args:
        image_gray (np.ndarray): loaded gray image
        treshold (int): gamma max of the points searched (default: 128)
        num_columns (int): number of colmuns to look as extremity of image (default: 70)
    """

    # Impossible to annote, height and width are integers
    height, width = image_gray.shape[:2]

    # Find the point without stars on the left side of the grayscale image
    left_x: int = next(
        (
            x
            for x in range(num_columns)
            for y in range(height)
            if np.any(image_gray[y, x] <= threshold)
        ),
        None,
    )

    # Find the point without stars at the 1/3 of the grayscale image
    one_third_x: int = width // 3
    one_third_y: int = next(
        (y for y in range(height) if np.any(image_gray[y, one_third_x] <= threshold)),
        None,
    )

    # Find the point without stars at the 2/3 of the grayscale image
    two_thirds_x: int = 2 * (width // 3)
    two_thirds_y: int = next(
        (y for y in range(height) if np.any(image_gray[y, two_thirds_x] <= threshold)),
        None,
    )

    # Find the point without stars on the right side of the grayscale image
    right_x: int = next(
        (
            x
            for x in range(width - 1, width - num_columns - 1, -1)
            for y in range(height)
            if np.any(image_gray[y, x] <= threshold)
        ),
        None,
    )

    return left_x, one_third_x, one_third_y, two_thirds_x, two_thirds_y, right_x


def generate_linear_gradient(
    image_color: np.ndarray,
    left_x: int,
    one_third_x: int,
    one_third_y: int,
    two_thirds_x: int,
    two_thirds_y: int,
    right_x: int,
) -> np.ndarray:
    """
    Generate linear gradient in the color image based on color points
    Args:
        image_color (np.ndarray): Color image for gradient generation
        left_x (int): X-coordinate of the left boundary for gradient interpolation
        one_third_x (int): X-coordinate of the 1/3 boundary for gradient interpolation
        one_third_y (int): Y-coordinate common to the 1/3 boundary for gradient interpolation
        two_thirds_x (int): X-coordinate of the 2/3 boundary for gradient interpolation
        two_thirds_y (int): Y-coordinate common to the 2/3 boundary for gradient interpolation
        right_x (int): X-coordinate of the right boundary for gradient interpolation

    Returns:
        np.ndarray: The linear gradient generated
    """

    color_pixel_left: np.ndarray = image_color[0, left_x]
    color_pixel_one_third: np.ndarray = image_color[one_third_y, one_third_x]
    color_pixel_two_thirds: np.ndarray = image_color[two_thirds_y, two_thirds_x]
    color_pixel_right: np.ndarray = image_color[0, right_x]

    # Generate a horizontal linear gradient using the four color points
    gradient_linear: np.ndarray = np.zeros_like(image_color)

    # Calculate the ratios for the three segments
    ratio_left: np.ndarray = np.linspace(0, 1, one_third_x - left_x, endpoint=False)
    ratio_middle: np.ndarray = np.linspace(
        0, 1, two_thirds_x - one_third_x, endpoint=False
    )
    ratio_right: np.ndarray = np.linspace(0, 1, right_x - two_thirds_x + 1)

    # Interpolate colors using the ratios
    gradient_linear[:, :one_third_x] = (1 - ratio_left)[
        :, np.newaxis
    ] * color_pixel_left + ratio_left[:, np.newaxis] * color_pixel_one_third
    gradient_linear[:, one_third_x:two_thirds_x] = (1 - ratio_middle)[
        :, np.newaxis
    ] * color_pixel_one_third + ratio_middle[:, np.newaxis] * color_pixel_two_thirds
    gradient_linear[:, two_thirds_x : right_x + 1] = (1 - ratio_right)[
        :, np.newaxis
    ] * color_pixel_two_thirds + ratio_right[:, np.newaxis] * color_pixel_right

    return gradient_linear


if __name__ == "__main__":
    print("Test for 100 gradient generation: ")

    image_color = cv2.imread(
        "gradient/Elephants_Trunk_Combined.jpg", cv2.IMREAD_COLOR
    ).astype(np.float64)
    image_gray = cv2.imread(
        "gradient/Elephants_Trunk_Combined.jpg", cv2.IMREAD_GRAYSCALE
    ).astype(np.float64)

    start_time = time.time()

    for _ in range(100):
        (
            left_x,
            one_third_x,
            one_third_y,
            two_thirds_x,
            two_thirds_y,
            right_x,
        ) = seach_points(image_gray)

        gradient_linear = generate_linear_gradient(
            image_color,
            left_x,
            one_third_x,
            one_third_y,
            two_thirds_x,
            two_thirds_y,
            right_x,
        )

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time for 100 gradient generations: {elapsed_time} seconds")
