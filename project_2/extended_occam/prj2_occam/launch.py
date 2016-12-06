import os
import json
from occam import Occam

# Load OCCAM information
object = Occam.load()

# Gather paths
scripts_path    = os.path.dirname(__file__)
job_path        = os.getcwd()
object_path = "/occam/%s-%s" % (object.id(), object.revision())
# Path to your executable
executable_path="project_2/tomsim.py"

#########################################################
#                                                       #
#           OCCAM gives us the configuration            #
#                                                       #
#########################################################
input_configurations_path = object.configuration_file("Configuration Options")


#########################################################
#                                                       #
#       The only input is the executable file           #
#                                                       #
#########################################################
# Set default input file
default_input_file_path="dummy_program/input.txt"
input_file_path=os.path.join(object_path,default_input_file_path)
## Check if user gave us a new file
inputs = object.inputs("trace")
if len(inputs) > 0:
    files = inputs[0].files()
    if len(files) > 0:
        input_path = inputs[0].files()[0]
    else:
        temp_input_path = os.path.join(inputs[0].volume(),"output.trace")
        if os.path.exists(temp_input_path):
            input_path=temp_input_path
#########################################################
#                                                       #
#  The output goes in this directory(see object.json)   #
#                                                       #
#########################################################
# Output file dir and path
output_dir_path="new_output"
output_file_path=os.path.join(output_dir_path,"statistics.json")
# Create dir and set full path
output_dir_full_path = os.path.join(object.path(), output_dir_path)
if not os.path.exists(output_dir_full_path):
    os.mkdir(output_dir_full_path);
output_full_path = os.path.join(object.path(), output_file_path)

#########################################################
#                                                       #
#                   Build run command                   #
#                                                       #
#########################################################
executable=os.path.join(object_path,executable_path)
print input_configurations_path
args=["python3",
    executable,
    input_file_path,
    input_configurations_path,
    output_full_path
]
command = ' '.join(args)
Occam.report(command)
