import pacman_dev as pc
import json

lis = [i["id"] for i in pc.get_installed()]

details = {}

for i in lis:
    print(i)
    details[i]= pc.get_info(i)


with open('./temp.json', 'w') as f:
    json.dump(details, f)
