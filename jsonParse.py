import json
import os
import datetime


#Start data match

def get_value_from_data(domain_name, data_file='your_file.xlsx', tags=''):
    """
    Retrieves the corresponding value from an json file based on the given domain_name. Assume this will 
    move to an API json response payload from Waltz.

    Args:
        domain_name (str): The domain name to search for.
        header_values: The Tags header values to pull out
    Returns:
        str: The corresponding value for the given domain_name, or None if not found.
    """
    try:
        # Check if the file exists CURRENTLY Redundant for use as output file
        if os.path.exists(data_file):
            #C:\Users\deano\vscode\python\CIOnPage\data.json
            with open(data_file, 'r') as data_file: data_content = json.load(data_file)
            
        #corresponding_value = filtered_df['values'].iloc[0]
            for item in data_content:
                if item['Domain'] == domain_name:
                    result = {key: value for key, value in item.items() if key in tags}
                    return result
        else:
            print(f"No data found for domain '{domain_name}'")
            return None
    except FileNotFoundError:
        print(f"Data file '{data_file}' not found.")
        return None
def generate_unique_file_name():
    # Get the current date and time
    now = datetime.datetime.now()
    
    # Format the date and time as ddmmyyhhmmss
    unique_id = now.strftime("%d%m%y%H%M%S")
    
    return unique_id
def save_puml_to_file(file_name, puml_content):
    """
    Saves the given text content to a file if it doesn't already exist.

    Args:
        file_name (str): The name of the file.
        puml_content (str): The text content to save in the file.

    Returns:
        str: A message indicating whether the file was created or already exists.
    """
    # Check if the file already exists
    if os.path.exists(file_name):
        return f"The file '{file_name}' already exists."
    else:
        # Create the file and write the text content to it
        with open(file_name, 'w') as file:
            file.write(puml_content)
        return f"The file '{file_name}' has been created and the content has been saved."


unique_id = generate_unique_file_name()
#print(unique_id)

puml_file = "C:\\temp\\" +  unique_id + "output.puml"
config_path = "C:\\users\\deano\\vscode\\python\\CIOnPage\\"
#data_path = "C:\\users\\deano\\vscode\\python\\CIOnPage\\"
json_path = config_path + "test.json"
#Assume that data will eventually be an API
data_file = config_path + "data.json"
#json_path = config_path + "small.json"
excel_file = config_path + "env_data.xlsx"
tag_values = ""
indents = 0
output_string = ""
domain_prefix = ""
end_puml = "@enduml"
puml_header = """@startuml test


skinparam rectangle<<behavior>> {
	roundCorner 25
}
!include <archimate/Archimate>
skinparam shadowing true
sprite $bProcess jar:archimate/business-process
sprite $bService jar:archimate/business-service
sprite $bFunction jar:archimate/business-function
sprite $bActor jar:archimate/business-actor
sprite $bActivity jar:archimate/business-activity
sprite $aService jar:archimate/application-service
sprite $aComponent jar:archimate/application-component
sprite $bCapability jar:archimate/strategy-capability

header
Test One view
endheader
"""

prefix = """ rectangle """
postfix = " <<$archimate/application-component>> #Business{ "
postfix_business_function = "<<$bFunction>> #Business{"
postfix_business_service = "<<$bService>> #Business{"
postfix_application = "<<$aComponent>> #Application"


with open(json_path, 'r') as file: data = json.load(file)

enterprise_domain_name= data["Enterprise Domain"]["Name"] 
architecture_domains= data["Enterprise Domain"]["Domain Group"]
#print(f"Domain Name: {enterprise_domain_name}")
#print(f"{prefix} {enterprise_domain_name} {postfix}")
#print(f"Archictecture Domain Names: ")

output_string = puml_header + "\n"
output_string += prefix + f'"{enterprise_domain_name}"' + postfix_business_function + " \n"
for archdomainkey, archdomainvalue in architecture_domains.items(): 

    #print (f"Architecture Domain: {archdomainvalue['Name']}")
    #print(f"{prefix} {archdomainvalue['Name']} {postfix_business_service}") 
    domain_prefix = archdomainvalue['Name'][:3]
    #print(f"domain prefix: {domain_prefix}")
    output_string += prefix + f'"' + archdomainvalue['Name'] + f'"' + postfix_business_service + " \r \n"
    indents = 1
    sub_domains = archdomainvalue["Domains"]

    if sub_domains:
        indents += 1
        i = 1 
    for subdomainkey, subdomainvalue in sub_domains.items(): 

        #print(f"Sub Domains: {subdomainvalue['Name']}")
        #print(f"{prefix} {subdomainvalue['Name']} {postfix}")
        output_string += "\t" * (indents) + prefix + f'"' + subdomainvalue['Name'] + f'"' + postfix_business_service + " \r \n"
        
        if "Tags" in subdomainvalue:

            tags = subdomainvalue["Tags"]
            tag_values = ""

            result = get_value_from_data(subdomainvalue['Name'],data_file,tags)
            if result:
                #print(f"The values for domain '{subdomainvalue['Name']}' is: {result}")
                value_descriptor = subdomainvalue['Tag Description']
                #print(f"Value Descriptor is: {value_descriptor}")
                for key, value in result.items():
                    tag_values += f'{key} : {value}' + """\\n"""            
                output_string += "\t" * (indents) + prefix + f'" <b>' + value_descriptor + '</b> \\n' + tag_values + f'" ' +  f'As {domain_prefix}{i}' + f' ' + postfix_application + " \n"
                
            else:
                print("No matches")
                tag_values = "Value Not specified"
                output_string += "\t" * (indents) + prefix + f'"' + tag_values + f'" ' +  f'As {domain_prefix}{i}' + f' ' + postfix_application + " \n"
            i += 1
        else:
            print("No tags found for this subdomain.")
        
        output_string += "\t" * (indents) + "} \n"
    for i in range(indents -1):
            output_string += "\t" * (indents - 1) + "} \n "
output_string += end_puml

print(output_string) 
#write to unique file in temp folder
save_puml_to_file(puml_file,output_string)




