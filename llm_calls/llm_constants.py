CARD_MODEL = "claude-opus-5-5"

# Opus 5.5 always thinks; effort is the only control, and its default is medium. Set here rather
# than left to the default so a change of model cannot change it silently.
CARD_EFFORT = "medium"

EMBEDDING_MODEL = None

# Thinking is billed as output and counts against this, so it has to leave room for both.
MAX_TOKENS = 16000
