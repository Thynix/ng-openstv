from collections import defaultdict, OrderedDict
from typing import Dict
from typing import OrderedDict as OrderedDictType
from format import blt


class TieError(Exception):
    pass


# TODO: What generic election results can be supported here?
#       Maybe wait until there's more than one format.
# TODO: Support more than one seat.
def get_irv_winner(ballots: Dict[blt.Ballot, int]) -> OrderedDictType[int, int]:
    # TODO: remove votes for withdrawn candidates

    while True:
        votes_per_candidate = __sum_first_choices(ballots)
        if __has_winner(votes_per_candidate):
            return votes_per_candidate

        if len(votes_per_candidate) == 2:
            number_one, vote_count = votes_per_candidate.popitem()
            number_two, check_vote_count = votes_per_candidate.popitem()
            assert vote_count == check_vote_count

            raise TieError(f"Candidates {number_one} and {number_two} are tied at {vote_count} votes.")

        ballots = __remove_loser_votes(ballots, votes_per_candidate)


def __sum_first_choices(ballots: Dict[blt.Ballot, int]) -> OrderedDictType[int, int]:
    votes_per_candidate = defaultdict(lambda: 0)
    for ballot, weight in ballots.items():
        if len(ballot.candidates) == 0:
            continue

        votes_per_candidate[ballot.candidates[0]] += weight

    sorted_votes = OrderedDict()
    for candidate_number in sorted(
            votes_per_candidate.keys(),
            key=lambda k: votes_per_candidate[k],
            reverse=True,
    ):
        sorted_votes[candidate_number] = votes_per_candidate[candidate_number]

    return sorted_votes


# TODO: How to detect ties? No winner with two candidates remaining?
def __has_winner(choices: Dict[int, int]) -> bool:
    total_votes = sum(choices.values())
    for candidate_number, votes in choices.items():
        # TODO: Break out victory threshold?
        if votes > (total_votes / 2):
            return True

    return False


def __remove_loser_votes(ballots: Dict[blt.Ballot, int], votes: Dict[int, int]) -> Dict[blt.Ballot, int]:
    loser_candidate = min(votes.keys(), key=lambda c: votes[c])
    for ballot in ballots.keys():
        if len(ballot.candidates) == 0:
            continue

        if ballot.candidates[0] == loser_candidate:
            ballot.candidates.pop(0)

    return ballots
