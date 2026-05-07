# Test Coverage Analysis for azure-ai-evaluation

**Analysis Date:** December 29, 2025  
**Package Version:** 1.14.0  
**Analysis Type:** Unit Tests Coverage

## Executive Summary

This document provides a comprehensive analysis of test coverage for the `azure-ai-evaluation` package based on unit tests execution.

### Overall Statistics

- **Total Python Files Analyzed:** 278
- **Overall Coverage:** 29% (based on unit tests only)
- **Files with 100% Coverage:** 83 files (30%)
- **Files with 0% Coverage:** 81 files (29%)
- **Total Test Files:** 75 test files
  - Unit Tests: 35 files
  - E2E Tests: ~40 files

## Coverage by Module

### 1. Evaluators Module (`_evaluators/`)
- **Total Files:** 71
- **Average Coverage:** 87.1%
- **Status:** ✅ **Well-tested**

**Best Covered Files:**
- Most `__init__.py` files: 100%
- Core evaluator implementations: High coverage

**Files Needing Attention:**
- `_tool_call_success.py`: 14.8%
- `_task_adherence.py`: 23.1%
- `_base_rai_svc_eval.py`: 32.9%
- `_tool_output_utilization.py`: 35.4%
- `_rouge.py`: 43.8%

**Analysis:** The evaluators module is the most mature and well-tested component of the package. Most evaluator implementations have excellent coverage, though some specialized evaluators need additional test coverage.

### 2. Evaluate Module (`_evaluate/`)
- **Total Files:** 13
- **Average Coverage:** 77.2%
- **Status:** ✅ **Good coverage**

**Best Covered Files:**
- `eval_run_context.py`: 97.3%
- `_eval_run.py`: 89.3%
- `target_run_context.py`: 89.2%

**Files Needing Attention:**
- `_evaluate_aoai.py`: 65.4%
- `_evaluate.py`: 65.9%
- `code_client.py`: 70.5%

**Analysis:** The core evaluation execution logic is well-tested. The main evaluation orchestration has good coverage, though some edge cases in AOAI integration could benefit from more tests.

### 3. Other Core Files
- **Total Files:** 66
- **Average Coverage:** 69.2%
- **Status:** ✅ **Moderate to good coverage**

**Best Covered Files:**
- Graders: 100% coverage across multiple grader implementations
- Core utilities: Generally high coverage

**Files Needing Attention:**
- `_ai_services.py`: 0%
- `_sk_services.py`: 1.9%
- `rouge_scorer.py`: 9.1%

### 4. Simulator Module (`simulator/`)
- **Total Files:** 23
- **Average Coverage:** 62.4%
- **Status:** ⚠️ **Moderate coverage - needs improvement**

**Best Covered Files:**
- Configuration and constants: 100%
- Data structures: 84%

**Files Needing Attention:**
- `_generated_rai_client.py`: 0%
- `_conversation.py`: 13.6%
- `_proxy_completion_model.py`: 19.5%
- `_adversarial_simulator.py`: 22.3%
- `_indirect_attack_simulator.py`: 24.2%

**Analysis:** The simulator module has significant gaps in test coverage, particularly for generated client code and advanced simulation features. Core simulation logic needs more comprehensive testing.

### 5. Red Team Module (`red_team/`)
- **Total Files:** 30
- **Average Coverage:** 3.3%
- **Status:** ❌ **Critically low coverage**

**Coverage Status:**
- Most files: 0% coverage
- Only one `__init__.py` has any coverage

**Files with No Coverage (Sample):**
- `_agent_functions.py`: 0%
- `_agent_tools.py`: 0%
- `_red_team.py`: 0%
- `_orchestrator_manager.py`: 0%
- `_result_processor.py`: 0%

**Analysis:** The red team module is essentially untested at the unit test level. This represents a significant quality and maintenance risk. The module likely has E2E tests but lacks comprehensive unit test coverage.

### 6. Common Module (`_common/`)
- **Total Files:** 75
- **Average Coverage:** 25.8%
- **Status:** ⚠️ **Low coverage**

**Coverage Breakdown:**
- Generated code: Mostly 0% coverage (expected)
- Utility functions: Variable coverage (33-66%)
- RAI service client: 46% coverage

**Files Needing Attention:**
- Generated model and serialization code: 0%
- OneDp service patterns: 0%
- RAI client implementations: 0%

**Analysis:** The common module contains a mix of generated code (which typically has lower coverage expectations) and utility functions. Hand-written utilities have reasonable coverage, but generated code and some critical infrastructure components lack tests.

## Critical Findings

### Strengths
1. **Evaluators:** The core evaluator functionality is well-tested with 87% average coverage
2. **Evaluation Engine:** The main evaluation execution logic has strong coverage at 77%
3. **Graders:** All grader implementations have 100% coverage
4. **Test Infrastructure:** Good test fixture and helper coverage

### Weaknesses
1. **Red Team Module:** Critically undertested (3.3% coverage) - highest priority for improvement
2. **Simulator Module:** Needs significant improvement (62.4% coverage)
3. **Generated Code:** Much generated client code has 0% coverage
4. **AI Services Integration:** Service converters and integrations are poorly tested

## Recommendations

### Immediate Priority (High Impact)
1. **Add Red Team Unit Tests**
   - Focus on core orchestration logic
   - Test agent functions and tools
   - Test result processing
   - Target: Achieve at least 60% coverage

2. **Improve Simulator Coverage**
   - Add tests for adversarial simulator
   - Test conversation handling
   - Test proxy completion models
   - Target: Achieve 75% coverage

### Medium Priority
3. **Test Service Converters**
   - Add tests for `_ai_services.py`
   - Add tests for `_sk_services.py`
   - Focus on conversion logic

4. **Complete Evaluator Coverage**
   - Add tests for low-coverage evaluators (tool call success, task adherence)
   - Ensure all evaluators have comprehensive test suites

### Lower Priority
5. **Consider Testing Generated Code**
   - Evaluate if generated code should be tested
   - May not be necessary if generated from well-tested schemas
   - Focus on integration tests instead

6. **Documentation**
   - Document testing strategy for each module
   - Create testing guidelines for contributors

## How to Run Coverage Analysis

### Run Unit Tests with Coverage
```bash
cd /path/to/azure-ai-evaluation
pytest tests/unittests --cov=azure.ai.evaluation --cov-report=html --cov-report=term --cov-branch
```

### Run All Tests with Coverage (Including E2E)
```bash
cd /path/to/azure-ai-evaluation
tox run -c ../../../eng/tox/tox.ini --root .
```

### View HTML Coverage Report
After running tests, open:
```bash
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
start htmlcov/index.html  # On Windows
```

## Coverage Data Files

The following coverage artifacts are generated:
- `.coverage` - Coverage data file
- `coverage.json` - JSON format coverage data
- `htmlcov/` - HTML coverage report with line-by-line details
- `test-junit-whl.xml` - JUnit test results

## Test Organization

```
tests/
├── unittests/           # Unit tests (35 files)
│   ├── test_aoai_*.py
│   ├── test_content_safety_*.py
│   ├── test_tool_*.py
│   └── ...
├── e2etests/            # End-to-end tests (~40 files)
│   ├── test_evaluate.py
│   ├── test_builtin_evaluators.py
│   ├── test_red_team.py
│   └── ...
├── converters/          # Converter tests
│   └── ai_agent_converter/
└── test_configs/        # Test configuration files
```

## Next Steps

1. Review this analysis with the team
2. Prioritize testing gaps based on business criticality
3. Create tasks/issues for improving coverage in critical areas
4. Set coverage targets for new code (recommend 80%+ for new features)
5. Consider setting up coverage gates in CI/CD pipeline
6. Run comprehensive E2E test coverage to supplement unit test coverage

## Notes

- This analysis is based on **unit tests only**. E2E tests likely provide additional coverage not reflected in these numbers.
- Generated code (e.g., from autorest) is expected to have lower coverage as it's tested through integration rather than unit tests.
- The overall 29% coverage figure is only for unit tests; actual coverage including E2E tests is likely higher.
- Coverage for red team features may be primarily in E2E tests rather than unit tests.

---

**Report Generated By:** GitHub Copilot Coding Agent  
**For Questions:** Refer to the Azure SDK for Python testing documentation
