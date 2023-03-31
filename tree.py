import requests
import openai
import json
from openai import ChatCompletion
import os
import json

# Set up your API keys
TREE_API_TOKEN = "420420420420420420420420420420420420"
OPENAI_API_KEY = "6969696969696969696969696969696969696969"

# Configure the OpenAI API
openai.api_key = OPENAI_API_KEY

# Replace with your desired tree
TREE_OWNER = "tree_owner"
TREE_NAME = "tree_name"

# Read the tree structure of a GitHub tree using the GitHub API
def read_tree_structure(tree_owner, tree_name):
    url = f"https://{tree_owner}/{tree_name}recursive=1"
    headers = {"Authorization": f"token {TREE_API_TOKEN}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    return data["tree"]

# Summarize the tree structure using GPT-4 API
def summarize_folder_structure(tree, tree_type):
    folders = {}
    for item in tree:
        if item["type"] == "tree" and not item["path"].startswith(".next") and not item["path"].startswith("node_modules"):
            folders[item["path"]] = []

    for item in tree:
        if item["type"] == "blob":
            for folder in folders.keys():
                if item["path"].startswith(folder) and not item["path"].startswith(".next") and not item["path"].startswith("node_modules"):
                    folders[folder].append(item["path"])

    folder_summary = "Folder structure:\n\n"
    for folder, files in folders.items():
        folder_summary += f"{folder}:\n"
        for file in files:
            folder_summary += f"  - {file}\n"
        folder_summary += "\n"

    prompt = f":\n\n{folder_summary}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        
        messages=[{"role": "system", "content": ""},
                  {"role": "user", "content": f":{folder_summary}"}],
        max_tokens=4096,
        n=1,
        stop=None,
        temperature=0.8,
    )

    summary = response['choices'][0]['message']['content'].strip()
    return summary

# Main function that runs when you trigger the program, takes in user info to help generate
def main():
    # Check if the JSON file exists
    if os.path.exists('user_input.json'):
        with open('user_input.json', 'r') as f:
            user_input = json.load(f)
            # Get user input for tree owner and name
            tree_owner = "irvineAlgotrading"
            tree_name = "openai"
            tree_type = "nextjs app"
    else:
        # Get user input for tree owner and name
        tree_owner = "irvineAlgotrading"
        tree_name = "openaisf"
        tree_type = "nextjs app"

    # Save the user input to a JSON file
    user_input = {
        'tree_owner': tree_owner,
        'tree_name': tree_name,
        'tree_type': tree_type
    }
    with open('user_input.json', 'w') as f:
        json.dump(user_input, f)

    tree = read_tree_structure(tree_owner, tree_name)
    if tree is not None:
        summary = summarize_folder_structure(tree, tree_type)
        print(":", summary, "\n")
        print("")
         # Combine the print statements into a single string
        combined_text = f": {summary}\n\n "
        
        # Save the combined text to a JSON file
    if os.path.exists('summary.json'):
            with open('summary.json', 'w') as f:
                json.dump({"summary": combined_text}, f)

if __name__ == "__main__":
    main()