PLAY_SCORES = {
    'rock': 1,
    'paper': 2,
    'scissors': 3
}

GAME_SCORES = {
    'win': 6,
    'draw': 3,
    'loss': 0
}

GAME_RULES = {
    ('rock', 'paper'): 'win',
    ('rock', 'scissors'): 'loss',
    ('paper', 'rock'): 'loss',
    ('paper', 'scissors'): 'win',
    ('scissors', 'rock'): 'win',
    ('scissors', 'paper'): 'loss'
}

MAPPING = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors',
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors'
}


def parse_line(line: str) -> tuple[str, str]:
    them, me = line.strip().split()
    return (MAPPING[them], MAPPING[me])


def evaluate_game(game: tuple[str, str]) -> str:
    them, me = game
    if them == me:
        return 'draw'
    else:
        return GAME_RULES[game]


# Part 2 functions
RESPONSE_MAPPING = {
    'X': 'loss',
    'Y': 'draw',
    'Z': 'win'
}

BEATS = {
    'rock': 'scissors',
    'paper': 'rock',
    'scissors': 'paper'
}

LOSES = {v: k for k, v in BEATS.items()}


def lookup_response(outcome: str, them: str) -> str:
    if outcome == 'draw':
        return them
    elif outcome == 'win':
        return LOSES[them]
    elif outcome == 'loss':
        return BEATS[them]


def parse_line2(line: str) -> tuple[str, str]:
    them, me = line.strip().split()
    outcome = RESPONSE_MAPPING[me]
    them = MAPPING[them]
    me = lookup_response(outcome, them)
    return (them, me)


if __name__ == '__main__':
    # Part 1
    running_total = 0
    with open('input.txt') as f:
        for line in f:
            game = parse_line(line)
            outcome = evaluate_game(game)
            game_score = GAME_SCORES[outcome]
            play_score = PLAY_SCORES[game[1]]
            running_total += game_score + play_score

    print(running_total)

    # Part 2
    running_total = 0
    with open('input.txt') as f:
        for line in f:
            game = parse_line2(line)
            outcome = evaluate_game(game)
            game_score = GAME_SCORES[outcome]
            play_score = PLAY_SCORES[game[1]]
            running_total += game_score + play_score
    print(running_total)
