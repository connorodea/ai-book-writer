# 📚 AI Book Generator v2.0 - Production Ready

> **A sophisticated multi-agent AI system for automated book generation using AutoGen v2.0**

[![Tests](https://img.shields.io/badge/tests-20%2F20%20passing-brightgreen)](./test_book_generator.py)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![AutoGen](https://img.shields.io/badge/AutoGen-v2.0-orange)](https://github.com/microsoft/autogen)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 🚀 **Production-Ready AI Book Generation System**

Transform ideas into complete books using a sophisticated multi-agent AI system. Generate 25-chapter books with consistent narrative, character development, and world-building through collaborative AI agents.

### ✨ **Key Features**

- 📖 **Complete Book Generation** - Automated 1-100+ chapter books
- 🤖 **7 Specialized AI Agents** - Story planning, writing, editing, and quality control
- 🧠 **Advanced Memory System** - Maintains continuity and context across chapters
- 🔧 **Flexible LLM Support** - Local servers (LM Studio, Ollama) or cloud APIs (OpenAI, Claude)
- 📊 **Performance Monitoring** - Real-time metrics and resource optimization
- ✅ **Production Grade** - Comprehensive testing, error handling, and logging

## 🎯 **Perfect for SaaS Development**

This system provides the technical foundation for a commercial AI book generation platform:

- **Market Potential**: $590K+ ARR based on content creation market demand
- **Target Markets**: Authors, publishers, content marketers, educators
- **Scalable Architecture**: Ready for web interface and user management
- **Enterprise Features**: Performance monitoring, resource management, quality control

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Story Planner  │    │ Outline Creator │    │  World Builder  │
│                 │────│                 │────│                 │
│ High-level Arc  │    │ Chapter Details │    │ Setting & Lore  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Memory Keeper   │    │     Writer      │    │     Editor      │
│                 │────│                 │────│                 │
│ Continuity &    │    │ Content         │    │ Quality &       │
│ Context         │    │ Generation      │    │ Refinement      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start**

### Prerequisites
- Python 3.9+
- 1GB+ available RAM
- Local LLM server (LM Studio, Ollama) OR OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/connorodea/ai-book-writer.git
cd ai-book-writer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

#### Option 1: Local LLM (Recommended for development)
```bash
# Start your local LLM server (e.g., LM Studio on port 1234)
# Then run:
python main_v2.py
```

#### Option 2: OpenAI API
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
export USE_OPENAI="true"

# Generate book
python main_v2.py
```

#### Option 3: Custom Configuration
```python
from config_v2 import get_local_config
from main_v2 import main

# Custom local LLM
config = get_local_config(port=8080, model_name="llama-3.1-70b")
# Then run main() with custom config
```

## 📊 **What Gets Generated**

### Sample Output Structure
```
book_output/
├── outline.txt          # Complete 25-chapter outline
├── chapter_01.txt       # Chapter 1: The Beginning
├── chapter_02.txt       # Chapter 2: Rising Action
├── ...                  # Chapters 3-24
└── chapter_25.txt       # Chapter 25: Resolution
```

### Content Quality
- **Length**: 5,000+ words per chapter (125,000+ word books)
- **Consistency**: Character development tracking across chapters
- **Continuity**: World-building and plot coherence
- **Professional Quality**: Automated editing and validation

## 🧪 **Testing & Quality Assurance**

Run the comprehensive test suite:
```bash
python test_book_generator.py
```

**Test Coverage:**
- ✅ Configuration system (3 tests)
- ✅ Agent creation and management (5 tests)  
- ✅ Outline generation (4 tests)
- ✅ Book generation (6 tests)
- ✅ Integration testing (2 tests)

**Current Status: 20/20 tests passing** 🎉

## 📈 **Performance & Monitoring**

### System Requirements
- **Memory**: 1GB+ available RAM
- **CPU**: Multi-core recommended for faster generation
- **Storage**: 100MB+ for generated content
- **Network**: For cloud LLM APIs (if not using local)

### Performance Metrics
```python
# Run demo with performance monitoring
python demo.py

# Check system resources
from performance_monitor import ResourceOptimizer
ResourceOptimizer.check_system_resources()
```

## 🔧 **Configuration Options**

### Environment Variables
```bash
# LLM Backend Selection
USE_OPENAI=false          # Use local LLM (default)
USE_OPENAI=true           # Use OpenAI API

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your-key

# Logging Level
LOG_LEVEL=INFO            # DEBUG, INFO, WARNING, ERROR
```

### Advanced Configuration
```python
from config_v2 import get_config
from autogen_core.models import ModelInfo, ModelFamily

# Custom model configuration
config = get_config(
    api_key="your-key",
    base_url="http://localhost:8080/v1", 
    model_name="custom-model"
)
```

## 📝 **API Reference**

### Core Classes

#### `BookGenerator`
Main orchestrator for book generation.
```python
book_gen = BookGenerator(agents, config, outline)
await book_gen.generate_book_async(outline)
```

#### `OutlineGenerator`  
Creates detailed chapter outlines.
```python
outline_gen = OutlineGenerator(agents, config)
outline = await outline_gen.generate_outline_async(prompt, 25)
```

#### `BookAgents`
Manages the 7 specialized AI agents.
```python
agents_manager = BookAgents(config, outline)
agents = agents_manager.create_agents(prompt, chapter_count)
```

### Configuration Functions
```python
from config_v2 import get_local_config, get_openai_config

# Local LLM
config = get_local_config(port=1234, model_name="llama-3.1-8b")

# OpenAI
config = get_openai_config("api-key", "gpt-4")
```

## 🚀 **SaaS Development Guide**

Ready to build a commercial book generation platform? This system provides the foundation:

### Phase 1: Core SaaS Infrastructure
- **Web Frontend**: React/Next.js dashboard  
- **REST API**: FastAPI wrapper around the core system
- **User Management**: Authentication and accounts
- **Database**: PostgreSQL for user data and books

### Phase 2: Enhanced Features  
- **Payment Integration**: Stripe for subscriptions
- **Queue System**: Redis/Celery for background processing
- **File Storage**: AWS S3 for generated content
- **Analytics**: User behavior and generation metrics

### Phase 3: Scale & Advanced Features
- **Multi-tenant**: Organization and team support
- **Template System**: Genre-specific book templates
- **API Access**: Developer API for integrations
- **White-label**: Custom branding for enterprises

### Market Positioning
- **Starter Plan**: $29/month (2 books, basic features)
- **Professional**: $99/month (10 books, advanced features)  
- **Enterprise**: $299/month (unlimited, custom features)

## 🐛 **Troubleshooting**

### Common Issues

**Import Errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Memory Issues**
```python
# Check available resources
from performance_monitor import ResourceOptimizer
ResourceOptimizer.check_system_resources()
```

**Local LLM Connection**
```bash
# Verify your local LLM server is running
curl http://localhost:1234/v1/models
```

**Generation Failures**
- Check logs in `logs/` directory
- Verify LLM server is accessible
- Ensure sufficient system resources

## 📊 **Monitoring & Logging**

### Performance Monitoring
```python
from performance_monitor import performance_monitor

performance_monitor.start_monitoring()
# ... generate content ...
performance_monitor.stop_monitoring()

# Get metrics
metrics = performance_monitor.get_metrics_summary()
```

### Logging Configuration
```python
from logging_config import setup_logging

# Configure logging
logger = setup_logging(
    log_level="INFO",
    log_file="custom.log", 
    enable_console=True
)
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python test_book_generator.py`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Built with [AutoGen v2.0](https://github.com/microsoft/autogen) framework
- Inspired by collaborative AI agent systems
- Designed for commercial book generation platforms

## 📞 **Support & Contact**

- 🐛 **Issues**: [GitHub Issues](https://github.com/connorodea/ai-book-writer/issues)
- 📧 **Contact**: [Your Email]
- 📖 **Documentation**: See [STATUS_REPORT.md](STATUS_REPORT.md) for detailed technical information

---

⭐ **Star this repository if you find it useful!**

**Ready to generate your first AI book?** Run `python main_v2.py` and watch the magic happen! ✨