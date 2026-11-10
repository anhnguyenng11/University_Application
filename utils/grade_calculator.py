from utils import constants

def calculate_grade(mark: float) -> str:
    """
    Calculates the grade based on the mark.
    """
    if mark < constants.P_THRESHOLD:
        return "Z"
    elif mark < constants.C_THRESHOLD:
        return "P"
    elif mark < constants.D_THRESHOLD:
        return "C"
    elif mark < constants.HD_THRESHOLD:
        return "D"
    return "HD"
