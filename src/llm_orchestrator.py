"""
LLM Orchestrator - Dynamic LLM Selection Engine
Routes prompts to the most suitable LLM based on analysis of prompt characteristics.
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import os


class PromptType(Enum):
    """Categorization of prompt types."""
    CODE = "code"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    CONVERSATIONAL = "conversational"
    TECHNICAL = "technical"
    DOMAIN_SPECIFIC = "domain_specific"
    MATH = "math"
    REASONING = "reasoning"


class ModelCapability(Enum):
    """LLM model capabilities."""
    CODE_GENERATION = "code_generation"
    CODE_ANALYSIS = "code_analysis"
    CREATIVE_WRITING = "creative_writing"
    LOGICAL_REASONING = "logical_reasoning"
    MATH_SOLVING = "math_solving"
    CONVERSATIONAL = "conversational"
    DOMAIN_KNOWLEDGE = "domain_knowledge"
    VISION = "vision"
    LONG_CONTEXT = "long_context"


@dataclass
class PromptAnalysis:
    """Results of prompt analysis."""
    prompt_type: PromptType
    confidence: float
    keywords: List[str]
    complexity_score: float
    required_capabilities: List[ModelCapability]
    domain_tags: List[str]


@dataclass
class RoutingDecision:
    """Orchestrator's routing decision."""
    selected_model: str
    reasoning: str
    alternative_models: List[Tuple[str, float]]
    analysis: PromptAnalysis


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv(f"{model_name.upper()}_API_KEY")
        self.capabilities: List[ModelCapability] = []
        self.max_tokens = 2048
        self.latency_ms = 0
        self.cost_per_1k_tokens = 0.0
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from the prompt."""
        pass
    
    def is_available(self) -> bool:
        """Check if provider is available."""
        return self.api_key is not None
    
    def get_cost_estimate(self, tokens: int) -> float:
        """Estimate cost for token count."""
        return (tokens / 1000) * self.cost_per_1k_tokens


class GoogleGeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider."""
    
    def __init__(self, model_name: str = "gemini-pro", api_key: Optional[str] = None):
        super().__init__(model_name, api_key)
        self.capabilities = [
            ModelCapability.CODE_GENERATION,
            ModelCapability.CODE_ANALYSIS,
            ModelCapability.CONVERSATIONAL,
            ModelCapability.CREATIVE_WRITING,
            ModelCapability.LOGICAL_REASONING,
            ModelCapability.DOMAIN_KNOWLEDGE
        ]
        self.max_tokens = 32000
        self.latency_ms = 800
        self.cost_per_1k_tokens = 0.00075
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(model_name)
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini: {e}")
                self.model = None
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Gemini."""
        if not self.model:
            return "Gemini model not available"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"


class MockLLMProvider(BaseLLMProvider):
    """Mock LLM provider for testing."""
    
    def __init__(self, model_name: str = "mock-model"):
        super().__init__(model_name, api_key="mock-key")
        self.capabilities = list(ModelCapability)
        self.responses = {}
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate mock response."""
        return f"[{self.model_name}] Response to: {prompt[:50]}..."
    
    def set_response(self, prompt: str, response: str):
        """Set predefined response for testing."""
        self.responses[prompt] = response


class PromptAnalyzer:
    """Analyzes prompts to determine optimal routing."""
    
    # Domain-specific keywords
    CODE_KEYWORDS = {
        'python', 'javascript', 'java', 'code', 'function', 'class', 'def', 'return',
        'debug', 'algorithm', 'refactor', 'optimize', 'syntax', 'error', 'exception'
    }
    
    CREATIVE_KEYWORDS = {
        'story', 'poem', 'creative', 'write', 'imagine', 'fiction', 'character',
        'dialogue', 'narrative', 'describe', 'artistic', 'compose'
    }
    
    ANALYTICAL_KEYWORDS = {
        'analyze', 'explain', 'why', 'how', 'compare', 'evaluate', 'assess',
        'data', 'statistics', 'trend', 'pattern', 'insight', 'finding'
    }
    
    MATH_KEYWORDS = {
        'calculate', 'solve', 'equation', 'formula', 'math', 'number',
        'probability', 'geometry', 'algebra', 'derivative', 'integral'
    }
    
    REASONING_KEYWORDS = {
        'logic', 'reasoning', 'prove', 'argument', 'conclusion', 'hypothesis',
        'evidence', 'infer', 'deduce', 'syllogism', 'premise', 'logical',
        'proof', 'demonstrate', 'establish', 'justify', 'valid'
    }
    
    DOMAIN_KEYWORDS = {
        'medical', 'legal', 'financial', 'technical', 'academic', 'scientific',
        'business', 'marketing', 'sales', 'customer', 'product', 'service'
    }
    
    def __init__(self):
        self.prompt_history = []
    
    def analyze(self, prompt: str) -> PromptAnalysis:
        """
        Analyze prompt to determine type and characteristics.
        
        Args:
            prompt: Input prompt to analyze
            
        Returns:
            PromptAnalysis with classification results
        """
        prompt_lower = prompt.lower()
        self.prompt_history.append(prompt)
        
        # Extract keywords
        keywords = self._extract_keywords(prompt_lower)
        
        # Score for each prompt type
        scores = {
            PromptType.CODE: self._score_code(prompt_lower, keywords),
            PromptType.CREATIVE: self._score_creative(prompt_lower, keywords),
            PromptType.ANALYTICAL: self._score_analytical(prompt_lower, keywords),
            PromptType.MATH: self._score_math(prompt_lower, keywords),
            PromptType.REASONING: self._score_reasoning(prompt_lower, keywords),
            PromptType.CONVERSATIONAL: 0.5,  # Default base score
            PromptType.TECHNICAL: self._score_technical(prompt_lower, keywords),
            PromptType.DOMAIN_SPECIFIC: self._score_domain(prompt_lower, keywords),
        }
        
        # Determine primary type
        primary_type = max(scores, key=scores.get)
        confidence = min(scores[primary_type], 1.0)
        
        # Calculate complexity
        complexity_score = self._calculate_complexity(prompt)
        
        # Determine required capabilities
        capabilities = self._map_capabilities(primary_type, keywords)
        
        # Extract domain tags
        domain_tags = self._extract_domain_tags(prompt_lower, keywords)
        
        return PromptAnalysis(
            prompt_type=primary_type,
            confidence=confidence,
            keywords=keywords,
            complexity_score=complexity_score,
            required_capabilities=capabilities,
            domain_tags=domain_tags
        )
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Split by whitespace and punctuation
        words = re.findall(r'\b\w+\b', text)
        # Filter short words and common stopwords
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'of', 'in', 'to'}
        return [w for w in words if len(w) > 2 and w not in stopwords]
    
    def _score_code(self, prompt: str, keywords: List[str]) -> float:
        """Score likelihood of being a code-related prompt."""
        score = 0.0
        if any(kw in prompt for kw in self.CODE_KEYWORDS):
            score += 0.8
        # Check for code patterns (indentation, brackets, etc.)
        if '```' in prompt or re.search(r'def |class |function |return |if ', prompt):
            score += 0.7
        return min(score, 1.0)
    
    def _score_creative(self, prompt: str, keywords: List[str]) -> float:
        """Score likelihood of being creative content."""
        score = 0.0
        if any(kw in prompt for kw in self.CREATIVE_KEYWORDS):
            score += 0.8
        # Check for open-ended questions
        if prompt.count('?') > 2 or any(q in prompt for q in ['imagine', 'how would', 'what if']):
            score += 0.3
        return min(score, 1.0)
    
    def _score_analytical(self, prompt: str, keywords: List[str]) -> float:
        """Score likelihood of being analytical."""
        score = 0.0
        if any(kw in prompt for kw in self.ANALYTICAL_KEYWORDS):
            score += 0.8
        return min(score, 1.0)
    
    def _score_math(self, prompt: str, keywords: List[str]) -> float:
        """Score likelihood of being math-related."""
        score = 0.0
        if any(kw in prompt for kw in self.MATH_KEYWORDS):
            score += 0.8
        # Check for mathematical symbols
        if re.search(r'[\+\-\*/=∑∏∫√]', prompt):
            score += 0.5
        return min(score, 1.0)
    
    def _score_reasoning(self, prompt: str, keywords: List[str]) -> float:
        """Score likelihood of requiring logical reasoning."""
        score = 0.0
        if any(kw in prompt for kw in self.REASONING_KEYWORDS):
            score += 1.0  # Boost when reasoning keywords found
        return min(score, 1.0)
    
    def _score_technical(self, prompt: str, keywords: List[str]) -> float:
        """Score likelihood of being technical."""
        technical_patterns = ['api', 'database', 'server', 'client', 'protocol', 'framework']
        score = sum(0.3 for pattern in technical_patterns if pattern in prompt)
        return min(score, 1.0)
    
    def _score_domain(self, prompt: str, keywords: List[str]) -> float:
        """Score likelihood of being domain-specific."""
        score = 0.0
        if any(kw in prompt for kw in self.DOMAIN_KEYWORDS):
            score += 0.6
        return min(score, 1.0)
    
    def _calculate_complexity(self, prompt: str) -> float:
        """
        Calculate complexity score (0.0 to 1.0).
        Based on length, technical vocabulary, and question count.
        """
        score = 0.0
        
        # Length factor
        words = len(prompt.split())
        if words > 100:
            score += 0.3
        elif words > 50:
            score += 0.15
        
        # Question count
        score += min(prompt.count('?') * 0.1, 0.3)
        
        # Technical vocabulary
        tech_words = sum(1 for word in prompt.split() if len(word) > 10)
        score += min(tech_words * 0.02, 0.2)
        
        # Nested or complex structures
        if prompt.count('(') > 2 or prompt.count('[') > 2:
            score += 0.2
        
        return min(score, 1.0)
    
    def _map_capabilities(self, prompt_type: PromptType, keywords: List[str]) -> List[ModelCapability]:
        """Map prompt type to required model capabilities."""
        mapping = {
            PromptType.CODE: [
                ModelCapability.CODE_GENERATION,
                ModelCapability.CODE_ANALYSIS,
                ModelCapability.LOGICAL_REASONING
            ],
            PromptType.CREATIVE: [
                ModelCapability.CREATIVE_WRITING,
                ModelCapability.CONVERSATIONAL
            ],
            PromptType.ANALYTICAL: [
                ModelCapability.LOGICAL_REASONING,
                ModelCapability.DOMAIN_KNOWLEDGE
            ],
            PromptType.MATH: [
                ModelCapability.MATH_SOLVING,
                ModelCapability.LOGICAL_REASONING
            ],
            PromptType.REASONING: [
                ModelCapability.LOGICAL_REASONING,
                ModelCapability.DOMAIN_KNOWLEDGE
            ],
            PromptType.CONVERSATIONAL: [ModelCapability.CONVERSATIONAL],
            PromptType.TECHNICAL: [
                ModelCapability.DOMAIN_KNOWLEDGE,
                ModelCapability.CODE_ANALYSIS
            ],
            PromptType.DOMAIN_SPECIFIC: [
                ModelCapability.DOMAIN_KNOWLEDGE,
                ModelCapability.LOGICAL_REASONING
            ],
        }
        return mapping.get(prompt_type, [ModelCapability.CONVERSATIONAL])
    
    def _extract_domain_tags(self, prompt: str, keywords: List[str]) -> List[str]:
        """Extract domain-specific tags from prompt."""
        domains = []
        domain_mapping = {
            'medical': ['doctor', 'patient', 'disease', 'treatment', 'medication', 'health', 'symptoms', 'diabetes', 'diagnosis'],
            'legal': ['law', 'court', 'contract', 'attorney', 'lawsuit', 'regulation', 'legal', 'litigation'],
            'financial': ['money', 'investment', 'stock', 'crypto', 'budget', 'loan', 'finance', 'portfolio'],
            'technical': ['api', 'database', 'server', 'protocol', 'framework', 'algorithm', 'architecture'],
            'academic': ['research', 'thesis', 'paper', 'study', 'hypothesis', 'academic', 'education'],
        }
        
        for domain, domain_keywords in domain_mapping.items():
            if any(kw in prompt.lower() for kw in domain_keywords):
                domains.append(domain)
        
        return domains


class LLMOrchestrator:
    """
    Main orchestrator that routes prompts to optimal LLM.
    Dynamically selects the best model based on prompt analysis.
    """
    
    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.analyzer = PromptAnalyzer()
        self.model_profiles: Dict[str, Dict[str, Any]] = {}
        self.routing_history = []
        
        # Register default providers
        self._register_default_providers()
    
    def _register_default_providers(self):
        """Register default LLM providers."""
        # Google Gemini
        gemini = GoogleGeminiProvider()
        self.providers['gemini-pro'] = gemini
        self.model_profiles['gemini-pro'] = {
            'name': 'Google Gemini',
            'strengths': ['reasoning', 'coding', 'multi-domain'],
            'latency': 'medium',
            'cost': 'low',
            'max_tokens': 32000,
        }
        
        # Mock provider for testing
        mock = MockLLMProvider('test-model')
        self.providers['test-model'] = mock
        self.model_profiles['test-model'] = {
            'name': 'Test Model',
            'strengths': ['testing'],
            'latency': 'fast',
            'cost': 'free',
            'max_tokens': 2048,
        }
    
    def register_provider(self, name: str, provider: BaseLLMProvider, profile: Dict[str, Any]):
        """
        Register a new LLM provider.
        
        Args:
            name: Unique provider name
            provider: BaseLLMProvider instance
            profile: Provider metadata and characteristics
        """
        self.providers[name] = provider
        self.model_profiles[name] = profile
    
    def analyze_prompt(self, prompt: str) -> PromptAnalysis:
        """
        Analyze a prompt without routing.
        
        Args:
            prompt: Input prompt to analyze
            
        Returns:
            PromptAnalysis with detailed breakdown
        """
        return self.analyzer.analyze(prompt)
    
    def decide_routing(self, prompt: str, **kwargs) -> RoutingDecision:
        """
        Decide which LLM to route the prompt to without executing.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters (prefer_speed, prefer_cost, prefer_quality)
            
        Returns:
            RoutingDecision with selected model and reasoning
        """
        analysis = self.analyzer.analyze(prompt)
        
        # Score each provider
        provider_scores = {}
        for name, provider in self.providers.items():
            if not provider.is_available():
                continue
            
            score = self._score_provider_match(
                provider, analysis, **kwargs
            )
            provider_scores[name] = score
        
        if not provider_scores:
            raise ValueError("No available LLM providers")
        
        # Select best provider
        selected = max(provider_scores, key=provider_scores.get)
        
        # Sort alternatives
        alternatives = sorted(
            [(name, score) for name, score in provider_scores.items() if name != selected],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        reasoning = self._generate_routing_reasoning(
            selected, analysis, provider_scores, kwargs
        )
        
        decision = RoutingDecision(
            selected_model=selected,
            reasoning=reasoning,
            alternative_models=alternatives,
            analysis=analysis
        )
        
        self.routing_history.append(decision)
        return decision
    
    def _score_provider_match(self, provider: BaseLLMProvider, analysis: PromptAnalysis, **kwargs) -> float:
        """Calculate match score between provider capabilities and prompt needs."""
        score = 0.0
        
        # Capability match (primary factor)
        matching_capabilities = sum(
            1 for cap in analysis.required_capabilities 
            if cap in provider.capabilities
        )
        capability_score = matching_capabilities / max(len(analysis.required_capabilities), 1)
        score += capability_score * 0.5
        
        # Confidence in classification
        score += analysis.confidence * 0.2
        
        # Cost preference
        if kwargs.get('prefer_cost'):
            score += (1.0 - min(provider.cost_per_1k_tokens / 0.001, 1.0)) * 0.15
        
        # Speed preference
        if kwargs.get('prefer_speed'):
            score += (1.0 - min(provider.latency_ms / 2000, 1.0)) * 0.15
        
        # Quality preference (assume higher cost = better quality)
        if kwargs.get('prefer_quality'):
            score += min(provider.cost_per_1k_tokens / 0.001, 1.0) * 0.15
        else:
            # Default: balance
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_routing_reasoning(self, selected: str, analysis: PromptAnalysis, scores: Dict, kwargs: Dict) -> str:
        """Generate human-readable reasoning for routing decision."""
        reasoning = f"Selected '{selected}' for {analysis.prompt_type.value} prompt "
        reasoning += f"(confidence: {analysis.confidence:.1%}). "
        reasoning += f"Required capabilities: {', '.join(c.value for c in analysis.required_capabilities[:3])}. "
        
        if kwargs.get('prefer_speed'):
            reasoning += "Prioritized speed. "
        if kwargs.get('prefer_cost'):
            reasoning += "Prioritized cost efficiency. "
        if kwargs.get('prefer_quality'):
            reasoning += "Prioritized response quality. "
        
        return reasoning.strip()
    
    def orchestrate(self, prompt: str, **kwargs) -> Tuple[str, RoutingDecision]:
        """
        Main orchestration method - analyze prompt and generate response.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional routing preferences
            
        Returns:
            Tuple of (response, routing_decision)
        """
        decision = self.decide_routing(prompt, **kwargs)
        provider = self.providers[decision.selected_model]
        
        response = provider.generate(prompt, **kwargs)
        
        return response, decision
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get statistics about routing decisions."""
        if not self.routing_history:
            return {"total_routes": 0}
        
        type_counts = {}
        model_counts = {}
        
        for decision in self.routing_history:
            ptype = decision.analysis.prompt_type.value
            type_counts[ptype] = type_counts.get(ptype, 0) + 1
            model_counts[decision.selected_model] = model_counts.get(decision.selected_model, 0) + 1
        
        return {
            "total_routes": len(self.routing_history),
            "by_prompt_type": type_counts,
            "by_model": model_counts,
            "average_confidence": sum(d.analysis.confidence for d in self.routing_history) / len(self.routing_history),
        }
    
    def generate_routing_report(self) -> str:
        """Generate a detailed routing report."""
        stats = self.get_routing_stats()
        
        report = "=== LLM Orchestrator Routing Report ===\n"
        report += f"Total Routing Decisions: {stats['total_routes']}\n"
        report += f"Average Confidence: {stats.get('average_confidence', 0):.1%}\n\n"
        
        report += "By Prompt Type:\n"
        for ptype, count in stats.get('by_prompt_type', {}).items():
            report += f"  {ptype}: {count}\n"
        
        report += "\nBy Model:\n"
        for model, count in stats.get('by_model', {}).items():
            report += f"  {model}: {count}\n"
        
        return report
