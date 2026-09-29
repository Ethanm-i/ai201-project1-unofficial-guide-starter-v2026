def judge(question, expects, answer, results) -> bool:
    return expects.lower().strip() in answer.lower()

"""
LLM ad judge
repidfuzz ( thi works well in small chucks doesent do embeddings) 0 librarys to no libraries 
this is what repidfuzz can help do
"""

def retrueval_hits (expcted, results ) -> bool:
    """
    any part of my expect in the results
    """
    return any(expects.strip().lower() for chunk in results)