from enum import Enum

class Status(Enum):
    BACKLOG = "Backlog"
    IN_PROGRESS = "In Progress"
    REVIEW = "Review"
    DONE = "Done"

class Transition(Enum):
    BACKLOG_TO_IN_PROGRESS = "Backlog -> In Progress"
    IN_PROGRESS_TO_REVIEW = "In Progress -> Review"
    REVIEW_TO_DONE = "Review -> Done"

ALLOWED_TRANSITIONS = {
    Status.BACKLOG.value: [Transition.BACKLOG_TO_IN_PROGRESS.value],
    Status.IN_PROGRESS.value: [Transition.IN_PROGRESS_TO_REVIEW.value],
    Status.REVIEW.value: [Transition.REVIEW_TO_DONE.value],
}
