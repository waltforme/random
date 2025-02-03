from huggingface_hub import snapshot_download

# Define target directories
adapters = {
    "sikoraaxd/Qwen2-0.5B-Instruct-ru-lora": "/data/qwen2-ru-lora",
    "SHASWATSINGH3101/QWEN2-0.5-instruct-code": "/data/qwen2-code-lora"
}

for repo, target_dir in adapters.items():
    print(f"Downloading {repo} to {target_dir}...")
    snapshot_download(repo_id=repo, local_dir=target_dir)

print("All adapters downloaded successfully.")
