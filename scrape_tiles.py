import requests
import numpy
import json


"""
    The map boundaries,
"""

Y_b = 5845026.33  # y bottom
Y_t = 6229876.43  # y top
X_l = 1061781.78  # x left
X_r = 1907647.03  # x right

url = "https://app.wigeogis.com/kunden/tmobile/data/geoserver.php?d=&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng8&TRANSPARENT=false&LAYERS=tmobile%3Atmobile&STYLES=tmobile%3Atma_5g&srs=EPSG%3A900913&WIDTH=256&HEIGHT=256&CRS=EPSG%3A3857&BBOX={}"

im_size = 256
im_size_to_coord_coeff = 19.105468
iter_size = im_size * im_size_to_coord_coeff
points_fmap = []
points = []

for x in numpy.arange(X_l, X_r, iter_size):
    for y in numpy.arange(Y_b, Y_t, iter_size):
        points.append([x, y, x + iter_size, y + iter_size])

session = requests.session()
count = 0

for i in points:
    bbox = ",".join([str(j) for j in i])
    box_name = "x".join([str(j) for j in i])
    points_fmap.append({"bbox": bbox, "fname": box_name})
    r = session.get(url.format(bbox))
    with open(f"out/{box_name}.png", "wb") as file:
        file.write(r.content)
        file.close()
    count += 1

    if count >= 40:
        break

with open("bboxmap.json", "w") as f:
    json.dump(points_fmap, f)
    f.close()

print("scraped the images checkout!")
