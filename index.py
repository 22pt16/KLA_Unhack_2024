import pandas as pd
import math
import numpy as np

def print_data(file):
    for i in range(len(file)):
        print(file[i])

# Task 1: Read Care Areas from CSV File
def read_care_areas(file_name):
    care_areas = pd.read_csv(file_name, names=['id', 'x1', 'x2', 'y1', 'y2'])
    care_areas = care_areas.to_dict('records')
    return care_areas

# Task 2: Read Meta Data from CSV File
def read_meta_data(file_name):
    meta_data = pd.read_csv(file_name, names=['Main Field Size', 'Sub-Field Size'])
    meta_data = meta_data.to_dict('records')
    return meta_data

# Task 3: Generate Main Fields
def generate_main_fields(care_areas, meta_data):

    main_field_size = float(list(meta_data[1].values())[0])  # Extract the main field size from meta_data
    print(main_field_size)
    main_fields = []

    for care_area in care_areas:
        x1, x2, y1, y2 = care_area['x1'], care_area['x2'], care_area['y1'], care_area['y2']
        area = (y2-y1)*(x2-x1)
        # Calculate the number of main fields in x and y directions
        num_x = int(np.ceil((x2 - x1) / main_field_size))
        num_y = int(np.ceil((y2 - y1) / main_field_size))
        no_mf= np.ceil(area / pow(main_field_size,2))
        #print("No of main field = ",no_mf,num_x,num_y)

       
        for i in range(num_x):
            for j in range(num_y):

                mf_x1 = max(x1, x1 + i * main_field_size)
                mf_y1 = max(y1, y1 + j * main_field_size)
                mf_x2 = min(x2, mf_x1 + main_field_size)
                mf_y2 = min(y2, mf_y1 + main_field_size)

                if mf_x2 > mf_x1 and mf_y2 > mf_y1:  # Check for valid main field
                    main_fields.append({'id': len(main_fields), 'x1': mf_x1, 'x2': mf_x2, 'y1': mf_y1, 'y2': mf_y2})
        
    return main_fields
def generate_main_fields(care_area, meta_data):
    main_field_size = float(list(meta_data[1].values())[0])  # Extract the main field size from meta_data
    print(main_field_size)
    # Define the care area boundaries
    x1, x2, y1, y2 = care_area['x1'], care_area['x2'], care_area['y1'], care_area['y2']

    # Calculate the grid size
    grid_size = main_field_size / 2

    # Initialize a 2D array to store the grid
    num_x = int((x2 - x1) / grid_size)
    num_y = int((y2 - y1) / grid_size)
    grid = [[0 for _ in range(num_y)] for _ in range(num_x)]

    # Mark grid cells within the care area
    for x in range(x1, x2, grid_size):
        for y in range(y1, y2, grid_size):
            # Simple check to see if the grid cell is within the care area
            if (x + grid_size > x1 and x < x2 and
                    y + grid_size > y1 and y < y2):
                xi = int((x - x1) / grid_size)
                yi = int((y - y1) / grid_size)
                grid[xi][yi] = 1

    # Combine adjacent grid cells to form main fields
    main_fields = []
    for i in range(num_x):
        for j in range(num_y):
            if grid[i][j] == 1:
                x = x1 + i * grid_size
                y = y1 + j * grid_size
                main_fields.append({
                    'x1': x,
                    'x2': x + main_field_size,
                    'y1': y,
                    'y2': y + main_field_size
                })

    return main_fields

 
# Task 4: Generate Sub Fields
def generate_sub_fields(main_fields, meta_data):
    sub_fields = []
    sub_field_size = float(list(meta_data[1].values())[1])
   
    for main_field in main_fields:
        x1, x2, y1, y2 = main_field['x1'], main_field['x2'], main_field['y1'], main_field['y2']
        num_x = int(np.ceil((x2 - x1) / sub_field_size))
        num_y = int(np.ceil((y2 - y1) / sub_field_size))
       
        for i in range(num_x):
            for j in range(num_y):
                sf_x1 = x1 + i * sub_field_size
                sf_y1 = y1 + j * sub_field_size
                sf_x2 = sf_x1 + sub_field_size
                sf_y2 = sf_y1 + sub_field_size
                sub_field = {
                    'id': len(sub_fields),
                    'x1': sf_x1,
                    'x2': sf_x2,
                    'y1': sf_y1,
                    'y2': sf_y2,
                    'MF_ID': main_field['id'],
                }
                sub_fields.append(sub_field)
       # print(sub_fields)
    return sub_fields

# Task 5: Write Main Fields to CSV File
def write_main_fields(file_name, main_fields):
    pd.DataFrame(main_fields).to_csv(file_name, index=False, header =False)

# Task 6: Write Sub Fields to CSV File
def write_sub_fields(file_name, sub_fields):
    pd.DataFrame(sub_fields).to_csv(file_name, index=False, header=False)

# Main program
def main():
    print("Mile Stone 3")
    care_areas = read_care_areas(r"C:\Users\skava\Downloads\Unhack-22pt16\MileStone3\Input and Output\CareAreas.csv")
    meta_data = read_meta_data(r"C:\Users\skava\Downloads\Unhack-22pt16\MileStone3\Input and Output\metadata.csv")

    main_fields = generate_main_fields(care_areas, meta_data)
    sub_fields = generate_sub_fields(main_fields, meta_data)

   # print_data(sub_fields)
    write_main_fields(r"C:\Users\skava\Downloads\Unhack-22pt16\MileStone3\Input and Output\mainfields.csv", main_fields)
    print("writing...")
    write_sub_fields(r"C:\Users\skava\Downloads\Unhack-22pt16\MileStone3\Input and Output\subfields.csv", sub_fields)

main()


