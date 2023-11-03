import random

# Number of camels and initial positions
num_camels = 5
camel_positions = [0] * num_camels  # All camels start at position 0

# Track the order of camels in the race; the first camel in the list is the bottom one in the stack
camel_order = list(range(num_camels))

# Function to roll the die for a camel
def roll_dice():
    return random.choice([1, 2, 3])  # Assuming dice have values 1-3 for simplicity

# Function to move camels based on dice roll
def move_camel(camel_index):
    roll = roll_dice()
    camel = camel_order[camel_index]
    current_position = camel_positions[camel]

    # Find all camels on top of the current camel and move them together
    stack_index = camel_index
    while stack_index < len(camel_order) and camel_positions[camel_order[stack_index]] == current_position:
        camel_positions[camel_order[stack_index]] += roll
        stack_index += 1

    # If camels reach a position with other camels, stack them together
    new_position = camel_positions[camel]
    if new_position in camel_positions[:camel_index]:
        # Find the bottom camel of the new stack and insert the moving camels above it
        bottom_camel_index = camel_positions.index(new_position)
        camel_order[bottom_camel_index+1:bottom_camel_index+1] = camel_order[camel_index:stack_index]

        # Remove the original positions of the moving camels
        del camel_order[camel_index:stack_index]

# Function to check for a winner
def check_winner():
    return any(position >= 16 for position in camel_positions)  # Assuming the track is 16 spaces long

# Function to print camel positions and stacks
def print_camel_info():
    print("Camel positions and order (bottom to top of stack):")
    for position in sorted(set(camel_positions)):
        stack = [camel for camel, pos in enumerate(camel_positions) if pos == position]
        print(f"Position {position}: {stack}")

# Main game loop
winner = False
turn_count = 0

while not winner:
    turn_count += 1
    print(f"\nTurn: {turn_count}")

    # Determine the move order based on the bottom-most camel in each stack
    move_order = sorted(range(num_camels), key=lambda x: (camel_positions[x], -x), reverse=True)

    for camel_index in move_order:
        move_camel(camel_index)
        print_camel_info()

        if check_winner():
            winner = True
            winning_camel = max(range(num_camels), key=lambda x: camel_positions[x])
            print(f"Game Over! Camel {winning_camel} wins!")
            break

    if not winner:
        input("Press Enter to continue to the next turn...")
