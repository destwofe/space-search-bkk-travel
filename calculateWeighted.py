import json

taxiNodes = json.load(open('data/nodes-taxi.json'))
btsNodes = json.load(open('data/nodes-bts.json'))
aprNodes = json.load(open('data/nodes-apr.json'))
mrtNodes = json.load(open('data/nodes-mrt.json'))

total_duration = 0
total_cost = 0

for dataNode in taxiNodes:
  total_duration += float(dataNode['duration'])
  total_cost += float(dataNode['cost'])

for dataNode in btsNodes:
  total_duration += float(dataNode['duration'])
  total_cost += float(dataNode['cost'])

for dataNode in aprNodes:
  total_duration += float(dataNode['duration'])
  total_cost += float(dataNode['cost'])

for dataNode in mrtNodes:
  total_duration += float(dataNode['duration'])
  total_cost += float(dataNode['cost'])

print(total_duration, total_cost)
print(total_cost/total_duration)
print(total_duration/total_cost)
