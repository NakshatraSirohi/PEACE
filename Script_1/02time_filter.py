main_folder = input("Enter main folder: ")

input_file = f'{main_folder}\\{main_folder}_killtime.txt'
output_file = f'{main_folder}\\{main_folder}_grouping.txt'

with open(input_file, 'r') as file:
    # Read and convert all lines to integers
    numbers = [int(line.strip()) for line in file]

# Initialize variables
all_groups = []  # List to hold all groups of numbers
current_group = [numbers[0]]  # Start with the first number in the first group
a = numbers[0]  # Reference point for each group

# Iterate through the numbers, starting from the second element
for i in range(1, len(numbers)):
    # Check if the difference with the first element of the group (a) is <= 20
    if numbers[i] - a <= 20:
        # If the difference is 20 or less, add to the current group
        current_group.append(numbers[i])
    else:
        # If the difference is more than 20, start a new group
        all_groups.append(current_group)  # Add the current group to the list of groups
        current_group = [numbers[i]]  # Start a new group with the current number
        a = numbers[i]  # Update the reference point for the new group

# Add the last group if it hasn't been added yet
all_groups.append(current_group)

# Print the groups
with open(output_file, "a") as file:
    for index, group in enumerate(all_groups):
        print(f'Group-{index}: {group}')
        file.write(f'{group}\n')
