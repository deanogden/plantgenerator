import json
import os
import pandas as pd

#Start XL Function


def get_value_from_excel(domain_name, excel_file='your_file.xlsx', sheet_name='totals', header_values=''):
    """
    Retrieves the corresponding value from an Excel sheet based on the given domain_name.

    Args:
        domain_name (str): The domain name to search for.
        excel_file (str): Path to the Excel file (default: 'your_file.xlsx').
        sheet_name (str): Name of the sheet containing the data (default: 'totals').

    Returns:
        str: The corresponding value for the given domain_name, or None if not found.
    """
    try:
        # Read the data into a pandas DataFrame
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Filter the DataFrame based on the domain_name
        filtered_df = df[df['Domain'] == domain_name]

        values_dict = {}
        if not filtered_df.empty:
            for header in header_values:
                if header in filtered_df.columns:
                    values_dict[header] = filtered_df[header].iloc[0]
                else:
                    print(f"Column '{header}' not found in the data.")
        return values_dict

        if not filtered_df.empty:
            #corresponding_value = filtered_df['values'].iloc[0]
            return data[domain_name]
        else:
            print(f"No data found for domain '{domain_name}'")
            return None
    except FileNotFoundError:
        print(f"Excel file '{excel_file}' not found.")
        return None
    
#End XL Function

file_path = "C:\\temp\\output.txt"
config_path = "C:\\users\\ICON0375\\Documents\\python\\"
#json_path = config_path + "test.json"
json_path = config_path + "small.json"
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


# Check if the file exists CURRENTLY Redundant
if not os.path.exists(file_path):
    # Create the file if it doesn't exist
    with open(file_path, 'w') as file:
        file.write('')

with open(json_path, 'r') as file: data = json.load(file)

enterprise_domain_name= data["Enterprise Domain"]["Name"] 
architecture_domains= data["Enterprise Domain"]["Architecture Domain"]
print(f"Domain Name: {enterprise_domain_name}")
print(f"{prefix} {enterprise_domain_name} {postfix}")
print(f"Archictecture Domain Names: ")

output_string = puml_header + "\n"
output_string += prefix + f'"{enterprise_domain_name}"' + postfix_business_function + " \n"
for archdomainkey, archdomainvalue in architecture_domains.items(): 

    print (f"Architecture Domain: {archdomainvalue['Name']}")
    print(f"{prefix} {archdomainvalue['Name']} {postfix_business_service}") 
    domain_prefix = archdomainvalue['Name'][:3]
    print(f"domain prefix: {domain_prefix}")
    output_string += prefix + f'"' + archdomainvalue['Name'] + f'"' + postfix_business_service + " \r \n"
    indents = 1
    sub_domains = archdomainvalue["Sub Domains"]

    if sub_domains:
        indents += 1
        i = 1 
    for subdomainkey, subdomainvalue in sub_domains.items(): 

        print(f"Sub Domains: {subdomainvalue['Name']}")
        print(f"{prefix} {subdomainvalue['Name']} {postfix}")
        output_string += "\t" * (indents) + prefix + f'"' + subdomainvalue['Name'] + f'"' + postfix_business_service + " \r \n"
        
        if "Tags" in subdomainvalue:

            tags = subdomainvalue["Tags"]
            tag_values = ""

            result = get_value_from_excel(subdomainvalue['Name'],excel_file, 'totals',tags)
            if result:
                print(f"The values for domain '{subdomainvalue['Name']}' is: {result}")
                value_descriptor = subdomainvalue['Tag Description']
                print(f"Value Descriptor is: {value_descriptor}")
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


