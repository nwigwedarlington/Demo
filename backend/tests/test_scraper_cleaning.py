from app.schemas.factcheck import NormalizedComment
from app.services.scraper import dedupe_and_clean_comments


def test_dedupe_and_spam_filter():
    comments = [
        NormalizedComment(author="A", comment=" Claim "),
        NormalizedComment(author="a", comment="claim"),
        NormalizedComment(author="B", comment="buy followers now"),
        NormalizedComment(author="C", comment=""),
    ]
    cleaned = dedupe_and_clean_comments(comments)
    assert len(cleaned) == 1
    assert cleaned[0].comment == "Claim"
