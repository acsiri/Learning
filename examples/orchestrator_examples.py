"""
LLM Orchestrator Examples
Demonstrates various use cases and routing decisions.
"""

from src.llm_orchestrator import (
    LLMOrchestrator,
    PromptType,
    ModelCapability,
    GoogleGeminiProvider,
    MockLLMProvider
)


def example_basic_routing():
    """Example 1: Basic routing of different prompt types."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Prompt Routing")
    print("="*60)
    
    orchestrator = LLMOrchestrator()
    
    # Test prompts of different types
    test_prompts = [
        "Write a Python function to sort an array using quicksort algorithm",
        "Tell me a creative story about a robot discovering emotions",
        "Analyze the impact of climate change on global economies",
        "Solve this equation: 2x^2 + 5x - 3 = 0",
        "What are the key principles of object-oriented programming?",
    ]
    
    for prompt in test_prompts:
        print(f"\nPrompt: {prompt[:60]}...")
        analysis = orchestrator.analyze_prompt(prompt)
        print(f"Type: {analysis.prompt_type.value}")
        print(f"Confidence: {analysis.confidence:.1%}")
        print(f"Complexity: {analysis.complexity_score:.1%}")
        print(f"Required capabilities: {[c.value for c in analysis.required_capabilities[:3]]}")


def example_routing_decisions():
    """Example 2: Examine routing decisions."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Routing Decisions & Reasoning")
    print("="*60)
    
    orchestrator = LLMOrchestrator()
    
    code_prompt = "Debug this Python code that's throwing a KeyError in the dictionary access"
    creative_prompt = "Write an inspiring poem about overcoming challenges"
    analytical_prompt = "Compare the strengths and weaknesses of microservices vs monolithic architecture"
    
    for prompt in [code_prompt, creative_prompt, analytical_prompt]:
        print(f"\nPrompt: {prompt}")
        decision = orchestrator.decide_routing(prompt)
        print(f"Selected Model: {decision.selected_model}")
        print(f"Reasoning: {decision.reasoning}")
        if decision.alternative_models:
            print(f"Alternatives: {decision.alternative_models}")


def example_routing_preferences():
    """Example 3: Routing with different preferences."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Routing with User Preferences")
    print("="*60)
    
    orchestrator = LLMOrchestrator()
    prompt = "Implement a machine learning model for image classification"
    
    # Route with quality preference
    print("\nWith QUALITY preference:")
    decision = orchestrator.decide_routing(prompt, prefer_quality=True)
    print(f"Selected: {decision.selected_model}")
    print(f"Reasoning: {decision.reasoning}")
    
    # Route with cost preference
    print("\nWith COST preference:")
    decision = orchestrator.decide_routing(prompt, prefer_cost=True)
    print(f"Selected: {decision.selected_model}")
    print(f"Reasoning: {decision.reasoning}")
    
    # Route with speed preference
    print("\nWith SPEED preference:")
    decision = orchestrator.decide_routing(prompt, prefer_speed=True)
    print(f"Selected: {decision.selected_model}")
    print(f"Reasoning: {decision.reasoning}")


def example_orchestration():
    """Example 4: Full orchestration with response generation."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Full Orchestration (with Response)")
    print("="*60)
    
    orchestrator = LLMOrchestrator()
    
    prompts = [
        "Write a simple 'Hello World' program in Python",
        "What are the benefits of using Docker containers?",
        "Explain quantum computing to a 10-year-old",
    ]
    
    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        response, decision = orchestrator.orchestrate(prompt)
        print(f"Routed to: {decision.selected_model}")
        print(f"Response: {response}")


def example_custom_providers():
    """Example 5: Register and use custom providers."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Provider Registration")
    print("="*60)
    
    orchestrator = LLMOrchestrator()
    
    # Register custom providers
    gpt_provider = MockLLMProvider("gpt-4")
    gpt_provider.capabilities = [
        ModelCapability.CODE_GENERATION,
        ModelCapability.LOGICAL_REASONING,
        ModelCapability.CREATIVE_WRITING,
    ]
    orchestrator.register_provider(
        "gpt-4",
        gpt_provider,
        {
            "name": "OpenAI GPT-4",
            "strengths": ["reasoning", "coding", "creativity"],
            "latency": "medium",
            "cost": "high",
            "max_tokens": 8192,
        }
    )
    
    # Register specialized model
    code_provider = MockLLMProvider("code-specialist")
    code_provider.capabilities = [
        ModelCapability.CODE_GENERATION,
        ModelCapability.CODE_ANALYSIS,
    ]
    orchestrator.register_provider(
        "code-specialist",
        code_provider,
        {
            "name": "Code Specialist Model",
            "strengths": ["code generation", "code analysis"],
            "latency": "fast",
            "cost": "medium",
            "max_tokens": 4096,
        }
    )
    
    # Test routing with new providers
    code_prompt = "Optimize this recursive function for better performance"
    creative_prompt = "Write a science fiction short story"
    
    print("\nCode Prompt Routing:")
    decision = orchestrator.decide_routing(code_prompt)
    print(f"Selected: {decision.selected_model}")
    
    print("\nCreative Prompt Routing:")
    decision = orchestrator.decide_routing(creative_prompt)
    print(f"Selected: {decision.selected_model}")


def example_routing_stats():
    """Example 6: Analyze routing statistics."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Routing Statistics & Analytics")
    print("="*60)
    
    orchestrator = LLMOrchestrator()
    
    # Simulate multiple routing decisions
    prompts = [
        "Write Python code for binary search",
        "Create a short poem about nature",
        "Analyze the stock market trends",
        "Solve: Find all prime numbers up to 100",
        "Explain machine learning to beginners",
        "Write a recursive function to calculate factorial",
    ]
    
    for prompt in prompts:
        orchestrator.decide_routing(prompt)
    
    # Get and display statistics
    stats = orchestrator.get_routing_stats()
    print("\nRouting Statistics:")
    print(f"Total Decisions: {stats['total_routes']}")
    print(f"Average Confidence: {stats['average_confidence']:.1%}")
    
    print("\nBreakdown by Prompt Type:")
    for ptype, count in stats['by_prompt_type'].items():
        print(f"  {ptype}: {count} ({count/stats['total_routes']:.1%})")
    
    # Generate full report
    print("\nDetailed Report:")
    print(orchestrator.generate_routing_report())


def example_domain_specific_routing():
    """Example 7: Domain-specific routing."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Domain-Specific Routing")
    print("="*60)
    
    orchestrator = LLMOrchestrator()
    
    domain_prompts = {
        "medical": "What are the symptoms and treatment options for Type 2 diabetes?",
        "legal": "Explain the difference between civil and criminal law",
        "financial": "How should I diversify my investment portfolio?",
        "technical": "Design a microservices architecture for an e-commerce platform",
        "academic": "What are the main theories in behavioral psychology?",
    }
    
    for domain, prompt in domain_prompts.items():
        print(f"\nDomain: {domain}")
        print(f"Prompt: {prompt}")
        analysis = orchestrator.analyze_prompt(prompt)
        print(f"Detected domains: {analysis.domain_tags}")
        decision = orchestrator.decide_routing(prompt)
        print(f"Routed to: {decision.selected_model}")


def example_complexity_analysis():
    """Example 8: Analyze prompt complexity."""
    print("\n" + "="*60)
    print("EXAMPLE 8: Complexity Analysis")
    print("="*60)
    
    orchestrator = LLMOrchestrator()
    
    simple_prompt = "What is 2+2?"
    moderate_prompt = "Explain how photosynthesis works in plants and how it relates to the carbon cycle"
    complex_prompt = """
    Design a distributed system for processing real-time financial data streams that:
    1) Ingests data from multiple exchanges in low-latency fashion
    2) Applies complex mathematical models for anomaly detection
    3) Provides decision support for algorithmic trading
    4) Maintains consistency across geographically distributed nodes
    5) Handles failure scenarios gracefully
    What architectural patterns would you recommend?
    """
    
    prompts = [
        ("Simple", simple_prompt),
        ("Moderate", moderate_prompt),
        ("Complex", complex_prompt),
    ]
    
    for level, prompt in prompts:
        analysis = orchestrator.analyze_prompt(prompt)
        print(f"\n{level} Prompt:")
        print(f"  Length: {len(prompt.split())} words")
        print(f"  Complexity Score: {analysis.complexity_score:.1%}")
        print(f"  Type: {analysis.prompt_type.value}")
        print(f"  Keywords: {', '.join(analysis.keywords[:5])}")


if __name__ == "__main__":
    # Run all examples
    example_basic_routing()
    example_routing_decisions()
    example_routing_preferences()
    example_orchestration()
    example_custom_providers()
    example_routing_stats()
    example_domain_specific_routing()
    example_complexity_analysis()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)
