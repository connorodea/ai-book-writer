"""Main script for running the book generation system - Updated for AutoGen v2"""
import os
import asyncio
from config_v2 import get_local_config, get_openai_config
from agents_v2 import BookAgents
from book_generator_v2 import BookGenerator
from outline_generator_v2 import OutlineGenerator

async def main():
    """Main function to run the book generation system"""
    print("🚀 Starting AI Book Writer v2.0")
    
    # Configuration - Choose your LLM backend
    use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"
    
    if use_openai:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ Error: OPENAI_API_KEY environment variable not set")
            print("Please set your OpenAI API key or use local LLM")
            return
        agent_config = get_openai_config(api_key, "gpt-4")
        print("🤖 Using OpenAI GPT-4")
    else:
        agent_config = get_local_config(port=1234, model_name="llama-3.1-8b-instruct")
        print("🏠 Using local LLM at localhost:1234")
    
    # Initial prompt for the book
    initial_prompt = """
    Create a story in my established writing style with these key elements:
    Its important that it has several key storylines that intersect and influence each other. The story should be set in a modern corporate environment, with a focus on technology and finance. The protagonist is a software engineer named Dane who has just completed a groundbreaking stock prediction algorithm. The algorithm predicts a catastrophic market crash, but Dane oversleeps and must rush to an important presentation to share his findings with executives. The tension arises from the questioning of whether his "error" might actually be correct.

    The piece is written in third-person limited perspective, following Dane's thoughts and experiences. The prose is direct and technical when describing the protagonist's work, but becomes more introspective during personal moments. The author employs a mix of dialogue and internal monologue, with particular attention to time progression and technical details around the algorithm and stock predictions.
    Story Arch:

    Setup: Dane completes a groundbreaking stock prediction algorithm late at night
    Initial Conflict: The algorithm predicts a catastrophic market crash
    Rising Action: Dane oversleeps and must rush to an important presentation
    Climax: The presentation to executives where he must explain his findings
    Tension Point: The questioning of whether his "error" might actually be correct

    Characters:

    Dane: The protagonist; a dedicated software engineer who prioritizes work over personal life. Wears grey polo shirts on Thursdays, tends to get lost in his work, and struggles with work-life balance. More comfortable with code than public speaking.
    Gary: Dane's nervous boss who seems caught between supporting Dane and managing upper management's expectations
    Jonathan Morego: Senior VP of Investor Relations who raises pointed questions about the validity of Dane's predictions
    Silence: Brief mention as an Uber driver
    C-Level Executives: Present as an audience during the presentation

    World Description:
    The story takes place in a contemporary corporate setting, likely a financial technology company. The world appears to be our modern one, with familiar elements like:

    Major tech companies (Tesla, Google, Apple, Microsoft)
    Stock market and financial systems
    Modern technology (neural networks, predictive analytics)
    Urban environment with rideshare services like Uber
    Corporate hierarchy and office culture

    The story creates tension between the familiar corporate world and the potential for an unprecedented financial catastrophe, blending elements of technical thriller with workplace drama. The setting feels grounded in reality but hints at potentially apocalyptic economic consequences.
    """

    num_chapters = 25
    
    try:
        # Create agents for outline generation
        print("📝 Creating outline generation agents...")
        outline_agents = BookAgents(agent_config)
        agents = outline_agents.create_agents(initial_prompt, num_chapters)
        
        # Generate the outline
        outline_gen = OutlineGenerator(agents, agent_config)
        print("📋 Generating book outline...")
        outline = await outline_gen.generate_outline_async(initial_prompt, num_chapters)
        
        if not outline:
            print("❌ Error: No outline was generated.")
            return
        
        print(f"✅ Generated outline with {len(outline)} chapters")
        
        # Print the generated outline
        print("\n📖 Generated Outline:")
        for chapter in outline:
            print(f"\nChapter {chapter['chapter_number']}: {chapter['title']}")
            print("-" * 50)
            print(chapter['prompt'])
        
        # Save the outline for reference
        print("\n💾 Saving outline to file...")
        with open("book_output/outline.txt", "w") as f:
            for chapter in outline:
                f.write(f"\nChapter {chapter['chapter_number']}: {chapter['title']}\n")
                f.write("-" * 50 + "\n")
                f.write(chapter['prompt'] + "\n")
        
        # Create new agents with outline context for book generation
        print("🔄 Creating book generation agents with outline context...")
        book_agents = BookAgents(agent_config, outline)
        agents_with_context = book_agents.create_agents(initial_prompt, num_chapters)
        
        # Initialize book generator with contextual agents
        book_gen = BookGenerator(agents_with_context, agent_config, outline)
        
        # Generate the book using the outline
        print("\n📚 Starting book generation...")
        await book_gen.generate_book_async(outline)
        
        print("\n🎉 Book generation completed!")
        print(f"📁 Check the 'book_output' directory for your generated book chapters")
        
    except KeyboardInterrupt:
        print("\n⏹️  Book generation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during book generation: {str(e)}")
        print("Check the logs above for more details")

def run_sync():
    """Synchronous wrapper for main function"""
    asyncio.run(main())

if __name__ == "__main__":
    run_sync()