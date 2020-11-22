from typing import List
from flask import Flask, render_template, url_for
from format.blt import load_blt, BLT, Ballot
import pickle
import fcntl

app = Flask(__name__)
app.config.from_object("config")


blt: BLT = None

# Lists of form element IDs, in candidate order, ordered from first to last
# preference.
candidate_options: List[List[str]] = list()


@app.before_first_request
def initialize():
    # Load BLT
    global blt
    with open(app.config["BLT_PATH"], "r") as blt_file:
        blt = load_blt(blt_file)

    # TODO: omit withdrawn candidates
    # Compute form options
    global candidate_options
    for choice_index in range(len(blt.candidate_names)):
        choice_level = list()
        candidate_options.append(choice_level)
        for candidate_number in range(1, len(blt.candidate_names) + 1):
            choice_level.append(f"choice_index:candidate_number")

    # Write the BLT pickle if it does not already exist
    try:
        with open(app.config["PICKLE_PATH"], "xb") as pickle_file:
            pickle.dump(blt, pickle_file, pickle.HIGHEST_PROTOCOL)
    except FileExistsError:
        pass


@app.route("/")
def vote_form():
    return render_template(
        "vote_form.html",
        form_target=url_for("submit_vote"),
        candidate_options=candidate_options,
        blt=blt,
    )


@app.route("/vote", methods=["POST"])
def submit_vote():
    # TODO: parse ballot out of radio buttons
    ballot = Ballot()
    with open(app.config["PICKLE_PATH"], "+b") as pickle_file:
        fcntl.flock(pickle_file, fcntl.F_EXLCK)
        running_results: BLT = pickle.load(pickle_file)
        running_results.add_ballot(ballot)
        return ""


