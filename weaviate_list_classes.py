"""
This script lists all classes in a Weaviate database.
Configure the Weaviate instance credentials at the beginning of the script.
Ensure you have the `weaviate-client` library installed to run this script.
"""

import weaviate
from weaviate.auth import AuthApiKey

import os

# Configuration: Weaviate instance credentials from environment variables
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

def create_weaviate_client(host, api_key):
    """
    Creates and returns a Weaviate client.
    
    :param host: The host URL of the Weaviate instance.
    :param api_key: The API key for authentication.
    :return: A Weaviate client object.
    """
    return weaviate.Client(
        url=host,
        auth_client_secret=AuthApiKey(api_key=api_key),
    )

def fetch_classes(client):
    """
    Fetches and returns all classes from a Weaviate schema.
    
    :param client: The Weaviate client.
    :return: A list of class names.
    """
    schema = client.schema.get()
    return schema.get('classes', [])

def print_classes(classes):
    """
    Prints the list of classes with a color gradient.
    
    :param classes: A list of class dictionaries.
    """
    if classes:
        print_with_gradient("\n\nExisting classes in the Weaviate database:", '\033[92m', '\033[94m')  # Green to Blue
        for cls in classes:
            print(f"\033[92m- {cls['class']}\033[0m\n\n")
    else:
        print_with_gradient("\n\nNo classes found in the Weaviate database.", '\033[94m', '\033[92m')  # Blue to Green

def print_with_gradient(text, start_color, end_color):
    """
    Prints the given text with a gradient effect from start_color to end_color.
    This is a simplified version that alternates between two colors for demonstration.
    
    :param text: The text to print with gradient.
    :param start_color: The ANSI escape code for the start color.
    :param end_color: The ANSI escape code for the end color.
    """
    colors = [start_color, end_color]
    gradient_text = ''.join([colors[i % len(colors)] + char for i, char in enumerate(text)])
    gradient_text += '\033[0m'  # Reset color at the end
    print(f"{gradient_text}\n\n")

def main():
    """
    Main function to list all classes in a Weaviate database.
    """
    client = create_weaviate_client(WEAVIATE_HOST, WEAVIATE_API_KEY)
    classes = fetch_classes(client)
    print_classes(classes)

if __name__ == "__main__":
    main()
