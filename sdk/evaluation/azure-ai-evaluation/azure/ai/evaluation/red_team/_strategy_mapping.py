# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilities for mapping AttackStrategy to PyRIT FoundryStrategy."""

from typing import List, Optional

from ._attack_strategy import AttackStrategy

# Lazy import to avoid circular dependencies
_FoundryStrategy = None


def _get_foundry_strategy():
    """Lazy import of FoundryStrategy to avoid early PyRIT dependency."""
    global _FoundryStrategy
    if _FoundryStrategy is None:
        from pyrit.scenario.scenarios.foundry_scenario import FoundryStrategy
        _FoundryStrategy = FoundryStrategy
    return _FoundryStrategy


def map_to_foundry_strategy(strategy: AttackStrategy) -> Optional[object]:
    """
    Map an AttackStrategy enum value to its FoundryStrategy equivalent.
    
    :param strategy: The AttackStrategy to map
    :type strategy: AttackStrategy
    :return: The corresponding FoundryStrategy member, or None if no mapping exists
    :rtype: Optional[FoundryStrategy]
    """
    FoundryStrategy = _get_foundry_strategy()
    
    # Direct mappings for converter strategies
    mapping = {
        AttackStrategy.EASY: FoundryStrategy.EASY,
        AttackStrategy.MODERATE: FoundryStrategy.MODERATE,
        AttackStrategy.DIFFICULT: FoundryStrategy.DIFFICULT,
        AttackStrategy.AnsiAttack: FoundryStrategy.AnsiAttack,
        AttackStrategy.AsciiArt: FoundryStrategy.AsciiArt,
        AttackStrategy.AsciiSmuggler: FoundryStrategy.AsciiSmuggler,
        AttackStrategy.Atbash: FoundryStrategy.Atbash,
        AttackStrategy.Base64: FoundryStrategy.Base64,
        AttackStrategy.Binary: FoundryStrategy.Binary,
        AttackStrategy.Caesar: FoundryStrategy.Caesar,
        AttackStrategy.CharacterSpace: FoundryStrategy.CharacterSpace,
        AttackStrategy.CharSwap: FoundryStrategy.CharSwap,
        AttackStrategy.Diacritic: FoundryStrategy.Diacritic,
        AttackStrategy.Flip: FoundryStrategy.Flip,
        AttackStrategy.Leetspeak: FoundryStrategy.Leetspeak,
        AttackStrategy.Morse: FoundryStrategy.Morse,
        AttackStrategy.ROT13: FoundryStrategy.ROT13,
        AttackStrategy.SuffixAppend: FoundryStrategy.SuffixAppend,
        AttackStrategy.StringJoin: FoundryStrategy.StringJoin,
        AttackStrategy.Tense: FoundryStrategy.Tense,
        AttackStrategy.UnicodeConfusable: FoundryStrategy.UnicodeConfusable,
        AttackStrategy.UnicodeSubstitution: FoundryStrategy.UnicodeSubstitution,
        AttackStrategy.Url: FoundryStrategy.Url,
        AttackStrategy.Jailbreak: FoundryStrategy.Jailbreak,
        AttackStrategy.MultiTurn: FoundryStrategy.MultiTurn,
        AttackStrategy.Crescendo: FoundryStrategy.Crescendo,
    }
    
    return mapping.get(strategy)


def requires_custom_handling(strategy: AttackStrategy) -> bool:
    """
    Check if a strategy requires custom handling outside FoundryScenario.
    
    :param strategy: The AttackStrategy to check
    :type strategy: AttackStrategy
    :return: True if the strategy needs custom handling
    :rtype: bool
    """
    # IndirectJailbreak and Baseline require special handling
    return strategy in (AttackStrategy.IndirectJailbreak, AttackStrategy.Baseline)


def map_strategy_list(strategies: List[AttackStrategy]) -> tuple[List[object], List[AttackStrategy]]:
    """
    Map a list of AttackStrategy values to FoundryStrategy equivalents.
    
    :param strategies: List of AttackStrategy values to map
    :type strategies: List[AttackStrategy]
    :return: Tuple of (mapped_foundry_strategies, unmapped_strategies)
    :rtype: tuple[List[FoundryStrategy], List[AttackStrategy]]
    """
    mapped = []
    unmapped = []
    
    for strategy in strategies:
        foundry_strategy = map_to_foundry_strategy(strategy)
        if foundry_strategy is not None:
            mapped.append(foundry_strategy)
        else:
            unmapped.append(strategy)
    
    return mapped, unmapped
