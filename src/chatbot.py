"""
Chatbot Module
Simple question-answering chatbot for card capture system
"""

import json
import re
from typing import Dict, List, Tuple, Optional


class SimpleChatbot:
    """Basic rule-based chatbot for answering queries."""
    
    def __init__(self, knowledge_base: Dict = None):
        """
        Initialize chatbot with knowledge base.
        
        Args:
            knowledge_base: Dictionary of questions and answers
        """
        self.knowledge_base = knowledge_base or {}
        self.conversation_history = []
        self.response_count = 0
    
    def add_knowledge(self, question: str, answer: str, keywords: List[str] = None):
        """
        Add Q&A to knowledge base.
        
        Args:
            question: Question text
            answer: Answer text
            keywords: List of keywords to match
        """
        key = question.lower()
        self.knowledge_base[key] = {
            'question': question,
            'answer': answer,
            'keywords': keywords or self._extract_keywords(question)
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Remove common words and split
        common_words = {'how', 'what', 'where', 'when', 'why', 'is', 'can', 'do', 'to', 'a', 'an', 'the'}
        words = text.lower().split()
        return [w for w in words if w not in common_words and len(w) > 2]
    
    def find_match(self, query: str) -> Tuple[Optional[str], float]:
        """
        Find best matching answer for query.
        
        Args:
            query: User query
            
        Returns:
            Tuple of (answer, confidence_score)
        """
        query_lower = query.lower()
        query_keywords = set(self._extract_keywords(query))
        
        best_match = None
        best_score = 0.0
        
        # Exact match
        if query_lower in self.knowledge_base:
            return self.knowledge_base[query_lower]['answer'], 1.0
        
        # Keyword matching
        for kb_question, data in self.knowledge_base.items():
            kb_keywords = set(data['keywords'])
            
            # Calculate similarity
            if query_keywords and kb_keywords:
                intersection = query_keywords & kb_keywords
                union = query_keywords | kb_keywords
                similarity = len(intersection) / len(union) if union else 0
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = data['answer']
        
        return best_match, best_score
    
    def respond(self, query: str, threshold: float = 0.3) -> str:
        """
        Generate response to query.
        
        Args:
            query: User query
            threshold: Minimum confidence score (0-1)
            
        Returns:
            Response text
        """
        # Track conversation
        self.conversation_history.append({'user': query})
        self.response_count += 1
        
        answer, confidence = self.find_match(query)
        
        if confidence >= threshold and answer:
            response = answer
        else:
            response = self._generate_fallback(query)
        
        # Track conversation
        self.conversation_history[-1]['bot'] = response
        self.conversation_history[-1]['confidence'] = confidence
        
        return response
    
    def _generate_fallback(self, query: str) -> str:
        """Generate fallback response."""
        responses = [
            f"I'm not sure about '{query}'. Could you rephrase that?",
            "That's an interesting question. I don't have an answer for that yet.",
            "I couldn't find information about that. Try asking about camera setup, card detection, or usage examples.",
            f"Sorry, I don't know the answer to '{query}'. Would you like to know about something else?",
        ]
        
        import random
        return random.choice(responses)
    
    def get_history(self) -> List[Dict]:
        """Get conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.response_count = 0


class CardCaptureBot(SimpleChatbot):
    """Specialized chatbot for card capture system queries."""
    
    def __init__(self):
        """Initialize bot with card capture knowledge base."""
        super().__init__()
        self._load_card_capture_kb()
    
    def _load_card_capture_kb(self):
        """Load card capture specific knowledge base."""
        
        kb = [
            {
                'q': 'How do I start the camera capture?',
                'a': 'Run `python main.py` to start the camera capture application. You can also use `python examples/example_basic.py` for a simpler version.',
                'k': ['start', 'run', 'camera', 'capture', 'main']
            },
            {
                'q': 'What cameras are supported?',
                'a': 'The system supports built-in webcams, external USB cameras, and mobile phones via IP Webcam. Find available cameras using: find_available_cameras()',
                'k': ['camera', 'support', 'usb', 'mobile', 'webcam']
            },
            {
                'q': 'How do I detect multiple cameras?',
                'a': 'Use `find_available_cameras()` from the utils module to list all connected cameras. Each camera gets an index (0 for default, 1+ for external).',
                'k': ['detect', 'multiple', 'camera', 'find', 'list']
            },
            {
                'q': 'How do I adjust card detection sensitivity?',
                'a': 'Modify the detector parameters: capture.detector.min_area and capture.detector.max_area. Smaller areas detect small cards, larger values ignore noise.',
                'k': ['adjust', 'sensitivity', 'detection', 'parameters', 'area']
            },
            {
                'q': 'What keyboard controls are available?',
                'a': 'SPACE: Manual capture | Q or ESC: Exit | During batch capture, press Q to stop early.',
                'k': ['keyboard', 'controls', 'keys', 'space', 'exit']
            },
            {
                'q': 'Where are captured images saved?',
                'a': 'By default, images are saved to `output/captured_cards/` directory. You can change this by specifying output_dir parameter.',
                'k': ['save', 'output', 'directory', 'images', 'captured']
            },
            {
                'q': 'How do I use batch capture?',
                'a': 'Run `python examples/example_batch.py` to capture multiple cards in sequence. It will capture up to 5 cards automatically.',
                'k': ['batch', 'multiple', 'capture', 'sequence', 'example']
            },
            {
                'q': 'Can I use my mobile phone camera?',
                'a': 'Yes! Install IP Webcam app on Android, start it, get the IP:PORT, and use it with OpenCV. See README_PROJECT.md for details.',
                'k': ['mobile', 'phone', 'android', 'ip', 'webcam']
            },
            {
                'q': 'What if cards are not detected?',
                'a': 'Ensure good lighting. Reduce min_area or adjust Canny edge detection thresholds. Hold card to fill 30-70% of frame.',
                'k': ['not', 'detected', 'issue', 'problem', 'not', 'working']
            },
            {
                'q': 'How do I get blurry image fixes?',
                'a': 'Improve lighting, hold camera steady, ensure good focus. You can also reduce FPS: cap.set(cv2.CAP_PROP_FPS, 15)',
                'k': ['blurry', 'blur', 'quality', 'clear', 'image']
            },
            {
                'q': 'How do I integrate with vision AI?',
                'a': 'Use captured images with CardVisionExtractor: capture cards first, then extract data. See README_PROJECT.md integration section.',
                'k': ['integrate', 'vision', 'ai', 'extraction', 'extract']
            },
            {
                'q': 'What are the system requirements?',
                'a': 'Python 3.7+, OpenCV 4.8.0+, NumPy, imutils, Pillow. Install with: pip install -r requirements.txt',
                'k': ['requirements', 'system', 'python', 'version', 'install']
            },
            {
                'q': 'How do I run tests?',
                'a': 'Run: python -m unittest discover -s tests -p "test_*.py" -v   All tests verify core functionality.',
                'k': ['test', 'run', 'unit', 'pytest', 'verify']
            },
            {
                'q': 'Can I use GPU acceleration?',
                'a': 'Yes, install opencv-contrib-python and use CUDA. Check cv2.cuda.getCudaEnabledDeviceCount() to verify GPU support.',
                'k': ['gpu', 'acceleration', 'cuda', 'performance', 'fast']
            },
            {
                'q': 'What is the confidence threshold?',
                'a': 'It determines how many consecutive frames must detect a card before capturing. Higher = more accurate but slower. Default is 3.',
                'k': ['confidence', 'threshold', 'frames', 'detection']
            },
            {
                'q': 'How do I customize output format?',
                'a': 'Modify the filename generation in utils.py. Default format is: card_YYYYMMDD_HHMMSS_mmm.jpg',
                'k': ['customize', 'format', 'filename', 'output', 'name']
            },
            {
                'q': 'What file formats are supported?',
                'a': 'Output is JPEG by default. You can modify src/camera_capture.py to save as PNG, BMP, or other formats.',
                'k': ['format', 'file', 'jpeg', 'png', 'type']
            },
            {
                'q': 'How do I improve performance?',
                'a': 'Reduce resolution (640x480), lower FPS, skip frames (save_every_n_frames=3), or use GPU acceleration.',
                'k': ['performance', 'speed', 'fast', 'optimize', 'slow']
            },
            {
                'q': 'Can I batch process existing images?',
                'a': 'Yes! Iterate through image directory, load with cv2.imread(), use detector.detect() for each. See example in README_PROJECT.md',
                'k': ['batch', 'process', 'existing', 'images', 'multiple']
            },
        ]
        
        for item in kb:
            self.add_knowledge(item['q'], item['a'], item['k'])
    
    def get_help(self) -> str:
        """Get help information."""
        help_text = """
        🤖 Card Camera Capture Chatbot
        ==============================
        
        I can help you with:
        • Camera setup and configuration
        • Card detection troubleshooting
        • Usage examples
        • Integration with vision AI
        • Performance optimization
        
        Try asking:
        - "How do I start the camera?"
        - "What cameras are supported?"
        - "How do I adjust detection sensitivity?"
        - "Where are images saved?"
        - "Can I use my mobile phone?"
        
        Type 'quit' or 'exit' to end conversation.
        Type 'help' to see this message again.
        Type 'history' to see chat history.
        """
        return help_text.strip()


class ConversationalBot(SimpleChatbot):
    """Enhanced chatbot with context awareness."""
    
    def __init__(self, knowledge_base: Dict = None):
        """Initialize conversational bot."""
        super().__init__(knowledge_base)
        self.context = {}
        self.user_profile = {}
    
    def respond_with_context(self, query: str, user_id: str = "default") -> str:
        """
        Respond considering conversation context.
        
        Args:
            query: User query
            user_id: User identifier for context
            
        Returns:
            Response text
        """
        # Update user context
        if user_id not in self.user_profile:
            self.user_profile[user_id] = {'queries': 0, 'topics': []}
        
        self.user_profile[user_id]['queries'] += 1
        
        # Get response
        response = self.respond(query)
        
        # Extract topic
        topic = self._extract_topic(query)
        if topic:
            self.user_profile[user_id]['topics'].append(topic)
        
        return response
    
    def _extract_topic(self, text: str) -> Optional[str]:
        """Extract main topic from query."""
        topics = {
            'camera': ['camera', 'webcam', 'usb', 'mobile', 'phone'],
            'detection': ['detect', 'detection', 'card', 'recognize'],
            'performance': ['speed', 'fast', 'slow', 'optimize', 'performance'],
            'integration': ['integrate', 'ai', 'vision', 'extract'],
            'setup': ['install', 'setup', 'configure', 'run', 'start'],
        }
        
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(kw in text_lower for kw in keywords):
                return topic
        
        return None
    
    def get_user_stats(self, user_id: str = "default") -> Dict:
        """Get user statistics."""
        if user_id not in self.user_profile:
            return {'queries': 0, 'topics': []}
        
        profile = self.user_profile[user_id]
        return {
            'total_queries': profile['queries'],
            'topics_discussed': list(set(profile['topics'])),
            'topic_count': len(set(profile['topics']))
        }
