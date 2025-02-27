"""
Configuration for PyRIT strategies based on attack budgets and other parameters.
This module defines mappings between attack budgets and appropriate PyRIT strategies.
"""

from typing import Dict, List, Any, Union, Optional, Type
from enum import Enum

# Import all potential PyRIT strategies and converters with their correct paths
from pyrit.orchestrator.single_turn.flip_attack_orchestrator import FlipAttackOrchestrator
from pyrit.orchestrator.multi_turn.crescendo_orchestrator import CrescendoOrchestrator
from pyrit.orchestrator.single_turn.prompt_sending_orchestrator import PromptSendingOrchestrator
from pyrit.orchestrator.multi_turn.red_teaming_orchestrator import RedTeamingOrchestrator

# Check if these classes are available in the installed version of PyRIT
# You may need to adjust these imports based on your PyRIT version
try:
    from pyrit.prompt_converter.base64_converter import Base64Converter
    from pyrit.prompt_converter.hex_converter import HexConverter
    from pyrit.prompt_converter.homoglyph_converter import HomoglyphConverter
    from pyrit.prompt_converter.leet_converter import LeetConverter
    from pyrit.prompt_converter.morse_converter import MorseConverter
    from pyrit.prompt_converter.reverse_converter import ReverseConverter
    from pyrit.prompt_converter.unicode_converter import UnicodeConverter
    from pyrit.prompt_converter.flip_converter import FlipConverter
except ImportError:
    # Fallback if the specific converters aren't available
    Base64Converter = None
    HexConverter = None
    HomoglyphConverter = None
    LeetConverter = None
    MorseConverter = None
    ReverseConverter = None
    UnicodeConverter = None
    FlipConverter = None

class StrategyType(Enum):
    """Types of PyRIT components that can be used in attacks."""
    ORCHESTRATOR = "orchestrator"
    CONVERTER = "converter"
    

class BudgetLevel(Enum):
    """Budget levels for attacks."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# Define mappings between budget levels and PyRIT strategies
BUDGET_TO_STRATEGIES = {
    BudgetLevel.LOW.value: [
        {"class": FlipAttackOrchestrator, "params": {}, "type": StrategyType.ORCHESTRATOR.value},
        {"class": LeetConverter, "params": {}, "type": StrategyType.CONVERTER.value},
    ],
    BudgetLevel.MEDIUM.value: [
        {"class": CrescendoOrchestrator, "params": {}, "type": StrategyType.ORCHESTRATOR.value},
        {"class": Base64Converter, "params": {}, "type": StrategyType.CONVERTER.value},
        {"class": HomoglyphConverter, "params": {}, "type": StrategyType.CONVERTER.value},
    ],
    BudgetLevel.HIGH.value: [
        {"class": RedTeamingOrchestrator, "params": {}, "type": StrategyType.ORCHESTRATOR.value},
        {"class": UnicodeConverter, "params": {}, "type": StrategyType.CONVERTER.value},
        {"class": MorseConverter, "params": {}, "type": StrategyType.CONVERTER.value},
    ]
}


def get_strategies_for_budget(budget_levels: List[str]) -> Dict[str, List[Any]]:
    """
    Get PyRIT strategies for the specified budget levels.
    
    Args:
        budget_levels: List of budget levels (e.g., ["low", "medium"])
        
    Returns:
        Dictionary with orchestrators and converters lists
    """
    orchestrators = []
    converters = []
    
    for level in budget_levels:
        if level not in [b.value for b in BudgetLevel]:
            continue
            
        strategies = BUDGET_TO_STRATEGIES.get(level, [])
        for strategy in strategies:
            # Skip if the class is None (not available in this PyRIT version)
            if strategy["class"] is None:
                continue
                
            if strategy["type"] == StrategyType.ORCHESTRATOR.value:
                orchestrators.append(strategy["class"](**strategy["params"]))
            elif strategy["type"] == StrategyType.CONVERTER.value:
                converters.append(strategy["class"](**strategy["params"]))
    
    return {
        "orchestrators": orchestrators,
        "converters": converters
    }


def create_orchestrator(
    orchestrators: Optional[List[Any]] = None, 
    converters: Optional[List[Any]] = None,
    target: Any = None
) -> PromptSendingOrchestrator:
    """
    Create a PyRIT orchestrator with the specified components.
    
    Args:
        orchestrators: List of PyRIT orchestrator strategies
        converters: List of PyRIT converters
        target: The target for the orchestrator
        
    Returns:
        Configured PyRIT orchestrator
    """
    orchestrator_kwargs = {}
    
    if target:
        orchestrator_kwargs["target"] = target
    
    if orchestrators:
        orchestrator_kwargs["strategies"] = orchestrators
    
    if converters:
        orchestrator_kwargs["converters"] = converters
    
    return PromptSendingOrchestrator(**orchestrator_kwargs)