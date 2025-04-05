from datetime import datetime as dt
import wget
import os

repository_url = input("Enter URL repository: ")
dir_path = input("Enter path dirrectory: ")
version = input(float("Enter version product: "))


file_name = wget.download(repository_url)

if