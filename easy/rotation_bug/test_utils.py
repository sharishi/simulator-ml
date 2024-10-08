import utils
from skimage import data
import numpy as np


def test_rotated_image() -> None:
    """Test rotated_image function."""
    image = data.astronaut()[:300, :, :]
    result = utils.rotated_image(image)
    assert result.shape == image.shape, f"{result.shape} != {image.shape}"
