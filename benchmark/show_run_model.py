from pprint import pprint

import openml
import pickle
import pandas as pd

OPENML_APIKEY = '8b2cf3aaf752f91c77672b1143d0071b'
# run_id = 9650926
# run = openml.runs.get_run(run_id)

# run_v = vars(run)
# pprint(run_v)

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)  

def load_object(filename):
  with open(filename, 'rb') as inp:
    obj = pickle.load(inp)
  return obj

def list_flows():
  flow_dict = openml.flows.list_flows()
  flow_list = [ f for f in flow_dict.values() ]
  return flow_list

def download_flows(flow_list, file_name):
  index = 0
  flows = []
  for flow_item in flow_list:
    index += 1
    if index % 10 == 1:
      print("Saving %s" % index)
      save_object(flows, file_name)
    flow_id = flow_item["id"]
    try:
      flow = openml.flows.get_flow(flow_id)
      flows.append(flow)
    except Exception as e:
      print('Failed to load : '+ str(flow_id))
 
def list_parameters(flow, component):
  return [ (flow.flow_id, component.name, k, v ) for k,v in component.parameters.items() ]

def flatten_flow(parent):
  r = [parent]
  for child in parent.components.values():
    r.extend(flatten_flow(child))
  return r

def flatten_flow_parameters(parent):
  parameters = [ p for c in flatten_flow(parent) for p in list_parameters(parent, c)]
  return parameters

def build_parameter_frame(parameters):
  rows = {}
  for p in parameters:
    flow_id = p[0]
    component_name = p[1]
    key = (flow_id, component_name)
    name = p[2]
    value = p[3]

    if not key in rows:
      row = {}
      row["parameters"] = name
      row["flow_id"] = flow_id
      row["component_name"] = component_name
      rows[key] = row
    else:
      row = rows[key]
      row["parameters"] = row["parameters"] + "|" + name
    row[name] = value

  row_list = list(rows.values())
  frame = pd.DataFrame(row_list)
  return frame

#flow_list = list_flows()
#download_flows(flow_list, 'benchmark\\flows.pkl')
flows = load_object('benchmark\\flows.pkl')
parameters = [ p for f in flows for p in flatten_flow_parameters(f) ]
frame = build_parameter_frame(parameters)
frame.to_csv("benchmark\\parameters\\parameters.csv", index=False)
