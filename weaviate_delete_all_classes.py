import weaviate
from weaviate.auth import AuthApiKey
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def initialize_client(credentials):
    """Initialize and return a Weaviate client."""
    return weaviate.Client(
        url=credentials["host"],
        auth_client_secret=AuthApiKey(api_key=credentials["api_key"]),
    )

def fetch_classes(client):
    """Fetch and return classes from the Weaviate schema."""
    schema = client.schema.get()
    return schema.get('classes', [])

def confirm_deletion(class_name):
    """Prompt user for confirmation before deletion."""
    user_input = input(f"\n{Fore.YELLOW}Do you really want to delete the class '{class_name}'? (yes/no): {Style.RESET_ALL}").strip().lower()
    return user_input == 'yes'

def delete_classes(client, classes):
    """Delete classes from Weaviate schema after user confirmation."""
    if not classes:
        print(f"\n{Fore.BLUE}No classes found in the Weaviate database. No action taken.{Style.RESET_ALL}\n")
        return

    print(f"\n{Fore.WHITE}Classes to be deleted:{Style.RESET_ALL}\n")
    for cls in classes:
        print(f"{Fore.BLUE}- {cls['class']}{Style.RESET_ALL}")

    print(f"\n{Fore.WHITE}Starting deletion process...\n{Style.RESET_ALL}")
    for cls in classes:
        class_name = cls['class']
        if confirm_deletion(class_name):
            try:
                client.schema.delete_class(class_name)
                print(f"\n{Fore.GREEN}Successfully deleted class '{class_name}'.{Style.RESET_ALL}\n")
            except Exception as e:
                print(f"\n{Fore.RED}Failed to delete class '{class_name}': {e}{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}Deletion of class '{class_name}' skipped.{Style.RESET_ALL}\n")

def get_credentials():
    """Prompt user for Weaviate credentials and return them."""
    host = input("\nEnter Weaviate host URL: ").strip()
    api_key = input("Enter API key: ").strip()
    return {"host": host, "api_key": api_key}

def main():
    credentials = get_credentials()
    client = initialize_client(credentials)
    classes = fetch_classes(client)
    delete_classes(client, classes)

if __name__ == "__main__":
    main()



