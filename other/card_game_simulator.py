import random
from collections import defaultdict

def simulate_game():
    """Simulate one game where three cards are flipped randomly."""
    cards = [1, 1, 1]  # All cards start with the front side (1)
    rounds = 0
    while sum(cards) > 0:  # Continue until all cards are on the back side (0)
        rounds += 1
        card_to_flip = random.randint(0, 2)  # Randomly choose a card to flip
        cards[card_to_flip] = 1 - cards[card_to_flip]  # Flip the chosen card
    return rounds

def simulate_games(num_simulations):
    """Simulate multiple games and count occurrences of each round number."""
    round_counts = defaultdict(int)
    for _ in range(num_simulations):
        rounds = simulate_game()
        round_counts[rounds] += 1
    return round_counts

# Run 1,000,000 simulations
num_simulations = 1_000_000
round_counts = simulate_games(num_simulations)

# Sort and print the results
for round_num, count in sorted(round_counts.items()):
    print(f"Rounds: {round_num}, Count: {count}")
