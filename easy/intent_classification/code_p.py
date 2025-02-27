from sentence_transformers import SentenceTransformer
from typing import List
import torch


def init_sentence_encoder(model_name: str = 'cointegrated/rubert-tiny2') -> SentenceTransformer:
    """
    Initialize a SentenceTransformer model for encoding sentences.

    Parameters:
        model_name (str): The name of the model to load. Default is 'cointegrated/rubert-tiny2'.
            Model names can be found at the Hugging Face model hub: https://huggingface.co/models

    Returns:
        SentenceTransformer: An initialized SentenceTransformer model.

    Raises:
        ValueError: If the model name is empty.
        RuntimeError: If the model fails to load.
    """
    if not model_name:
        raise ValueError("Model name is empty")
    try:
        model = SentenceTransformer(model_name)
    except Exception as e:
        raise RuntimeError(f"Failed to load the model '{model_name}': {e}")
    return model


class Route:
    """
    A class representing a route, which consists of a name and a list of sentences.

    Attributes:
        name (str): The name of the route.
        sentences (List[str]): A list of sentences representing the route.
        embeddings (torch.Tensor): Embeddings of the sentences generated by the SentenceTransformer.
    """

    def __init__(self, name: str, sentences: List[str]):
        """
        Initialize a Route instance.

        Parameters:
            name (str): The name of the route.
            sentences (List[str]): A list of sentences for the route.

        Raises:
            ValueError: If the route name is empty or the sentences list is empty or contains empty sentences.
            RuntimeError: If there is an error encoding the sentences.
        """
        if not name:
            raise ValueError("Route name cannot be empty.")
        if not sentences:
            raise ValueError("Sentences list cannot be empty.")
        if any(not sentence for sentence in sentences):
            raise ValueError("Sentences list cannot contain empty sentences.")

        self.name = name
        self.sentences = sentences
        model = init_sentence_encoder()
        try:
            self.embeddings = torch.tensor(model.encode(sentences))
        except Exception as e:
            raise RuntimeError(f"Error encoding sentences: {e}")


class SemanticRouter:
    """
    A class representing a semantic router for classifying user intents.
    """

    def __init__(self, routes: List[Route]):
        """
        Initialize a SemanticRouter instance.

        Parameters:
            routes (List[Route]): A list of Route objects.
        """
        self.routes = routes

    def classify_intent(self, user_input: str, similarity_threshold: float = 0.8) -> str:
        """
        Classify the intent of a user input by comparing it to predefined routes.

        Parameters:
            user_input (str): The user's input to classify.
            similarity_threshold (float): The threshold for similarity to consider a match. Default is 0.8.

        Returns:
            str: The name of the best matching route if the similarity exceeds the threshold, otherwise None.
        """
        model = init_sentence_encoder()
        try:
            user_embedding = torch.tensor(model.encode([user_input]))
        except Exception as e:
            raise RuntimeError(f"Error encoding sentences: {e}")

        best_match = None
        highest_similarity = 0.0

        for route in self.routes:
            similarities = torch.nn.functional.cosine_similarity(user_embedding, route.embeddings)
            max_similarity = similarities.max().item()

            if max_similarity > highest_similarity and max_similarity >= similarity_threshold:
                highest_similarity = max_similarity
                best_match = route.name

        return best_match
