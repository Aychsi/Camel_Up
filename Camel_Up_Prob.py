import random
from collections import Counter
import copy

# Camel directions
camel_directions = {
    'red': 1,
    'blue': 1,
    'green': 1,
    'purple': 1,
    'yellow': 1,
    'white': -1,
    'black': -1
}

regular_camels = {'red', 'blue', 'green', 'purple', 'yellow'}

# 🧱 Display the board as text with emoji
def display_board(board):
    emoji_map = {
        "red": "🔴", "blue": "🔵", "green": "🟢",
        "yellow": "💛", "purple": "🟣",
        "white": "⚪", "black": "⚫"
    }
    print("\n📦 Board State:\n")
    for pos in sorted(board.keys(), reverse=True):
        stack = board[pos]
        camel_strs = [f"{emoji_map.get(c, '')} {c}" for c in stack]
        print(f"[{pos:>3}] " + " ".join(camel_strs))

def get_user_board_state():
    print("🎲 Enter the board state:")
    print("Each line = one space on the track.")
    print("Format: <position> <camel1> <camel2> ... (from bottom to top)")
    print("Type 'done' when finished.")
    board_state = {}
    while True:
        line = input("> ").strip()
        if line.lower() == "done":
            break
        parts = line.split()
        pos = int(parts[0])
        camels = parts[1:]
        board_state[pos] = camels
    return board_state

def get_rolled_dice():
    print("\n🎲 Enter rolled camel dice (space-separated):")
    return input("> ").strip().split()

def get_desert_tiles():
    print("\n🏜️ Enter desert tiles:")
    print("Each line = one tile. Format: <position> <effect> (must be +1 or -1)")
    print("Type 'done' when finished.")
    desert_tiles = {}
    while True:
        line = input("> ").strip()
        if line.lower() == "done":
            break
        pos, effect = line.split()
        desert_tiles[int(pos)] = int(effect)
    return desert_tiles

def find_camel(board, camel):
    for pos, stack in board.items():
        if camel in stack:
            return pos, stack.index(camel)
    return None, None

def move_camel(board, camel, roll, desert_tiles):
    pos, height = find_camel(board, camel)
    stack_to_move = board[pos][height:].copy()
    board[pos] = board[pos][:height]
    if not board[pos]:
        del board[pos]

    direction = camel_directions[camel]
    new_pos = pos + direction * roll

    tile_effect = desert_tiles.get(new_pos, 0)
    final_pos = new_pos + tile_effect

    if final_pos in board:
        if tile_effect == -1:
            board[final_pos] = stack_to_move + board[final_pos]  # camel goes under
        else:
            board[final_pos] += stack_to_move  # camel goes on top
    else:
        board[final_pos] = stack_to_move

def simulate_leg(board_state, rolled_dice, desert_tiles, n_simulations=10000):
    all_camels = list(camel_directions.keys())
    unrolled = [camel for camel in all_camels if camel not in rolled_dice]
    win_counter = Counter()

    for _ in range(n_simulations):
        board = copy.deepcopy(board_state)
        remaining_dice = unrolled.copy()
        random.shuffle(remaining_dice)

        for camel in remaining_dice:
            roll = random.randint(1, 3)
            move_camel(board, camel, roll, desert_tiles)

        positions = sorted(board.keys(), reverse=True)
        for pos in positions:
            top_stack = board[pos]
            for candidate in reversed(top_stack):
                if candidate in regular_camels:
                    win_counter[candidate] += 1
                    break
            else:
                continue
            break

    results = {
        camel: (win_counter[camel] / n_simulations) * 100
        for camel in sorted(regular_camels)
    }
    return results

# Run program
print("🐪 Camel Up: Leg Win Probability Simulator 🐪\n")
board_state = get_user_board_state()
rolled_dice = get_rolled_dice()
desert_tiles = get_desert_tiles()

print("\n🧱 Initial Board State:")
display_board(board_state)

print("\n🎲 Rolled Dice:")
print(", ".join(rolled_dice) if rolled_dice else "None")

results = simulate_leg(board_state, rolled_dice, desert_tiles)

print("\n📊 Leg Win Probabilities:")
for camel, pct in results.items():
    print(f"{camel.capitalize():<7}: {pct:.2f}%")
