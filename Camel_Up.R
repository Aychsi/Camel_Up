# Number of camels
num_camels <- 5

# Initialize camel positions at the start of the track
camel_positions <- rep(1, num_camels)

# Initialize stacks with each camel in its own stack
camel_stacks <- lapply(1:num_camels, function(x) x)

# Roll dice for one camel
roll_dice <- function() {
  sample(1:3, 1)  # Assuming dice have values 1-3 for simplicity
}

# Move camels
move_camel <- function(camel, dice_roll) {
  # Find the current position and stack of the camel
  current_position <- camel_positions[camel]
  stack_index <- which(sapply(camel_stacks, function(stack) camel %in% stack))
  
  # Move the camel and all camels on top of it
  move_stack <- camel_stacks[[stack_index]]
  camel_positions[move_stack] <- camel_positions[move_stack] + dice_roll
  
  # Check if moving to a stack with other camels
  if (any(camel_positions == current_position + dice_roll)) {
    target_stack_index <- which(sapply(camel_stacks, function(stack) any(camel_positions[stack] == current_position + dice_roll)))
    camel_stacks[[target_stack_index]] <- c(camel_stacks[[target_stack_index]], move_stack)
    camel_stacks[[stack_index]] <- NULL  # Remove the old stack
  } else {
    camel_stacks[[stack_index]] <- move_stack
  }
  
  # Remove any NULL entries in camel_stacks
  camel_stacks <- camel_stacks[sapply(camel_stacks, function(x) !is.null(x))]
}

# Check for winners
check_winner <- function() {
  if (any(camel_positions >= 16)) {  # Assuming the track is 16 spaces long
    return(TRUE)
  }
  return(FALSE)
}

# Print camel positions and stacks
print_camel_info <- function() {
  cat("Camel positions:\n")
  for (camel in 1:num_camels) {
    cat(sprintf("Camel %d is at position %d\n", camel, camel_positions[camel]))
  }
  cat("\nCamel stacks:\n")
  for (i in seq_along(camel_stacks)) {
    cat(sprintf("Stack %d contains camels: %s\n", i, paste(camel_stacks[[i]], collapse = ", ")))
  }
}

# Main game loop
winner <- FALSE
turn_count <- 0
remaining_camels <- 1:num_camels  # All camels start as 'not moved yet'

repeat {
  turn_count <- turn_count + 1
  cat("\nTurn:", turn_count, "\n")
  
  # Reset remaining camels for the next turn
  remaining_camels <- 1:num_camels
  
  while (length(remaining_camels) > 0) {
    # Select a random camel from those that haven't moved yet
    camel <- sample(remaining_camels, 1)
    
    # Roll the dice for the selected camel
    dice_roll <- roll_dice()
    
    # Move the selected camel
    move_camel(camel, dice_roll)
    
    # Remove the moved camel from the list of remaining camels
    remaining_camels <- remaining_camels[!remaining_camels %in% camel]
    
    # Print out current positions and stacks
    print_camel_info()
    
    # Check for a winner
    winner <- check_winner()
    
    if (winner) {
      cat("Game Over! We have a winner!\n")
      break
    }
  }
  
  if (winner) {
    break
  }
  
  # Wait for user input to proceed to the next turn
  readline(prompt = "Press [enter] to continue to the next turn...")
}
