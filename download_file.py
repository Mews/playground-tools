if __name__ == "__main__":
    from getpass import getpass
    import json
    import requests
    import os

    from utils import get_headers, run_command

    msg = "This app is used to download a file from the playground servers"

    print("-"*len(msg)+"\n"+msg+"\n"+"-"*len(msg)+"\n")

    username = input("Username:")
    password = getpass(prompt="Password:")
    print("Getting request headers...")
    HEADERS = get_headers(username, password)

    file_name = input("File:")
    download_path = "downloads/"+file_name

    print("Uploading file to file.io...")
    
    output = run_command(f'curl -F "file=@{file_name}" https://file.io', HEADERS)

    download_url = json.loads(output)["link"]

    print(f"File uploaded to {download_url}")
    print("Downloading file...")

    download_bytes = requests.get(download_url).content

    print(f"Downloaded file ({len(download_bytes)} bytes)")
    print(f"Saving file to downloads/{file_name}...")

    if not os.path.exists(download_path) and os.path.dirname(download_path):
        os.makedirs(os.path.dirname(download_path), exist_ok=True)

    with open(download_path, "wb") as f:
        f.write(download_bytes)