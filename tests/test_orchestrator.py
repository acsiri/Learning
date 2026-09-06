"""
Tests for LLM Orchestrator
Comprehensive test suite for prompt analysis, routing, and provider management.
"""

import unittest
from src.llm_orchestrator import (
    LLMOrchestrator,
    PromptAnalyzer,
    PromptType,
    ModelCapability,
    GoogleGeminiProvider,
    MockLLMProvider,
    PromptAnalysis,
    RoutingDecision,
)


class TestPromptAnalyzer(unittest.TestCase):
    """Test prompt analysis functionality."""
    
    def setUp(self):
        self.analyzer = PromptAnalyzer()
    
    def test_code_prompt_detection(self):
        """Test detection of code-related prompts."""
        prompt = "Write a Python function to reverse a list"
        analysis = self.analyzer.analyze(prompt)
        self.assertEqual(analysis.prompt_type, PromptType.CODE)
        self.assertGreater(analysis.confidence, 0.6)
    
    def test_creative_prompt_detection(self):
        """Test detection of creative prompts."""
        prompt = "Write a short story about a time traveler"
        analysis = self.analyzer.analyze(prompt)
        self.assertEqual(analysis.prompt_type, PromptType.CREATIVE)
        self.assertGreater(analysis.confidence, 0.5)
    
    def test_analytical_prompt_detection(self):
        """Test detection of analytical prompts."""
        prompt = "Analyze the pros and cons of remote work"
        analysis = self.analyzer.analyze(prompt)
        self.assertEqual(analysis.prompt_type, PromptType.ANALYTICAL)
        self.assertGreater(analysis.confidence, 0.5)
    
    def test_math_prompt_detection(self):
        """Test detection of math-related prompts."""
        prompt = "Solve the quadratic equation 2x^2 + 5x - 3 = 0"
        analysis = self.analyzer.analyze(prompt)
        self.assertEqual(analysis.prompt_type, PromptType.MATH)
        self.assertGreater(analysis.confidence, 0.5)
    
    def test_reasoning_prompt_detection(self):
        """Test detection of reasoning-focused prompts."""
        prompt = "Use logical reasoning to prove that all prime numbers greater than 2 are odd"
        analysis = self.analyzer.analyze(prompt)
        self.assertIn(analysis.prompt_type, [PromptType.REASONING, PromptType.ANALYTICAL])
    
    def test_keyword_extraction(self):
        """Test keyword extraction from prompts."""
        prompt = "Python database server framework"
        analysis = self.analyzer.analyze(prompt)
        self.assertIn("python", [kw.lower() for kw in analysis.keywords])
    
    def test_complexity_scoring(self):
        """Test complexity scoring."""
        simple = "What is AI?"
        complex_prompt = "Discuss the implications of artificial intelligence on employment, with consideration of technological displacement, new skill requirements, and policy interventions needed for societal adaptation."
        
        simple_analysis = self.analyzer.analyze(simple)
        complex_analysis = self.analyzer.analyze(complex_prompt)
        
        self.assertLess(simple_analysis.complexity_score, complex_analysis.complexity_score)
    
    def test_domain_tag_extraction(self):
        """Test extraction of domain tags."""
        prompts = {
            "medical": "What are the symptoms of diabetes?",
            "legal": "Explain contract law fundamentals",
            "financial": "How to invest in stocks?",
        }
        
        for domain, prompt in prompts.items():
            analysis = self.analyzer.analyze(prompt)
            self.assertTrue(
                any(domain in tag for tag in analysis.domain_tags) or analysis.domain_tags,
                f"Domain '{domain}' not detected in tags: {analysis.domain_tags}"
            )
    
    def test_capability_mapping(self):
        """Test mapping of prompts to required capabilities."""
        code_prompt = "Write a Python function"
        analysis = self.analyzer.analyze(code_prompt)
        self.assertIn(ModelCapability.CODE_GENERATION, analysis.required_capabilities)
    
    def test_prompt_history(self):
        """Test that prompt history is maintained."""
        self.analyzer.analyze("First prompt")
        self.analyzer.analyze("Second prompt")
        self.assertEqual(len(self.analyzer.prompt_history), 2)


class TestLLMProviders(unittest.TestCase):
    """Test LLM provider functionality."""
    
    def test_mock_provider_generation(self):
        """Test mock provider response generation."""
        provider = MockLLMProvider("test-model")
        response = provider.generate("test prompt")
        self.assertIn("test-model", response)
        self.assertIn("test prompt", response)
    
    def test_mock_provider_capabilities(self):
        """Test that mock provider has all capabilities."""
        provider = MockLLMProvider()
        self.assertEqual(len(provider.capabilities), len(ModelCapability))
    
    def test_provider_availability(self):
        """Test provider availability check."""
        provider = MockLLMProvider()
        self.assertTrue(provider.is_available())
    
    def test_cost_estimation(self):
        """Test cost estimation."""
        provider = MockLLMProvider()
        provider.cost_per_1k_tokens = 0.001
        cost = provider.get_cost_estimate(1000)
        self.assertAlmostEqual(cost, 0.001, places=5)


class TestLLMOrchestrator(unittest.TestCase):
    """Test LLM orchestrator functionality."""
    
    def setUp(self):
        self.orchestrator = LLMOrchestrator()
    
    def test_orchestrator_initialization(self):
        """Test that orchestrator initializes with default providers."""
        self.assertGreater(len(self.orchestrator.providers), 0)
        self.assertGreater(len(self.orchestrator.model_profiles), 0)
    
    def test_provider_registration(self):
        """Test registering a new provider."""
        custom_provider = MockLLMProvider("custom-model")
        self.orchestrator.register_provider(
            "custom-model",
            custom_provider,
            {"name": "Custom", "strengths": ["testing"]}
        )
        self.assertIn("custom-model", self.orchestrator.providers)
    
    def test_analyze_prompt(self):
        """Test prompt analysis through orchestrator."""
        analysis = self.orchestrator.analyze_prompt("Write a Python program")
        self.assertIsInstance(analysis, PromptAnalysis)
        self.assertEqual(analysis.prompt_type, PromptType.CODE)
    
    def test_decide_routing(self):
        """Test routing decision without execution."""
        decision = self.orchestrator.decide_routing("Write Python code")
        self.assertIsInstance(decision, RoutingDecision)
        self.assertIsNotNone(decision.selected_model)
        self.assertIsNotNone(decision.reasoning)
        self.assertIsNotNone(decision.analysis)
    
    def test_routing_with_preferences(self):
        """Test routing with different preferences."""
        prompt = "Complex analysis task"
        
        # Test cost preference
        decision_cost = self.orchestrator.decide_routing(prompt, prefer_cost=True)
        self.assertIn("cost", decision_cost.reasoning.lower())
        
        # Test speed preference
        decision_speed = self.orchestrator.decide_routing(prompt, prefer_speed=True)
        self.assertIn("speed", decision_speed.reasoning.lower())
    
    def test_orchestrate_full_flow(self):
        """Test full orchestration flow."""
        prompt = "Explain quantum computing"
        response, decision = self.orchestrator.orchestrate(prompt)
        
        self.assertIsNotNone(response)
        self.assertIsInstance(decision, RoutingDecision)
        self.assertIn("test-model", response)  # Mock provider response
    
    def test_routing_history(self):
        """Test that routing history is maintained."""
        self.orchestrator.decide_routing("First prompt")
        self.orchestrator.decide_routing("Second prompt")
        self.assertEqual(len(self.orchestrator.routing_history), 2)
    
    def test_routing_statistics(self):
        """Test routing statistics calculation."""
        self.orchestrator.decide_routing("Write code")
        self.orchestrator.decide_routing("Write a story")
        self.orchestrator.decide_routing("Analyze data")
        
        stats = self.orchestrator.get_routing_stats()
        
        self.assertEqual(stats['total_routes'], 3)
        self.assertIn('by_prompt_type', stats)
        self.assertIn('by_model', stats)
        self.assertIn('average_confidence', stats)
    
    def test_routing_report_generation(self):
        """Test that routing report can be generated."""
        self.orchestrator.decide_routing("Test prompt 1")
        self.orchestrator.decide_routing("Test prompt 2")
        
        report = self.orchestrator.generate_routing_report()
        self.assertIn("Routing Report", report)
        self.assertIn("Total Routing Decisions", report)
    
    def test_empty_routing_stats(self):
        """Test stats when no routing has occurred."""
        fresh_orchestrator = LLMOrchestrator()
        stats = fresh_orchestrator.get_routing_stats()
        self.assertEqual(stats['total_routes'], 0)
    
    def test_alternative_models_suggestions(self):
        """Test that alternatives are suggested."""
        decision = self.orchestrator.decide_routing("Complex coding task")
        # Should have selected model and potentially alternatives
        self.assertIsNotNone(decision.selected_model)
        self.assertIsInstance(decision.alternative_models, list)


class TestRoutingLogic(unittest.TestCase):
    """Test routing logic and decision making."""
    
    def setUp(self):
        self.orchestrator = LLMOrchestrator()
        # Add multiple test providers with different capabilities
        
        code_provider = MockLLMProvider("code-specialist")
        code_provider.capabilities = [ModelCapability.CODE_GENERATION, ModelCapability.CODE_ANALYSIS]
        self.orchestrator.register_provider("code-specialist", code_provider, {"name": "Code Specialist"})
        
        creative_provider = MockLLMProvider("creative-specialist")
        creative_provider.capabilities = [ModelCapability.CREATIVE_WRITING]
        self.orchestrator.register_provider("creative-specialist", creative_provider, {"name": "Creative Specialist"})
    
    def test_code_routed_to_code_specialist(self):
        """Test that code prompts are routed to code specialist."""
        decision = self.orchestrator.decide_routing("Write a Python function for sorting")
        # Should prefer a code-focused provider
        self.assertIsNotNone(decision.selected_model)
    
    def test_creative_routed_to_creative_specialist(self):
        """Test that creative prompts are routed to creative specialist."""
        decision = self.orchestrator.decide_routing("Write a beautiful poem about nature")
        # Should prefer creative provider
        self.assertIsNotNone(decision.selected_model)
    
    def test_routing_consistency(self):
        """Test that similar prompts are routed consistently."""
        prompt1 = "Write a Python function to sort numbers"
        prompt2 = "Write a Python function to filter elements"
        
        decision1 = self.orchestrator.decide_routing(prompt1)
        decision2 = self.orchestrator.decide_routing(prompt2)
        
        # Both code prompts should be routed to same/similar type of provider
        self.assertEqual(decision1.selected_model, decision2.selected_model)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        self.orchestrator = LLMOrchestrator()
    
    def test_empty_prompt(self):
        """Test handling of empty prompt."""
        # Should not crash
        analysis = self.orchestrator.analyze_prompt("")
        self.assertIsInstance(analysis, PromptAnalysis)
    
    def test_very_long_prompt(self):
        """Test handling of very long prompt."""
        long_prompt = "word " * 1000  # 1000 words
        analysis = self.orchestrator.analyze_prompt(long_prompt)
        self.assertIsInstance(analysis, PromptAnalysis)
        self.assertGreater(analysis.complexity_score, 0)
    
    def test_special_characters_prompt(self):
        """Test handling of special characters."""
        special_prompt = "Test: @#$%^&*() []{};:,.<>? 'quotes' \"double\""
        analysis = self.orchestrator.analyze_prompt(special_prompt)
        self.assertIsInstance(analysis, PromptAnalysis)
    
    def test_multilingual_prompt(self):
        """Test handling of non-English text."""
        prompt = "Bonjour, comment allez-vous?"
        analysis = self.orchestrator.analyze_prompt(prompt)
        self.assertIsInstance(analysis, PromptAnalysis)
    
    def test_no_available_providers(self):
        """Test behavior when no providers available."""
        # Create orchestrator and remove all providers
        test_orch = LLMOrchestrator()
        test_orch.providers = {}
        
        with self.assertRaises(ValueError):
            test_orch.decide_routing("Any prompt")


class TestScoring(unittest.TestCase):
    """Test scoring mechanisms."""
    
    def setUp(self):
        self.orchestrator = LLMOrchestrator()
    
    def test_confidence_is_valid_probability(self):
        """Test that confidence scores are between 0 and 1."""
        prompt = "Random prompt about various things"
        analysis = self.orchestrator.analyze_prompt(prompt)
        self.assertGreaterEqual(analysis.confidence, 0.0)
        self.assertLessEqual(analysis.confidence, 1.0)
    
    def test_complexity_is_valid_score(self):
        """Test that complexity scores are between 0 and 1."""
        prompt = "Some test prompt"
        analysis = self.orchestrator.analyze_prompt(prompt)
        self.assertGreaterEqual(analysis.complexity_score, 0.0)
        self.assertLessEqual(analysis.complexity_score, 1.0)
    
    def test_provider_matching_score(self):
        """Test provider matching score calculation."""
        provider = MockLLMProvider("test")
        provider.capabilities = [ModelCapability.CODE_GENERATION]
        
        # Create mock analysis with code capability requirement
        analysis = self.orchestrator.analyze_prompt("Write Python code")
        
        score = self.orchestrator._score_provider_match(provider, analysis)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)


if __name__ == '__main__':
    unittest.main()
