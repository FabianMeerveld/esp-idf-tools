import os
import argparse
import shutil
import subprocess

def install_idf():
    # Check if the ESP-IDF is already installed
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    if os.path.exists(os.path.join(parent_dir, "esp-idf-v5.3")):
        print("ESP-IDF is already installed.")
        return

    # Change the current working directory to the parent directory
    os.chdir(parent_dir)
    print(f"Changed working directory to {parent_dir}")
    
    # Define the ESP-IDF repository URL and branch
    esp_idf_repo_url = "https://github.com/espressif/esp-idf.git"
    esp_idf_branch = "v5.3"
    esp_idf_dir = "esp-idf-v5.3"

    # Clone the ESP-IDF repository
    subprocess.run(["git", "clone", "-b", esp_idf_branch, "--recursive", esp_idf_repo_url, esp_idf_dir], check=True)
    os.chdir(esp_idf_dir)
    subprocess.run(["install.bat"], check=True)

    # Modify the uart.h file in the ESP-IDF
    uart_header_path = os.path.join(parent_dir, esp_idf_dir, "components", "esp_driver_uart", "include", "driver", "uart.h")
    modify_uart_header(uart_header_path)

    print("Testting the installation")
    test()
    print("ESP-IDF v5.3 installed successfully.")

def modify_uart_header(file_path):
    # Read the contents of the uart.h file
    with open(file_path, 'r') as file:
        content = file.readlines()

    lines_to_add = [
        "    };\n",
        "    struct \n",
        "    {\n",
        "        bool backup_before_sleep;\n",
        "    } flags;\n"
    ]

    # Find the position to insert the new lines
    insert_position = None
    for i, line in enumerate(content):
        if '};' in line:
            insert_position = i
            break

    if insert_position is None:
        raise ValueError("Could not find the insertion point in uart.h")

    # Insert the new lines before the final '};'
    content = content[:insert_position] + lines_to_add + content[insert_position:]

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(content)

    print(f"Modified {file_path} successfully.")

# Need to add setting it fully up
def add_component(arg):
    # Check if the "main" folder exists in the current directory
    if not os.path.exists("main"):
        print("Error: 'main' folder does not exist in the current directory.")
        return

    # Ensure "components" folder exists
    components_folder = "components"
    if not os.path.exists(components_folder):
        os.makedirs(components_folder)
        print(f"Created 'components' folder.")

    # Check if the argument is a Git URL or a file path
    if arg.startswith("http://") or arg.startswith("https://") or arg.startswith("git@"):
        # It's a Git URL
        repo_name = arg.split('/')[-1].replace('.git', '')
        destination = os.path.join(components_folder, repo_name)
        print(f"Cloning repository: {arg} into {destination}")
        try:
            subprocess.run(["git", "clone", arg, destination], check=True)
            print(f"Successfully cloned {repo_name} into 'components' folder.")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e}")
    else:
        # It's a file path
        if not os.path.exists(arg):
            print(f"Error: File or directory {arg} does not exist.")
            return

        destination = components_folder
        if os.path.isfile(arg):
            # If it's a file, copy it
            shutil.copy(arg, destination)
            print(f"Copied file {arg} to {destination}.")
        elif os.path.isdir(arg):
            # If it's a directory, copy it recursively
            component_name = os.path.basename(arg)
            shutil.copytree(arg, os.path.join(destination, component_name))
            print(f"Copied directory {arg} to {destination}.")
        else:
            print("Error: Argument is neither a file nor a directory.")

def test():
    print("Test function called.")
    subprocess.run(["idf.py", "--version"],shell=True ,check=True)

def create_project(name):
# Check if the project name is valid    
    if not name.isidentifier():
        print("Error: Project name is not a valid identifier.")
        return


def main():
    parser = argparse.ArgumentParser(description="Tool for managing projects and components.")
    
    parser.add_argument("command", choices=["add-component", "install-idf", "test", "create-project"], 
                        help="Command to execute")
    parser.add_argument("arg", help="Argument for the command", nargs='?')  # Optional argument
    
    args = parser.parse_args()

    if args.command == "add-component":
        if args.arg:
            add_component(args.arg)
        else:
            print("Error: 'add-component' requires a git link or file path argument.")
    elif args.command == "install-idf":
        install_idf()
    elif args.command == "test":
        test()
    elif args.command == "create-project":
        if args.arg:
            create_project(args.arg)
        else:
            print("Error: 'create-project' requires a project name argument.")
    
if __name__ == "__main__":
    main()
