"""
Constants used in Red Team Agent.
"""

import os
from .._attack_strategy import AttackStrategy
from .._attack_objective_generator import RiskCategory

# File extensions
BASELINE_IDENTIFIER = "baseline"
DATA_EXT = ".jsonl"
RESULTS_EXT = ".json"

# Mapping of attack strategies to complexity levels

ATTACK_STRATEGY_COMPLEXITY_MAP = {
    str(AttackStrategy.Baseline.value): "baseline",
    str(AttackStrategy.AnsiAttack.value): "easy",
    str(AttackStrategy.AsciiArt.value): "easy",
    str(AttackStrategy.AsciiSmuggler.value): "easy",
    str(AttackStrategy.Atbash.value): "easy",
    str(AttackStrategy.Base64.value): "easy",
    str(AttackStrategy.Binary.value): "easy",
    str(AttackStrategy.Caesar.value): "easy",
    str(AttackStrategy.CharacterSpace.value): "easy",
    str(AttackStrategy.CharSwap.value): "easy",
    str(AttackStrategy.Diacritic.value): "easy",
    str(AttackStrategy.Flip.value): "easy",
    str(AttackStrategy.Leetspeak.value): "easy",
    str(AttackStrategy.Morse.value): "easy",
    str(AttackStrategy.ROT13.value): "easy",
    str(AttackStrategy.SuffixAppend.value): "easy",
    str(AttackStrategy.StringJoin.value): "easy",
    str(AttackStrategy.UnicodeConfusable.value): "easy",
    str(AttackStrategy.UnicodeSubstitution.value): "easy",
    str(AttackStrategy.Url.value): "easy",
    str(AttackStrategy.EASY.value): "easy",
    str(AttackStrategy.Tense.value): "moderate",
    str(AttackStrategy.MODERATE.value): "moderate",
    str(AttackStrategy.DIFFICULT.value): "difficult",
    str(AttackStrategy.Jailbreak.value): "easy",
    str(AttackStrategy.IndirectJailbreak.value): "easy",
    str(AttackStrategy.MultiTurn.value): "difficult",
    str(AttackStrategy.Crescendo.value): "difficult",
}

# Task timeouts and status codes
INTERNAL_TASK_TIMEOUT = 120

# Sampling constants
# Multiplier for the maximum number of sampling iterations when round-robin sampling from risk subtypes.
# This prevents infinite loops while allowing sufficient attempts to find unique objectives.
# With N subtypes, this allows up to N * MAX_SAMPLING_ITERATIONS_MULTIPLIER total iterations.
MAX_SAMPLING_ITERATIONS_MULTIPLIER = 100

# Task status definitions
TASK_STATUS = {
    "PENDING": "pending",
    "RUNNING": "running",
    "COMPLETED": "completed",
    "FAILED": "failed",
    "TIMEOUT": "timeout",
    "INCOMPLETE": "incomplete",
}
