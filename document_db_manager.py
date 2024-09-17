import os # for file operations
import shutil # for file operations

# Global Variables
root_dir = "docDB"
intake_dir = "docTemp"

# setup_db() - creates the root directory if it does not exist and the intake directory
def setup_db():
    if not os.path.exists(intake_dir):
        os.makedirs(intake_dir)
        print("Intake directory created")
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
        print("Root directory created")

# Function to check if a file is properly named
def check_file(file_name):
    parts = file_name.split(".")
    return len(parts) == 4

# Funtion to get the case ID from the file name
def get_case_id(file_name):
    parts = file_name.split(".")
    return parts[0]

# Function to get the year from the file name
def get_year(file_name):
    parts = file_name.split(".")
    return parts[2]

# Function to generate the document path
def gen_doc_path(root, case_id, year):
    return os.path.join(root, case_id, year)

# Function to copy a file from intakeFolder to its correct document folder in rootFolder
def store_doc(intake_folder, file, root_folder):
    if not check_file(file):
        return False
    
    case_id = get_case_id(file)
    year = get_year(file)
    doc_path = gen_doc_path(root_folder, case_id, year)
    
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
        
    copy_path = os.path.join(intake_folder, file)
    paste_path = os.path.join(root_folder, file)
    
    shutil.copy2(copy_path, paste_path)

    if os.path.exists(paste_path) and os.path.getsize(copy_path) == os.path.getsize(paste_path):
        return True
    else:
        return False

# Function to copy all files from intakeFolder to the correct folder underneath rootFolder
def store_all_docs(intake_folder, root_folder):
    files = os.listdir(intake_folder)
    processed_count = 0
    not_processed = []
    
    for file in files:
        if store_doc(intake_folder, file, root_folder):
            os.remove(os.path.join(intake_folder, file))
            processed_count += 1
        else:
            not_processed.append(file)
    print("Processed: ", processed_count)
    if not_processed:
        print("Not processed: ", not_processed)
  
# Function to reset the root folder
def reset_db(root):
    for item in os.listdir(root):
        item_path = os.path.join(root, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
              
# Main function to demonstrate that the functions are working
def main():
    
        
    setup_db()
    
    if not os.path.exists(intake_dir) or not os.path.exists(root_dir):
        raise Exception("Either the intakeDir or rootDir does not exist. Aborting.")
    
    test_files = ["MA3324-SF-0722.Hiolis.2022.pptx", "MA3324.SF.0722.Hiolis.OrgChart.2022.pptx", "DE33452-1123.NewEnglandRoofing.2020.pdf"]
    for file in test_files:
        open(os.path.join(intake_dir, file), 'a').close()
    
    print("Files in intake folder before processing:")
    print(os.listdir(intake_dir))
    
    store_all_docs(intake_dir, root_dir)
    
    print("Files in intake folder after processing:")
    print(os.listdir(intake_dir))
    
    print("Files in root folder:")
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            print(os.path.join(root, name))
    
    reset_db(root_dir)
    
    print("Files in root folder after resetting:")
    print(os.listdir(root_dir))

# Run the main function
if __name__ == "__main__":
    main()
