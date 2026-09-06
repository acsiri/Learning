# LLM Orchestrator - Dynamic LLM Selection Engine

An intelligent system that analyzes incoming prompts and routes them to the most suitable Large Language Model (LLM) based on prompt characteristics, complexity, and domain.

## Overview

The LLM Orchestrator acts as a smart router for LLM requests. Instead of always using the same model, it:

1. **Analyzes** incoming prompts for type, complexity, and domain
2. **Classifies** them into categories (code, creative, analytical, etc.)
3. **Scores** available LLM providers based on their capabilities
4. **Routes** the prompt to the best-matching model
5. **Tracks** routing decisions and statistics

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                   LLM Orchestrator                          │
│  (Main orchestration engine and decision maker)             │
└──────────────┬──────────────────────────────────────────────┘
               │
       ┌───────┴────────┬──────────────┬────────────────┐
       │                │              │                │
       ▼                ▼              ▼                ▼
   Analyzer        Providers       Router          Tracker
   (Classify)      (LLMs)         (Score)         (Stats)
   
   ├─ Type         ├─ Gemini      ├─ Match        ├─ History
   ├─ Complexity   ├─ GPT-4       │  Capabilities ├─ Type Dist
   ├─ Keywords     ├─ Custom      │  Cost/Speed   └─ Model Dist
   └─ Domain       └─ Mock        └─ Preferences
```

### Prompt Types

The system classifies prompts into the following types:

- **CODE**: Programming tasks (writing, debugging, optimization)
- **CREATIVE**: Artistic and imaginative content (stories, poems)
- **ANALYTICAL**: Data analysis and interpretation
- **CONVERSATIONAL**: General dialogue and Q&A
- **TECHNICAL**: Complex technical explanations
- **DOMAIN_SPECIFIC**: Medical, legal, financial expertise
- **MATH**: Mathematical problem solving
- **REASONING**: Logical deduction and proof

### Model Capabilities

Models are scored on their ability to handle:

- `CODE_GENERATION`: Writing code
- `CODE_ANALYSIS`: Analyzing and debugging code
- `CREATIVE_WRITING`: Generating creative content
- `LOGICAL_REASONING`: Complex reasoning tasks
- `MATH_SOLVING`: Mathematical problems
- `CONVERSATIONAL`: General conversation
- `DOMAIN_KNOWLEDGE`: Specialized domain knowledge
- `VISION`: Image/vision understanding
- `LONG_CONTEXT`: Handling large documents

## Quick Start

### Basic Usage

```python
from src.llm_orchestrator import LLMOrchestrator

# Initialize orchestrator
orchestrator = LLMOrchestrator()

# Route and get response
prompt = "Write a Python function to reverse a string"
response, decision = orchestrator.orchestrate(prompt)

print(f"Model used: {decision.selected_model}")
print(f"Reasoning: {decision.reasoning}")
print(f"Response: {response}")
```

### Analyze Without Routing

```python
# Just analyze the prompt
analysis = orchestrator.analyze_prompt(prompt)

print(f"Type: {analysis.prompt_type}")
print(f"Complexity: {analysis.complexity_score}")
print(f"Keywords: {analysis.keywords}")
print(f"Required capabilities: {analysis.required_capabilities}")
```

### View Routing Decision

```python
# See which model will be used without executing
decision = orchestrator.decide_routing(prompt)

print(f"Selected: {decision.selected_model}")
print(f"Reasoning: {decision.reasoning}")
print(f"Alternatives: {decision.alternative_models}")
```

## Advanced Usage

### With Preferences

```python
# Route with specific preferences
response, decision = orchestrator.orchestrate(
    prompt,
    prefer_speed=True      # Optimize for fast response
)

response, decision = orchestrator.orchestrate(
    prompt,
    prefer_cost=True       # Optimize for cost efficiency
)

response, decision = orchestrator.orchestrate(
    prompt,
    prefer_quality=True    # Optimize for response quality
)
```

### Register Custom Providers

```python
from src.llm_orchestrator import BaseLLMProvider, ModelCapability

class CustomProvider(BaseLLMProvider):
    def generate(self, prompt: str, **kwargs) -> str:
        # Your implementation
        return "Response from custom provider"

# Register with orchestrator
provider = CustomProvider("my-model", api_key="xxx")
orchestrator.register_provider(
    "my-model",
    provider,
    {
        "name": "My Custom Model",
        "strengths": ["code", "reasoning"],
        "latency": "fast",
        "cost": "low",
        "max_tokens": 4096
    }
)
```

### Track Statistics

```python
# Get routing statistics
stats = orchestrator.get_routing_stats()

print(f"Total routes: {stats['total_routes']}")
print(f"Average confidence: {stats['average_confidence']:.1%}")
print(f"By type: {stats['by_prompt_type']}")
print(f"By model: {stats['by_model']}")

# Generate report
report = orchestrator.generate_routing_report()
print(report)
```

## Prompt Analysis in Detail

### Type Detection

The analyzer uses keyword matching and pattern recognition:

```python
analysis = orchestrator.analyze_prompt("Write a Python function")

# Analysis results:
# - prompt_type: PromptType.CODE
# - confidence: 0.85 (85% confident)
# - keywords: ['python', 'function', 'write']
# - complexity_score: 0.3 (relatively simple)
# - required_capabilities: [CODE_GENERATION, LOGICAL_REASONING]
# - domain_tags: []
```

### Complexity Calculation

Complexity is determined by:

1. **Length**: More words = higher complexity
2. **Question Count**: Multiple questions = higher complexity
3. **Technical Vocabulary**: Longer words = potentially more complex
4. **Structure**: Nested parentheses/brackets = more complex

Score range: 0.0 (very simple) to 1.0 (extremely complex)

### Domain Detection

The system identifies specialized domains:

- **Medical**: doctor, patient, treatment, medication
- **Legal**: law, court, contract, attorney
- **Financial**: money, investment, stock, budget
- **Technical**: API, database, server, protocol
- **Academic**: research, thesis, study, hypothesis

## Routing Scoring

The orchestrator scores each provider using:

```
Total Score = 
    (Capability Match * 0.5) +
    (Classification Confidence * 0.2) +
    (Cost Factor * 0.15) +
    (Speed Factor * 0.15) +
    (Default Bonus * 0.1)
```

Where:
- **Capability Match**: How many required capabilities does provider have?
- **Confidence**: How certain is the classification?
- **Cost Factor**: Price per 1K tokens (if prefer_cost enabled)
- **Speed Factor**: Latency in ms (if prefer_speed enabled)

## Built-in Providers

### Google Gemini

- **Model**: gemini-pro
- **Capabilities**: Code, Analysis, Reasoning, Creative
- **Max Tokens**: 32,000
- **Latency**: Medium (~800ms)
- **Cost**: Low ($0.00075/1K tokens)

### Test/Mock Provider

- **Model**: test-model
- **Capabilities**: All (for testing)
- **Max Tokens**: 2,048
- **Latency**: Fast
- **Cost**: Free

## Examples

### Example 1: Code Routing

```python
code_prompt = "Debug this Python code that's throwing a KeyError"
decision = orchestrator.decide_routing(code_prompt)

# Output:
# Selected: 'gemini-pro' (or specialized code model if available)
# Reasoning: Selected 'gemini-pro' for code prompt (confidence: 90%). 
#            Required capabilities: code_generation, code_analysis, 
#            logical_reasoning.
```

### Example 2: Creative Routing

```python
creative_prompt = "Write an inspiring poem about overcoming challenges"
decision = orchestrator.decide_routing(creative_prompt)

# Output:
# Selected: 'gemini-pro' (or creative-specialized model if available)
# Reasoning: Selected for creative prompt (confidence: 85%).
#            Required capabilities: creative_writing
```

### Example 3: Domain-Specific

```python
legal_prompt = "Explain the difference between civil and criminal law"
analysis = orchestrator.analyze_prompt(legal_prompt)

print(f"Domain tags: {analysis.domain_tags}")  # ['legal']
# A legal-specialized model would score higher here
```

## Running Tests

```bash
# Run all orchestrator tests
python -m unittest tests.test_orchestrator -v

# Run specific test class
python -m unittest tests.test_orchestrator.TestPromptAnalyzer -v

# Run specific test
python -m unittest tests.test_orchestrator.TestPromptAnalyzer.test_code_prompt_detection
```

## Running Examples

```bash
# Run orchestrator examples
python examples/orchestrator_examples.py
```

The examples include:
1. Basic prompt routing across types
2. Examining routing decisions
3. Routing with different preferences
4. Full orchestration flow
5. Custom provider registration
6. Routing statistics
7. Domain-specific routing
8. Complexity analysis

## Configuration

### Environment Variables

```bash
# Set API keys for providers
export GEMINI_API_KEY="your-api-key"
export GPT_API_KEY="your-api-key"
export CLAUDE_API_KEY="your-api-key"
```

### Preferences

When calling `orchestrate()` or `decide_routing()`:

```python
# Cost optimization
orchestrator.orchestrate(prompt, prefer_cost=True)

# Speed optimization  
orchestrator.orchestrate(prompt, prefer_speed=True)

# Quality optimization
orchestrator.orchestrate(prompt, prefer_quality=True)
```

## Performance Considerations

### Analysis Speed
- Prompt analysis: ~1-5ms
- Provider matching: ~2-10ms
- Total routing decision: ~5-20ms

### Caching Strategies
- Consider caching analyses for similar prompts
- Cache provider profiles to avoid recalculation

### Scalability
- Horizontally scalable with multiple orchestrator instances
- Provider pooling recommended for high throughput
- Consider async routing for non-blocking calls

## Extending the System

### Add New Provider

```python
class MyLLMProvider(BaseLLMProvider):
    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name, api_key)
        self.capabilities = [
            ModelCapability.CODE_GENERATION,
            ModelCapability.LOGICAL_REASONING,
        ]
        self.cost_per_1k_tokens = 0.002
        self.latency_ms = 500
    
    def generate(self, prompt: str, **kwargs) -> str:
        # Implement your LLM call
        pass

# Register
provider = MyLLMProvider("my-llm", api_key="xxx")
orchestrator.register_provider(
    "my-llm",
    provider,
    {"name": "My LLM", "strengths": ["code", "reasoning"]}
)
```

### Customize Analysis

```python
class CustomAnalyzer(PromptAnalyzer):
    def analyze(self, prompt: str) -> PromptAnalysis:
        # Add custom analysis logic
        analysis = super().analyze(prompt)
        # Modify analysis as needed
        return analysis

orchestrator.analyzer = CustomAnalyzer()
```

## API Reference

### LLMOrchestrator

#### Methods

- `analyze_prompt(prompt: str) -> PromptAnalysis`
  - Analyze prompt without routing
  
- `decide_routing(prompt: str, **kwargs) -> RoutingDecision`
  - Make routing decision without generating response
  
- `orchestrate(prompt: str, **kwargs) -> Tuple[str, RoutingDecision]`
  - Full flow: analyze, route, and generate response
  
- `register_provider(name: str, provider: BaseLLMProvider, profile: Dict) -> None`
  - Register new LLM provider
  
- `get_routing_stats() -> Dict[str, Any]`
  - Get routing statistics
  
- `generate_routing_report() -> str`
  - Generate formatted routing report

### PromptAnalysis

Data class containing analysis results:
- `prompt_type: PromptType`
- `confidence: float` (0.0-1.0)
- `keywords: List[str]`
- `complexity_score: float` (0.0-1.0)
- `required_capabilities: List[ModelCapability]`
- `domain_tags: List[str]`

### RoutingDecision

Data class containing routing results:
- `selected_model: str`
- `reasoning: str`
- `alternative_models: List[Tuple[str, float]]`
- `analysis: PromptAnalysis`

## Troubleshooting

### No Providers Available
- Ensure at least one provider is registered
- Check API keys are set in environment
- Verify provider initialization succeeded

### Unexpected Routing Decisions
- Review the analysis: `decision.analysis`
- Check provider capabilities against requirements
- Examine the reasoning: `decision.reasoning`

### Low Classification Confidence
- Prompt may be ambiguous or mix multiple types
- Consider providing more specific prompts
- Check routing statistics for patterns

## Future Enhancements

Planned improvements:
- [ ] Async/parallel routing
- [ ] Machine learning-based routing optimization
- [ ] Cost tracking and budget management
- [ ] Prompt caching and result memoization
- [ ] Multi-modal (text + image) support
- [ ] Fallback strategies for failed providers
- [ ] A/B testing framework for models
- [ ] Detailed latency and cost analytics

## License

Part of the Card Camera Capture Project.

## Support

For issues or questions, refer to the main project documentation or create an issue in the repository.
