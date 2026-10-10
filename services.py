from config import EXCELLENT_SCORE, GOOD_SCORE, AVERAGE_SCORE, PASS_SCORE

def calculate_grade(score: int) -> str:
    """Balı hərf qiymətinə çevirir."""
    if score >= EXCELLENT_SCORE:
        return 'A'
    elif score >= GOOD_SCORE:
        return 'B'
    elif score >= AVERAGE_SCORE:
        return 'C'
    elif score >= PASS_SCORE:
        return 'D'
    else:
        return 'F'

def calculate_statistics(students: list) -> dict:
    """Tələbə nəticələrinə əsasən statistikaları hesablayır."""
    if not students:
        return {"total": 0, "average": 0, "highest": 0, "lowest": 0}

    scores = [student["Score"] for student in students]

    return {
        "total": len(scores),
        "average": round(sum(scores) / len(scores), 1),
        "highest": max(scores),
        "lowest": min(scores)
    }