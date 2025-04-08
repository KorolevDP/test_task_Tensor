import datetime
import git
import json
import os
import shutil
import zipfile


def log(message):
    print(f"{datetime.datetime.now()}: {message}")


def clone_repository(repo_url):
    log(f"Clonning repository{repo_url}...")
    repo_dir = repo_url.split('/')[-1].replace('.git', '')
    if os.path.exists(repo_dir) and os.path.isdir(repo_dir):
        log(f"Folder {repo_dir} exists")
        return repo_dir
    git.Repo.clone_from(repo_url, repo_dir)
    log(f"The repository has been cloned into the directory: {repo_dir}")
    return repo_dir


def clean_directory(repo_dir, source_path):
    log("Cleaning directory..")
    temp_path = os.path.split(source_path)[0]
    finish_path = "".join((repo_dir, temp_path))

    for item in os.listdir(repo_dir):
        item_path = os.path.join(repo_dir, item)
        if os.path.isdir(item_path) and item_path != finish_path:
            shutil.rmtree(item_path)
            log(f"Directory removed: {item_path}")


def create_version_file(source_path, version):
    log("Creating file:  version.json...")
    files = [f for f in os.listdir(source_path) if f.endswith(('.py', '.js', '.sh'))]

    version_info = {
        "name": "hello world",
        "version": version,
        "files": files
    }

    version_file_path = os.path.join(source_path, 'version.json')

    with open(version_file_path, 'w') as version_file:
        json.dump(version_info, version_file, indent=4)

    log(f"File version.json created: {version_file_path}")


def archivation(source_path):
    log("Creating archive ..")

    archive_name = f"{os.path.basename(source_path)}{datetime.datetime.now().strftime('%d%m%Y')}.zip"

    with zipfile.ZipFile(archive_name, 'w') as archive:
        for foldername, subfolders, filenames in os.walk(source_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                archive.write(file_path, os.path.relpath(file_path, source_path))

    log(f"Archive created: {archive_name}")


def main(repo_url, source_path, version):
    repo_dir = clone_repository(repo_url)

    clean_directory(repo_dir, source_path)

    full_source_path = "".join((repo_dir, source_path))

    create_version_file(full_source_path, version)

    archivation(full_source_path)


if __name__ == "__main__":
    # Example using.
    repository_url = "https://github.com/paulbouwer/hello-kubernetes.git"
    relative_source_path = r"\src\app"
    product_version = "25.3000"

    main(repository_url, relative_source_path, product_version)