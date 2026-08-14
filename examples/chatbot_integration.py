"""
Chatbot Integration Example
Shows how to use the chatbot programmatically in your code
"""

from src import CardCaptureBot


def example_1_simple_qa():
    """Example 1: Simple Q&A"""
    print("\n" + "="*60)
    print("Example 1: Simple Q&A")
    print("="*60 + "\n")
    
    bot = CardCaptureBot()
    
    questions = [
        "How do I start the camera capture?",
        "What cameras are supported?",
        "How do I adjust card detection sensitivity?",
        "Where are captured images saved?",
    ]
    
    for question in questions:
        response = bot.respond(question)
        print(f"Q: {question}")
        print(f"A: {response}\n")


def example_2_batch_queries():
    """Example 2: Batch query processing"""
    print("\n" + "="*60)
    print("Example 2: Batch Query Processing")
    print("="*60 + "\n")
    
    bot = CardCaptureBot()
    
    queries = [
        "Can I use my phone camera?",
        "Cards not detecting",
        "How to run tests?",
        "GPU acceleration?",
    ]
    
    print("Processing batch queries:\n")
    for query in queries:
        response = bot.respond(query)
        print(f"Q: {query}")
        print(f"A: {response}")
        print("-" * 60)
    
    # Show stats
    history = bot.get_history()
    print(f"\nProcessed {len(history)} queries")


def example_3_programmatic_usage():
    """Example 3: Using bot in your application"""
    print("\n" + "="*60)
    print("Example 3: Programmatic Usage in Application")
    print("="*60 + "\n")
    
    bot = CardCaptureBot()
    
    # Example: Help system in camera capture app
    user_query = "I want to capture multiple cards at once"
    response = bot.respond(user_query)
    
    print("User asked:", user_query)
    print("Bot suggests:", response)
    
    print("\n" + "-"*60)
    
    # Example: Troubleshooting
    user_issue = "My images are too blurry"
    response = bot.respond(user_issue)
    
    print("\nUser reported:", user_issue)
    print("Bot solution:", response)


def example_4_conversational():
    """Example 4: Conversational with context"""
    print("\n" + "="*60)
    print("Example 4: Conversational Bot with Context")
    print("="*60 + "\n")
    
    from src import ConversationalBot
    
    bot = ConversationalBot()
    
    # Add custom knowledge
    bot.add_knowledge(
        "What's your name?",
        "I'm a Card Capture Assistant Bot! I help with camera setup and card detection.",
        ['name', 'who', 'you']
    )
    
    # Simulate multi-turn conversation
    user_id = "alice"
    
    queries = [
        "How do I start?",
        "Can I use multiple cameras?",
        "How to optimize speed?",
    ]
    
    for query in queries:
        response = bot.respond_with_context(query, user_id)
        print(f"{user_id}: {query}")
        print(f"Bot: {response}\n")
    
    # Get user profile
    stats = bot.get_user_stats(user_id)
    print("-" * 60)
    print(f"\nUser Profile for '{user_id}':")
    print(f"  Questions asked: {stats['total_queries']}")
    print(f"  Topics discussed: {', '.join(stats['topics_discussed'])}")


def example_5_custom_bot():
    """Example 5: Custom bot with domain knowledge"""
    print("\n" + "="*60)
    print("Example 5: Custom Domain-Specific Bot")
    print("="*60 + "\n")
    
    from src import SimpleChatbot
    
    bot = SimpleChatbot()
    
    # Add custom knowledge base
    custom_kb = [
        ("What is OCR?", "Optical Character Recognition - extracting text from images"),
        ("How to extract card numbers?", "Use Tesseract OCR or ML models trained on card data"),
        ("What's computer vision?", "The field of AI that helps computers understand images"),
    ]
    
    for question, answer in custom_kb:
        bot.add_knowledge(question, answer)
    
    # Query the bot
    test_queries = [
        "Tell me about OCR",
        "How do I extract data?",
        "What is computer vision?",
    ]
    
    for query in test_queries:
        response = bot.respond(query)
        print(f"Q: {query}")
        print(f"A: {response}\n")


def run_all_examples():
    """Run all examples."""
    examples = [
        ("Simple Q&A", example_1_simple_qa),
        ("Batch Queries", example_2_batch_queries),
        ("Programmatic Usage", example_3_programmatic_usage),
        ("Conversational Bot", example_4_conversational),
        ("Custom Domain Bot", example_5_custom_bot),
    ]
    
    print("\n" + "="*60)
    print("CHATBOT EXAMPLES")
    print("="*60)
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"Error in {name}: {e}")
        print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        examples = {
            '1': example_1_simple_qa,
            '2': example_2_batch_queries,
            '3': example_3_programmatic_usage,
            '4': example_4_conversational,
            '5': example_5_custom_bot,
        }
        
        if example_num in examples:
            examples[example_num]()
        else:
            print(f"Example {example_num} not found. Available: 1-5")
    else:
        run_all_examples()
