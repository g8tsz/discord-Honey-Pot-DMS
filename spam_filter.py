"""Classify the text a user sent in a private message."""
import re
import unicodedata

TOPIC = re.compile(r"\b(?:casinos?|poker|blackjack|sportsbooks?|sports?\s*betting|betting|parlays?|rakeback|free spins|slots?|(?:whale|diamond|vip|premium|daily|free) (?:picks?|plays?))\b")
LINK = re.compile(r"(?:https?://|discord\.gg/|discord(?:app)?\.com/invite/|t\.me/)\S+")
PITCH = re.compile(r"\b(?:instant cashouts?|daily rakeback|deposit bonus(?:es)?|welcome bonus(?:es)?|free spins|guaranteed (?:wins?|profit)|risk free bets?|(?:free|premium|vip|super whale|diamond) (?:picks?|plays?)|we (?:got|have) you(?: covered)?)\b")
RECRUIT = re.compile(r"\b(?:join (?:our|my|the) (?:free |vip )?(?:discord|server|group|sportsbook|casino|telegram|channel)|(?:sign up|register) (?:now|today|with us)|use (?:my|our) (?:referral |promo )?code|(?:dm|message) me for (?:access|picks|plays|the link))\b")


def is_promotional_spam(content: str) -> bool:
    text = unicodedata.normalize("NFKC", content).casefold()
    text = re.sub(r"[*_\x60~\u200b-\u200d\ufeff]", "", text)
    text = " ".join(re.sub(r"[-‐‑–—]", " ", text).split())
    if not TOPIC.search(text):
        return False
    signals = (LINK.search(text), PITCH.search(text), RECRUIT.search(text))
    return sum(bool(signal) for signal in signals) >= 2
