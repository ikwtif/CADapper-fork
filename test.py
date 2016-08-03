import json

print("loading settings -- change path?/chose path?")
with open("folders.txt","r")as f:
    settings = json.load(f)

print(settings)

print(settings['8888']['path'])
