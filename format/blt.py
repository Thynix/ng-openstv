from typing import List, Dict, TextIO


class Ballot:
    def __init__(self, candidates: List[int]):
        """
        :param candidates: Candidate numbers from first to last rank.
        """
        self.candidates = candidates

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, WeightedBallot):
            return NotImplemented

        return o.ballot == self.candidates

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return str({
            "ballot": ",".join(map(str, self.candidates)),
        })


class WeightedBallot:
    def __init__(self, candidates: List[int], weight: int = 1):
        """
        :param candidates: Candidate numbers from first to last rank.
        :param weight: Number of times to apply the ballot. Can be used for storing only unique ballots.
        """
        self.ballot = Ballot(candidates)

        if weight < 1:
            raise BLTError(f"Ballot weight must be at least 1; got {weight}")

        self.weight = weight

    def __str__(self) -> str:
        return str({
            "ballot": self.ballot,
            "weight": self.weight,
        })


def __load_ballot(line: str) -> WeightedBallot:
    try:
        values = list(map(int, line.split()))
    except ValueError as e:
        raise BLTError("Failed to parse integer on ballot line", e)

    if len(values) < 2:
        raise BLTError(f"Ballot line must have at least 2 numbers; got \"{line}\"")

    weight = values.pop(0)
    end_marker = values.pop(-1)
    if end_marker != 0:
        raise BLTError(f"Ballot end marker must be 0; got {end_marker}")

    return WeightedBallot(
        candidates=values,
        weight=weight,
    )


# Implements https://www.opavote.com/help/overview#blt-file-format
class BLT:
    ballots: Dict[Ballot, int]
    """Ballot weight keyed by ballot"""
    withdrawn_numbers: List[int]

    def __init__(self, title: str, candidate_names: List[str],
                 withdrawn_numbers: List[int], seat_count: int):
        """
        :param withdrawn_numbers: Candidate numbers that withdrew from the race.
        """
        if seat_count < 1:
            raise BLTError(f"Must be at least one seat; got {seat_count}")
        self.seat_count = seat_count

        for candidate_number in withdrawn_numbers:
            if candidate_number < 1:
                raise BLTError(f"Candidate numbers start at 1; got {candidate_number}")
            if candidate_number > len(candidate_names):
                raise BLTError(f"{candidate_number} exceeds count of candidates ({len(candidate_names)})")
        self.withdrawn_numbers = withdrawn_numbers

        if len(candidate_names) < 1:
            raise BLTError(f"Must be at least one candidate; got {len(candidate_names)}")

        for index, candidate_name in enumerate(candidate_names):
            if len(candidate_name.strip()) == 0:
                raise BLTError(f"Candidate #{index + 1} has an empty name")
        self.candidate_names = candidate_names

        if len(title.strip()) == 0:
            raise BLTError("Title is empty")
        self.title = title

        self.ballots = dict()

    def add_weighted_ballot(self, ballot: WeightedBallot):
        if ballot not in self.ballots:
            self.ballots[ballot.ballot] = ballot.weight
        else:
            self.ballots[ballot.ballot] += ballot.weight

    def add_ballot(self, ballot: Ballot):
        if ballot not in self.ballots:
            self.ballots[ballot] = 1
        else:
            self.ballots[ballot] += 1


def load_blt(stream: TextIO) -> BLT:
    # The first line has two numbers indicating the number of candidates and
    # the number of seats.
    line_values = __read_next_line(stream).split()
    if len(line_values) != 2:
        raise BLTError(f"Expecting candidate count and seat count on first "
                       f"line; found {len(line_values)} values")

    try:
        candidate_count = int(line_values[0])
        # As it's passed into BLT through list length, negative values won't
        # be represented, which would make the error misleading.
        if candidate_count < 1:
            raise BLTError(f"Must be at least one candidate; got {candidate_count}")
    except ValueError as e:
        raise BLTError("Failed to parse candidate count", e)

    try:
        seat_count = int(line_values[1])
    except ValueError as e:
        raise BLTError("Failed to parse seat count", e)

    # The next line could be withdrawn candidates, or the first ballot.
    line = __read_next_line(stream)
    try:
        # If it's withdrawn candidate numbers, it'll be negative.
        if int(line.split()[0]) < 0:
            withdrawn_numbers = list(map(lambda s: -int(s), line.split()))
            line = __read_next_line(stream)
        else:
            withdrawn_numbers = list()
    except ValueError as e:
        raise BLTError("Failed to parse second line of content", e)

    # Parse ballots until the end ballots marker.
    ballots = list()
    while not __is_end_ballots_marker(line):
        ballots.append(__load_ballot(line))
        line = __read_next_line(stream)

    # Read candidate names.
    candidate_names = list()
    for _ in range(candidate_count):
        candidate_names.append(__read_next_line(stream).strip("\""))

    title = __read_next_line(stream).strip("\"")

    try:
        line = __read_next_line(stream)
        raise BLTError(f"Found unexpected content after title line: \"{line}\"")
    except EOFError:
        pass

    blt = BLT(
        candidate_names=candidate_names,
        title=title,
        withdrawn_numbers=withdrawn_numbers,
        seat_count=seat_count,
    )

    for ballot in ballots:
        blt.add_weighted_ballot(ballot)

    return blt


def __is_end_ballots_marker(line):
    values = line.split()
    return len(values) == 1 and int(values[0]) == 0


# Blank lines, extra white space, and any comments (text after a #) are
# ignored.
def __read_next_line(stream: TextIO) -> str:
    """
    :return: A non-empty line with comments ignored.
    :raise EOFError:  Trying to read a line when no more are available.
    """
    for line in stream:
        # Strip any comments
        comment_index = line.find("#")
        if comment_index != -1:
            line = line[:comment_index]

        # Remove whitespace
        line = line.strip()

        # If the line is now empty, read another
        if len(line) == 0:
            continue

        return line

    raise EOFError


class BLTError(Exception):
    pass
