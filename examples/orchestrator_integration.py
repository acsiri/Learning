"""
LLM Orchestrator Integration Examples
Demonstrates how to integrate the orchestrator with existing systems.
"""

from src.llm_orchestrator import (
    LLMOrchestrator,
    BaseLLMProvider,
    ModelCapability,
)


class OrchestratedChatbot:
    """
    Enhanced chatbot that uses the LLM orchestrator for intelligent routing.
    Example integration with existing chatbot system.
    """
    
    def __init__(self):
        self.orchestrator = LLMOrchestrator()
        self.conversation_history = []
        self.routing_stats = {}
    
    def process_user_input(self, user_input: str, show_debug: bool = False) -> str:
        """
        Process user input using orchestrated routing.
        
        Args:
            user_input: User's message
            show_debug: Whether to show routing information
            
        Returns:
            Response from appropriate LLM
        """
        # Add to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Get analysis
        analysis = self.orchestrator.analyze_prompt(user_input)
        
        # Route to appropriate model
        response, decision = self.orchestrator.orchestrate(user_input)
        
        # Store in history
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "metadata": {
                "model": decision.selected_model,
                "prompt_type": analysis.prompt_type.value,
                "confidence": analysis.confidence,
            }
        })
        
        # Update stats
        self._update_stats(analysis, decision)
        
        if show_debug:
            print(f"\n[DEBUG] Routing Information:")
            print(f"  Model: {decision.selected_model}")
            print(f"  Type: {analysis.prompt_type.value}")
            print(f"  Confidence: {analysis.confidence:.1%}")
            print(f"  Reasoning: {decision.reasoning}")
        
        return response
    
    def _update_stats(self, analysis, decision):
        """Update routing statistics."""
        ptype = analysis.prompt_type.value
        model = decision.selected_model
        
        if ptype not in self.routing_stats:
            self.routing_stats[ptype] = {}
        
        if model not in self.routing_stats[ptype]:
            self.routing_stats[ptype][model] = 0
        
        self.routing_stats[ptype][model] += 1
    
    def get_conversation_summary(self) -> dict:
        """Get summary of conversation."""
        return {
            "total_messages": len(self.conversation_history),
            "routing_stats": self.routing_stats,
            "conversation": self.conversation_history
        }


class MultiModalOrchestratedSystem:
    """
    Advanced system that routes based on multiple signals.
    Can consider: prompt type, user history, resource constraints, etc.
    """
    
    def __init__(self):
        self.orchestrator = LLMOrchestrator()
        self.user_profiles = {}
        self.system_resources = {
            "budget_usd": 10.0,
            "speed_priority": False,
            "quality_priority": True,
        }
    
    def process_request(self, user_id: str, prompt: str, context: dict = None) -> dict:
        """
        Process request with multi-signal routing.
        
        Args:
            user_id: User identifier
            prompt: User's prompt
            context: Additional context (history, preferences, etc.)
            
        Returns:
            Response with metadata
        """
        context = context or {}
        
        # Get user profile
        user_profile = self.user_profiles.get(user_id, {})
        
        # Determine routing preferences based on multiple factors
        routing_prefs = {}
        
        # Check system resource constraints
        if self.system_resources["speed_priority"]:
            routing_prefs["prefer_speed"] = True
        
        if self.system_resources["quality_priority"]:
            routing_prefs["prefer_quality"] = True
        
        # Check user history for preferences
        if user_profile.get("prefers_cost_efficient"):
            routing_prefs["prefer_cost"] = True
        
        # Analyze prompt
        analysis = self.orchestrator.analyze_prompt(prompt)
        
        # Route with preferences
        response, decision = self.orchestrator.orchestrate(prompt, **routing_prefs)
        
        # Estimate cost
        estimated_tokens = len(response.split()) * 1.3  # Rough estimate
        provider = self.orchestrator.providers[decision.selected_model]
        estimated_cost = provider.get_cost_estimate(int(estimated_tokens))
        
        # Update budget
        self.system_resources["budget_usd"] -= estimated_cost
        
        return {
            "response": response,
            "model": decision.selected_model,
            "prompt_type": analysis.prompt_type.value,
            "confidence": analysis.confidence,
            "estimated_cost": estimated_cost,
            "remaining_budget": self.system_resources["budget_usd"],
            "reasoning": decision.reasoning,
        }
    
    def set_user_preference(self, user_id: str, preference: str, value: bool):
        """Set user routing preference."""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        self.user_profiles[user_id][preference] = value
    
    def set_system_constraint(self, constraint: str, value):
        """Set system-wide constraint."""
        self.system_resources[constraint] = value


class FallbackOrchestratedSystem:
    """
    Orchestrator with fallback strategies when primary routing fails.
    """
    
    def __init__(self):
        self.orchestrator = LLMOrchestrator()
        self.fallback_chain = []
    
    def process_with_fallback(self, prompt: str, max_attempts: int = 3) -> dict:
        """
        Process request with fallback chain.
        
        Args:
            prompt: Input prompt
            max_attempts: Maximum fallback attempts
            
        Returns:
            Response with fallback information
        """
        attempts = []
        
        for attempt in range(max_attempts):
            try:
                # Make routing decision
                decision = self.orchestrator.decide_routing(prompt)
                
                # Try to generate response
                provider = self.orchestrator.providers[decision.selected_model]
                response = provider.generate(prompt)
                
                attempts.append({
                    "attempt": attempt + 1,
                    "model": decision.selected_model,
                    "status": "success",
                    "response": response,
                })
                
                return {
                    "response": response,
                    "model_used": decision.selected_model,
                    "attempts": attempts,
                    "success": True,
                }
            
            except Exception as e:
                attempts.append({
                    "attempt": attempt + 1,
                    "model": decision.selected_model if 'decision' in locals() else "unknown",
                    "status": "failed",
                    "error": str(e),
                })
                
                if attempt < max_attempts - 1:
                    continue  # Try next fallback
                else:
                    # All attempts failed
                    return {
                        "response": None,
                        "model_used": None,
                        "attempts": attempts,
                        "success": False,
                        "error": "All fallback attempts exhausted",
                    }


# Integration Example: Using with existing Chatbot
def example_chatbot_integration():
    """Example: Integrate orchestrator with existing chatbot."""
    print("\n" + "="*60)
    print("EXAMPLE: Chatbot Integration")
    print("="*60)
    
    chatbot = OrchestratedChatbot()
    
    # Simulate conversation
    prompts = [
        "What is Python?",
        "Write a function to calculate fibonacci numbers",
        "Tell me a funny story",
        "Explain machine learning",
        "Debug this code: for i in range(10): print(i",
    ]
    
    for prompt in prompts:
        print(f"\nUser: {prompt}")
        response = chatbot.process_user_input(prompt, show_debug=True)
        print(f"Bot: {response}")
    
    # Print summary
    summary = chatbot.get_conversation_summary()
    print("\n" + "="*60)
    print("Conversation Summary:")
    print(f"Total Messages: {summary['total_messages']}")
    print("Routing Statistics:")
    for ptype, models in summary['routing_stats'].items():
        print(f"  {ptype}:")
        for model, count in models.items():
            print(f"    {model}: {count}")


# Integration Example: Multi-signal routing
def example_multimodal_integration():
    """Example: Multi-signal routing with constraints."""
    print("\n" + "="*60)
    print("EXAMPLE: Multi-Signal Routing")
    print("="*60)
    
    system = MultiModalOrchestratedSystem()
    
    # Set user preferences
    system.set_user_preference("user_123", "prefers_cost_efficient", True)
    
    # Process requests
    requests = [
        ("user_123", "Write optimized Python code"),
        ("user_456", "Help me understand quantum physics"),
    ]
    
    for user_id, prompt in requests:
        print(f"\nUser: {user_id}, Prompt: {prompt}")
        result = system.process_request(user_id, prompt)
        print(f"Model: {result['model']}")
        print(f"Response: {result['response']}")
        print(f"Cost: ${result['estimated_cost']:.4f}")
        print(f"Remaining Budget: ${result['remaining_budget']:.2f}")


# Integration Example: Fallback strategies
def example_fallback_integration():
    """Example: Fallback routing strategies."""
    print("\n" + "="*60)
    print("EXAMPLE: Fallback Orchestration")
    print("="*60)
    
    system = FallbackOrchestratedSystem()
    
    prompt = "Convert this image to text"
    print(f"\nPrompt: {prompt}")
    
    result = system.process_with_fallback(prompt)
    
    print(f"Success: {result['success']}")
    print(f"Model Used: {result['model_used']}")
    print("Attempts:")
    for attempt in result['attempts']:
        print(f"  Attempt {attempt['attempt']}: {attempt['status']} ({attempt.get('model', 'N/A')})")
    
    if result['response']:
        print(f"Response: {result['response']}")


# Integration Example: Request batching
def example_batch_processing():
    """Example: Batch processing with orchestrator."""
    print("\n" + "="*60)
    print("EXAMPLE: Batch Processing")
    print("="*60)
    
    orchestrator = LLMOrchestrator()
    
    # Batch of requests
    batch = [
        "Write Python code for web scraping",
        "Compose a haiku about autumn",
        "Explain the concept of entropy",
        "Design a REST API for a bookstore",
    ]
    
    total_cost = 0
    results = []
    
    for prompt in batch:
        response, decision = orchestrator.orchestrate(prompt)
        provider = orchestrator.providers[decision.selected_model]
        
        estimated_tokens = len(prompt.split()) + len(response.split())
        cost = provider.get_cost_estimate(estimated_tokens)
        total_cost += cost
        
        results.append({
            "prompt": prompt[:40] + "...",
            "model": decision.selected_model,
            "type": decision.analysis.prompt_type.value,
            "cost": cost,
        })
    
    print("\nBatch Processing Results:")
    print(f"{'Prompt':<40} {'Model':<15} {'Type':<15} {'Cost':<8}")
    print("-" * 80)
    
    for result in results:
        print(f"{result['prompt']:<40} {result['model']:<15} {result['type']:<15} ${result['cost']:.4f}")
    
    print("-" * 80)
    print(f"{'Total Cost:':<70} ${total_cost:.4f}")


if __name__ == "__main__":
    # Run all integration examples
    example_chatbot_integration()
    example_multimodal_integration()
    example_fallback_integration()
    example_batch_processing()
    
    print("\n" + "="*60)
    print("Integration examples completed!")
    print("="*60)
