"""
Chatbot Example - Interactive Chat Interface
Run this to chat with the card capture bot
"""

from src.chatbot import CardCaptureBot


def main():
    """Run interactive chatbot."""
    bot = CardCaptureBot()
    
    print(bot.get_help())
    print("\n" + "="*60 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for special commands
            if user_input.lower() in ['quit', 'exit']:
                print("\nBot: Goodbye! Have a great time with card capture! 👋")
                break
            
            elif user_input.lower() == 'help':
                print(f"\nBot:\n{bot.get_help()}\n")
                continue
            
            elif user_input.lower() == 'history':
                history = bot.get_history()
                if not history:
                    print("\nBot: No conversation history yet.\n")
                else:
                    print("\nBot: 📜 Conversation History")
                    print("="*60)
                    for i, msg in enumerate(history, 1):
                        print(f"\n{i}. You: {msg['user']}")
                        print(f"   Bot: {msg['bot']}")
                        conf = msg.get('confidence', 0)
                        print(f"   (Confidence: {conf:.1%})")
                    print("\n" + "="*60 + "\n")
                continue
            
            elif user_input.lower() == 'stats':
                stats = bot.get_history()
                print(f"\nBot: 📊 Stats")
                print(f"Questions answered: {len(stats)}")
                print(f"Total interactions: {bot.response_count}\n")
                continue
            
            # Get response
            response = bot.respond(user_input)
            print(f"\nBot: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\nBot: Goodbye! 👋")
            break
        except Exception as e:
            print(f"\nBot: Error: {e}\n")


if __name__ == "__main__":
    main()
