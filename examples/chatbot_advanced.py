"""
Advanced Chatbot Example - Conversational Bot with Context
Demonstrates conversational awareness and user profiling
"""

from src.chatbot import ConversationalBot


def main():
    """Run conversational chatbot with context."""
    
    # Initialize bot with custom knowledge
    bot = ConversationalBot()
    
    # Add general knowledge
    knowledge = [
        {
            'q': 'What is card camera capture?',
            'a': 'It\'s an automated system that detects and captures images of credit/debit cards using computer vision and OpenCV.',
            'k': ['card', 'capture', 'what']
        },
        {
            'q': 'Can you help me get started?',
            'a': 'Sure! Start with `python main.py` to launch the camera feed. Cards will be automatically detected and captured.',
            'k': ['help', 'started', 'start']
        },
        {
            'q': 'Tell me more about the project',
            'a': 'The Card Camera Capture project enables real-time detection of credit/debit cards and automatic image capture. Great for document processing and vision AI integration.',
            'k': ['project', 'about', 'more']
        },
    ]
    
    for item in knowledge:
        bot.add_knowledge(item['q'], item['a'], item['k'])
    
    print("="*60)
    print("🤖 Advanced Conversational Chatbot")
    print("="*60)
    print("\nI remember our conversation and adapt my responses!")
    print("Commands: 'quit', 'help', 'stats', 'profile'\n")
    
    user_id = input("Enter your name (default: user): ").strip() or "user"
    print(f"\nHello {user_id}! Let's chat about card capture.\n")
    
    while True:
        try:
            user_input = input(f"{user_id}: ").strip()
            
            if not user_input:
                continue
            
            # Special commands
            if user_input.lower() in ['quit', 'exit']:
                stats = bot.get_user_stats(user_id)
                print(f"\nBot: Thanks for chatting, {user_id}! 👋")
                print(f"Summary: You asked {stats['total_queries']} questions about {', '.join(stats['topics_discussed']) or 'various topics'}.\n")
                break
            
            elif user_input.lower() == 'help':
                print("""
Bot: Here's what I can help with:
  • Camera setup and configuration
  • Card detection and troubleshooting
  • Usage examples and integration
  • Performance optimization
  
Commands:
  • 'quit' - End conversation
  • 'stats' - Show conversation stats
  • 'profile' - Show your profile
  • 'help' - Show this help\n""")
                continue
            
            elif user_input.lower() == 'stats':
                history = bot.get_history()
                print(f"\nBot: 📊 Conversation Stats")
                print(f"Questions asked: {len(history)}")
                print(f"Topics: {', '.join(set(bot.user_profile.get(user_id, {}).get('topics', []))) or 'None yet'}\n")
                continue
            
            elif user_input.lower() == 'profile':
                stats = bot.get_user_stats(user_id)
                print(f"\nBot: 👤 Your Profile")
                print(f"Name: {user_id}")
                print(f"Total Questions: {stats['total_queries']}")
                print(f"Topics Discussed: {', '.join(stats['topics_discussed']) or 'None'}\n")
                continue
            
            # Get contextual response
            response = bot.respond_with_context(user_input, user_id)
            print(f"\nBot: {response}\n")
        
        except KeyboardInterrupt:
            print(f"\n\nBot: Goodbye, {user_id}! 👋\n")
            break
        except Exception as e:
            print(f"\nBot: Error: {e}\n")


if __name__ == "__main__":
    main()
