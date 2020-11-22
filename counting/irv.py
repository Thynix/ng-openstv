from collections import defaultdict
from typing import List, Dict, Union
from format import blt


class TieError(Exception):
    pass


# TODO: What generic election results can be supported here?
#       Maybe wait until there's more than one format.
# TODO: Support more than one seat.
def get_irv_winner(ballots: List[blt.Ballot]) -> int:
    # TODO: remove votes for withdrawn candidates

    while True:
        votes_per_candidate = __sum_first_choices(ballots)
        winner = __get_winner(votes_per_candidate)
        if winner is not None:
            return winner

        if len(votes_per_candidate) == 2:
            number_one, vote_count = votes_per_candidate.popitem()
            number_two, check_vote_count = votes_per_candidate.popitem()
            assert vote_count == check_vote_count

            raise TieError(f"Candidates {number_one} and {number_two} are tied at {vote_count} votes.")

        ballots = __remove_loser_votes(ballots, votes_per_candidate)


def __sum_first_choices(ballots: List[blt.Ballot]) -> Dict[int, int]:
    votes_per_candidate = defaultdict(lambda: 0)
    for ballot in ballots:
        if len(ballot.candidates) == 0:
            continue

        votes_per_candidate[ballot.candidates[0]] += 1

    return votes_per_candidate


# TODO: How to detect ties? No winner with two candidates remaining?
def __get_winner(choices: Dict[int, int]) -> Union[int, None]:
    total_votes = sum(choices.values())
    for candidate_number, votes in choices.items():
        # TODO: Break out victory threshold?
        if votes > (total_votes / 2):
            return candidate_number

    return None


def __remove_loser_votes(ballots: List[blt.Ballot], votes: Dict[int, int]) -> List[blt.Ballot]:
    loser_candidate = min(votes.keys(), key=lambda c: votes[c])
    for ballot in ballots:
        if len(ballot.candidates) == 0:
            continue

        if ballot.candidates[0] == loser_candidate:
            ballot.candidates.pop(0)

    return ballots
