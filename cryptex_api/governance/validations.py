
import re

TWITTER_RE = "^[a-zA-Z0-9_]{1,15}$"
DISCORD_RE = "^.{3,32}#[0-9]{4}$"

def is_empty(text):
    return text.strip() == ""

def max_len(text, l):
    return len(text) < l

def is_twitter_name(username):
    return not re.match(TWITTER_RE, username) is None

def is_discord_name(username):
    return not re.match(DISCORD_RE, username) is None