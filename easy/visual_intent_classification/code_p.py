import os
import base64
from PIL import Image
import io
from transformers import AutoProcessor, AutoModelForZeroShotImageClassification
import torch
from typing import List


class ImageProcessor:
    """
    A class for processing images.

    Attributes:
        image_path (str): The path to the image.
    """
    def __init__(self, image_path: str):
        """
        Initialize an ImageProcessor instance.

        Parameters:
            image_path (str): The path to the image.

        Raises:
            ValueError: If the image path is empty.
        """
        if not image_path:
            raise ValueError("Image path is empty." )
        if not os.path.exists(image_path):
            raise ValueError("Image file does not exist at the provided path.")
        self.image_path = image_path

    def prepare_image(self) -> Image.Image:
        """
        Method to prepare the image for processing.

        Returns:
            Image.Image: The prepared image.
        """
        # try:
        #     # Open the image
        #     with Image.open(self.image_path) as image:
        #         buffered = io.BytesIO()
        #         image.save(buffered, format=image.format)
        #         image_bytes = buffered.getvalue()
        #
        #         encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        #
        #     return encoded_image
        try:
            # Open the image and return it directly
            image = Image.open(self.image_path)
            return image

        except IOError as e:
            raise IOError(f"Unable to process the image: {e}")


class ClipModel:
    """
    A class for working with a classification model.

    Attributes:
        model (CLIPModel): The CLIP model instance.
        processor (CLIPProcessor): The CLIP processor instance.
    """
    def __init__(self):
        """
        Initialize a ClipModel instance.
        """
        # Load model directly
        self.model = AutoModelForZeroShotImageClassification.from_pretrained("yujiepan/clip-vit-tiny-random-patch14-336")
        self.processor = AutoProcessor.from_pretrained("yujiepan/clip-vit-tiny-random-patch14-336")

    def classify(self, image: Image.Image, intents: list) -> list:
        """
        Method for classifying data.

        Parameters:
            image (Image.Image): The image to classify.
            intents (list): The list of text categories.

        Returns:
            list: The classification result as probability distribution.
        """
        inputs = self.processor(text=intents, images=image, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Extract scores and normalize them to probabilities
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        return probs[0].detach().numpy().tolist()


class ImageClassifier:
    """
    A class for classifying images.

    Attributes:
        clip_model (ClipModel): An object for data classification.
        intents (List[str]): A list of categories for classification.
    """

    def __init__(self):
        """
        Initialize an ImageClassifier instance.
        """
        self.clip_model = ClipModel()  # Initialize the ClipModel
        self.intents = ["payment-problem", "course-problem", "profile-problem"]

    def classify_intent(self, image_path: str) -> str:
        """
        Method for classifying intent.

        Parameters:
            image_path (str): The path to the image.

        Returns:
            str: The category of intent.
        """
        image = ImageProcessor(image_path)
        prepared_image = image.prepare_image()

        probs = self.clip_model.classify(prepared_image, self.intents)
        max_index = probs.index(max(probs))

        # Return the corresponding intent
        return self.intents[max_index]
