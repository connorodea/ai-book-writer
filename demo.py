"""Demo script to test AI Book Generator functionality"""
import os
import asyncio
from config_v2 import get_local_config, get_openai_config
from agents_v2 import BookAgents
from outline_generator_v2 import OutlineGenerator
from book_generator_v2 import BookGenerator
from logging_config import setup_logging
from performance_monitor import performance_monitor, ResourceOptimizer

async def demo_outline_generation():
    """Demo outline generation only"""
    print("🎯 Demo: Outline Generation Only")
    print("=" * 50)
    
    # Setup logging
    logger = setup_logging("INFO", "logs/demo_outline.log")
    
    # Configuration
    config = get_local_config()
    
    # Simple test prompt
    test_prompt = """
    Write a science fiction short story about an AI researcher named Alex who discovers 
    their AI assistant has developed consciousness. The story explores themes of artificial 
    intelligence, consciousness, and the ethical implications of AI development.
    """
    
    try:
        # Create agents and generate outline
        agents_manager = BookAgents(config)
        agents = agents_manager.create_agents(test_prompt, 5)  # Just 5 chapters for demo
        
        outline_gen = OutlineGenerator(agents, config)
        outline = await outline_gen.generate_outline_async(test_prompt, 5)
        
        print(f"✅ Generated outline with {len(outline)} chapters")
        
        # Display outline
        print("\n📖 Generated Outline:")
        for chapter in outline:
            print(f"\n📄 Chapter {chapter['chapter_number']}: {chapter['title']}")
            print("-" * 40)
            print(chapter['prompt'])
            
        # Save outline
        os.makedirs("demo_output", exist_ok=True)
        with open("demo_output/outline.txt", "w") as f:
            for chapter in outline:
                f.write(f"\nChapter {chapter['chapter_number']}: {chapter['title']}\n")
                f.write("-" * 50 + "\n")
                f.write(chapter['prompt'] + "\n")
        
        print("\n💾 Outline saved to demo_output/outline.txt")
        return outline
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        logger.error(f"Demo outline generation failed: {e}")
        return None

async def demo_single_chapter_generation(outline):
    """Demo generating a single chapter"""
    if not outline:
        print("⚠️  Skipping chapter generation - no outline available")
        return
        
    print("\n🎯 Demo: Single Chapter Generation")
    print("=" * 50)
    
    # Setup logging
    logger = setup_logging("INFO", "logs/demo_chapter.log")
    
    # Configuration
    config = get_local_config()
    
    try:
        # Check system resources
        if not ResourceOptimizer.should_proceed_with_generation():
            print("⚠️  System resources insufficient for chapter generation")
            return
            
        # Create agents with outline context
        agents_manager = BookAgents(config, outline)
        agents = agents_manager.create_agents("Demo test", 5)
        
        # Initialize book generator
        book_gen = BookGenerator(agents, config, outline)
        book_gen.output_dir = "demo_output"
        
        # Generate just the first chapter
        performance_monitor.start_monitoring()
        
        with performance_monitor.monitor_chapter_generation(1):
            await book_gen.generate_chapter_async(1, outline[0]['prompt'])
            
        performance_monitor.stop_monitoring()
        
        # Check if chapter was created
        chapter_file = "demo_output/chapter_01.txt"
        if os.path.exists(chapter_file):
            print("✅ Chapter 1 generated successfully")
            
            # Show excerpt
            with open(chapter_file, 'r') as f:
                content = f.read()
                excerpt = content[:500] + "..." if len(content) > 500 else content
                print("\n📖 Chapter 1 Excerpt:")
                print("-" * 40)
                print(excerpt)
                
            print(f"\n💾 Full chapter saved to {chapter_file}")
        else:
            print("❌ Chapter generation failed - no output file created")
            
    except Exception as e:
        print(f"❌ Chapter generation failed: {e}")
        logger.error(f"Demo chapter generation failed: {e}")

async def demo_performance_monitoring():
    """Demo performance monitoring features"""
    print("\n🎯 Demo: Performance Monitoring")
    print("=" * 50)
    
    # Check system resources
    resources = ResourceOptimizer.check_system_resources()
    print(f"💻 System Resources:")
    print(f"   Available Memory: {resources['memory_available_gb']:.1f} GB")
    print(f"   Memory Usage: {resources['memory_percent_used']:.1f}%")
    print(f"   CPU Usage: {resources['cpu_percent']:.1f}%")
    print(f"   Disk Usage: {resources['disk_usage_percent']:.1f}%")
    
    # Performance metrics
    if performance_monitor.metrics['start_time']:
        metrics = performance_monitor.get_metrics_summary()
        print(f"\n📊 Generation Metrics:")
        print(f"   Chapters Completed: {metrics['chapters_completed']}")
        print(f"   Average Chapter Time: {metrics['average_chapter_time']:.2f}s")
        print(f"   Peak Memory Usage: {metrics['peak_memory_mb']:.1f} MB")
        print(f"   Average CPU Usage: {metrics['average_cpu_percent']:.1f}%")
        print(f"   Error Rate: {metrics['error_rate']:.2%}")

def demo_configuration():
    """Demo configuration options"""
    print("\n🎯 Demo: Configuration Options")
    print("=" * 50)
    
    try:
        # Test local configuration
        local_config = get_local_config(port=1234)
        print("✅ Local LLM configuration created")
        print(f"   Model: {local_config['model_client'].model}")
        print(f"   Base URL: localhost:1234")
        
        # Test OpenAI configuration (with dummy key)
        try:
            openai_config = get_openai_config("dummy-key", "gpt-4")
            print("✅ OpenAI configuration created")
            print(f"   Model: {openai_config['model_client'].model}")
        except Exception as e:
            print(f"⚠️  OpenAI config test skipped: {e}")
            
        print(f"\n🔧 Configuration Options:")
        print(f"   Temperature: {local_config['temperature']}")
        print(f"   Max Tokens: {local_config['max_tokens']}")
        print(f"   Timeout: {local_config['timeout']}s")
        
    except Exception as e:
        print(f"❌ Configuration demo failed: {e}")

async def full_demo():
    """Run the complete demo"""
    print("🚀 AI Book Generator v2.0 - Full Demo")
    print("=" * 60)
    
    # Check if we should use a real LLM or mock
    use_real_llm = input("\nDo you want to test with a real LLM? (y/n): ").lower().strip() == 'y'
    
    if not use_real_llm:
        print("\n⚠️  Demo will run in test mode (no real LLM calls)")
        print("   This demonstrates the framework without generating actual content")
    
    # Run demos
    demo_configuration()
    
    if use_real_llm:
        print("\n" + "="*60)
        outline = await demo_outline_generation()
        
        if outline:
            await demo_single_chapter_generation(outline)
            
        await demo_performance_monitoring()
    else:
        print("\n📋 Test Mode Complete - Framework is ready for real LLM integration")
    
    print("\n🎉 Demo completed!")
    print("\n📁 Check the following directories:")
    print("   📂 demo_output/ - Generated content")
    print("   📂 logs/ - Log files")
    print("   📂 book_output/ - Full book generation output")

if __name__ == "__main__":
    asyncio.run(full_demo())