#!/usr/bin/env python3

import os
import json
import fileinput

DESCRIBE_COMMAND_OUTPUT_FILE = 'nodes.log'
node_properties = {}
ALLOCATED_RESOURCES = 'Allocated resources'
props_to_read = ('Name', ALLOCATED_RESOURCES)


myCmd = 'kubectl describe nodes > ' + DESCRIBE_COMMAND_OUTPUT_FILE
os.system(myCmd)
describe_command_output_file = os.getcwd() + '/' + DESCRIBE_COMMAND_OUTPUT_FILE
lines = open(describe_command_output_file, "r")
node_name_dict = {}
node_name = ""

if lines.__sizeof__() > 0:
    for line in lines:
        if line.startswith("Name"):
            line = line.split(":")
            node_name = line[1].strip()
            if not node_properties.__contains__(node_name):
                node_properties[node_name] = None

            node_name_dict = {line[0].strip(): line[1].strip()}

        elif line.startswith(ALLOCATED_RESOURCES):
            line = lines.__next__()
            resources = ""
            cpu_res = {}
            mem_res = {}
            requests_key = ""
            limits_key = ""

            while not line.startswith("Events"):

                if line.strip().startswith("Resource"):
                    line = line.split()
                    resource_key = line[0]
                    requests_key = line[1]
                    limits_key = line[2]

                elif line.strip().startswith('cpu'):
                    line = line.split()
                    cpu = line[0]
                    cpu_res = {
                                cpu:
                                    {requests_key: line[1]+" "+line[2], limits_key: line[3]+" "+line[4]}
                            }

                elif line.strip().startswith('memory'):
                    line = line.split()
                    mem = line[0]
                    mem_res = {
                        mem:
                            {requests_key: line[1] + " " + line[2], limits_key: line[3] + " " + line[4]}
                    }

                line = lines.__next__() # iterating till events to get all resources

            all_props_of_node = [node_name_dict, cpu_res, mem_res]
            node_properties[node_name] = all_props_of_node


r = json.dumps(node_properties, indent=2)

print(r)

with open('output.json', 'w') as outfile:
    json.dump(node_properties, outfile, indent=2)

