import os
import weaviate
from weaviate.auth import AuthApiKey

# Configuration Options
# ---------------------
# Name of the index to be used in Weaviate
index_name = "documents"
# Dimension of the embeddings (e.g., 1536 for OpenAI embeddings)
dimension = 1536
# Credentials for Weaviate instance from environment variables
credentials = {
    "host": os.getenv("WEAVIATE_HOST"),  # Weaviate instance URL from environment variable
    "api_key": os.getenv("WEAVIATE_API_KEY"),  # API key for authentication from environment variable
}

class BaseEncoder:
    # Placeholder for the base encoder class
    pass

class DummyEncoder(BaseEncoder):
    def encode(self, text):
        # Implement your encoding logic here
        return [0] * dimension  # Adjusted for OpenAI embeddings

class WeaviateService:
    def __init__(self, index_name: str, dimension: int, credentials: dict, encoder: BaseEncoder):
        super().__init__()
        self.client = weaviate.Client(
            url=credentials["host"],
            auth_client_secret=AuthApiKey(api_key=credentials["api_key"]),
        )
        self.index_name = index_name
        self.ensure_class()

    def delete_existing_class(self):
        """Deletes the class if it exists."""
        if self.client.schema.exists(self.index_name):
            print(f"\033[92m\n\nDeleted existing class \033[94m'{self.index_name}'\033[92m\n\033[0m")
            self.client.schema.delete_class(self.index_name)
            

    def create_class(self, schema):
        """Creates a new class with the given schema."""
        self.client.schema.create_class(schema)
        print(f"\033[92m\nCreated class \033[94m'{self.index_name}'\033[92m with the provided schema.\n\n\033[0m")

    def ensure_class(self):
        """Ensures the class is deleted if exists, then creates a new one."""
        self.delete_existing_class()  # Delete the class if it exists
        # Define the schema
        schema = {
            "class": self.index_name,
            "properties": [{"name": "text", "dataType": ["text"]}],
        }
        self.create_class(schema)  # Create a new class with the schema

    def list_classes(self):
        """Lists all classes in the Weaviate schema."""
        schema = self.client.schema.get()
        classes = schema.get('classes', [])
        if classes:
            print("\n\nExisting classes in the Weaviate database:")
            for cls in classes:
                print(f"- {cls['class']}\n\n")
        else:
            print("No classes found in the Weaviate database.")

encoder = DummyEncoder()

# Initialize WeaviateService
weaviate_service = WeaviateService(index_name, dimension, credentials, encoder)

# List existing classes after operations
weaviate_service.list_classes()