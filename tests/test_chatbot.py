"""
Tests for Chatbot Module
"""

import unittest
from src.chatbot import SimpleChatbot, CardCaptureBot, ConversationalBot


class TestSimpleChatbot(unittest.TestCase):
    """Test SimpleChatbot class"""
    
    def setUp(self):
        """Set up test bot"""
        self.bot = SimpleChatbot()
    
    def test_add_knowledge(self):
        """Test adding knowledge to bot"""
        self.bot.add_knowledge("What is this?", "This is a test.")
        self.assertIn("what is this?", self.bot.knowledge_base)
    
    def test_find_match_exact(self):
        """Test exact match finding"""
        self.bot.add_knowledge("Hello", "Hi there!")
        answer, confidence = self.bot.find_match("Hello")
        self.assertEqual(confidence, 1.0)
        self.assertEqual(answer, "Hi there!")
    
    def test_keyword_extraction(self):
        """Test keyword extraction"""
        keywords = self.bot._extract_keywords("How do I start the camera?")
        keywords_str = ' '.join(keywords).lower()
        self.assertIn("start", keywords_str)
        self.assertIn("camera", keywords_str)
        self.assertNotIn("how", keywords_str)  # Common word filtered
    
    def test_respond(self):
        """Test response generation"""
        self.bot.add_knowledge("What is Python?", "Python is a programming language.")
        response = self.bot.respond("What is Python?")
        self.assertEqual(response, "Python is a programming language.")
    
    def test_conversation_history(self):
        """Test conversation tracking"""
        self.bot.respond("Hello")
        self.bot.respond("How are you?")
        history = self.bot.get_history()
        self.assertEqual(len(history), 2)


class TestCardCaptureBot(unittest.TestCase):
    """Test CardCaptureBot"""
    
    def setUp(self):
        """Set up card capture bot"""
        self.bot = CardCaptureBot()
    
    def test_initialization(self):
        """Test bot initializes with knowledge base"""
        self.assertGreater(len(self.bot.knowledge_base), 0)
    
    def test_camera_question(self):
        """Test camera-related question"""
        response = self.bot.respond("How do I start the camera?")
        self.assertIsNotNone(response)
        self.assertIn("python", response.lower() or "camera" in response.lower())
    
    def test_help_message(self):
        """Test help message"""
        help_text = self.bot.get_help()
        self.assertIn("Camera", help_text)
        self.assertIn("support", help_text.lower())
    
    def test_fallback_response(self):
        """Test fallback for unknown query"""
        response = self.bot.respond("xyzabc123unknown")
        self.assertIsNotNone(response)
        # Should either find something or provide fallback
        self.assertGreater(len(response), 0)


class TestConversationalBot(unittest.TestCase):
    """Test ConversationalBot"""
    
    def setUp(self):
        """Set up conversational bot"""
        self.bot = ConversationalBot()
    
    def test_context_tracking(self):
        """Test context awareness"""
        user_id = "test_user"
        self.bot.respond_with_context("Tell me about cameras", user_id)
        self.assertIn(user_id, self.bot.user_profile)
    
    def test_topic_extraction(self):
        """Test topic extraction"""
        topic = self.bot._extract_topic("How to setup camera?")
        self.assertEqual(topic, "camera")
    
    def test_user_stats(self):
        """Test user statistics"""
        user_id = "alice"
        self.bot.respond_with_context("What about cameras?", user_id)
        self.bot.respond_with_context("How to optimize speed?", user_id)
        
        stats = self.bot.get_user_stats(user_id)
        self.assertEqual(stats['total_queries'], 2)


if __name__ == "__main__":
    unittest.main()
