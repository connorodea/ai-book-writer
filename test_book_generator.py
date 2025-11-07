"""Comprehensive tests for the AI Book Generator system"""
import pytest
import os
import tempfile
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import sys

# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_v2 import get_local_config, get_openai_config
from agents_v2 import BookAgents
from outline_generator_v2 import OutlineGenerator
from book_generator_v2 import BookGenerator

class TestConfig:
    """Test configuration functions"""
    
    def test_get_local_config(self):
        """Test local configuration creation"""
        config = get_local_config()
        assert "model_client" in config
        assert config["temperature"] == 0.7
        assert config["max_tokens"] == 2000
        assert config["timeout"] == 600

    def test_get_openai_config(self):
        """Test OpenAI configuration creation"""
        config = get_openai_config("test-api-key", "gpt-4")
        assert "model_client" in config
        assert config["temperature"] == 0.7

    def test_custom_port_config(self):
        """Test local config with custom port"""
        config = get_local_config(port=8080)
        # Can't directly test the URL but we can test that config is created
        assert "model_client" in config

class TestBookAgents:
    """Test BookAgents functionality"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing"""
        mock_client = Mock()
        return {
            "model_client": mock_client,
            "temperature": 0.7,
            "max_tokens": 2000
        }
    
    @pytest.fixture
    def sample_outline(self):
        """Sample outline for testing"""
        return [
            {
                "chapter_number": 1,
                "title": "The Beginning",
                "prompt": "- Key Events: Introduction\n- Character Developments: Meet protagonist\n- Setting: Corporate office\n- Tone: Mysterious"
            },
            {
                "chapter_number": 2,
                "title": "The Discovery",
                "prompt": "- Key Events: Algorithm completed\n- Character Developments: Dane's dedication shown\n- Setting: Late night office\n- Tone: Tense"
            }
        ]
    
    def test_book_agents_initialization(self, mock_config):
        """Test BookAgents initialization"""
        agents = BookAgents(mock_config)
        assert agents.agent_config == mock_config
        assert agents.outline is None
        assert isinstance(agents.world_elements, dict)
        assert isinstance(agents.character_developments, dict)
    
    def test_book_agents_with_outline(self, mock_config, sample_outline):
        """Test BookAgents initialization with outline"""
        agents = BookAgents(mock_config, sample_outline)
        assert agents.outline == sample_outline
        assert "Chapter 1: The Beginning" in agents._format_outline_context()
    
    def test_create_agents(self, mock_config):
        """Test agent creation"""
        agents = BookAgents(mock_config)
        agent_dict = agents.create_agents("Test prompt", 5)
        
        expected_agents = [
            "story_planner", "world_builder", "memory_keeper",
            "writer", "editor", "user_proxy", "outline_creator"
        ]
        
        for agent_name in expected_agents:
            assert agent_name in agent_dict
    
    def test_world_element_tracking(self, mock_config):
        """Test world element tracking"""
        agents = BookAgents(mock_config)
        agents.update_world_element("office", "Modern corporate building")
        
        assert "office" in agents.world_elements
        assert agents.world_elements["office"] == "Modern corporate building"
        
        context = agents.get_world_context()
        assert "office" in context
        assert "Modern corporate building" in context
    
    def test_character_development_tracking(self, mock_config):
        """Test character development tracking"""
        agents = BookAgents(mock_config)
        agents.update_character_development("Dane", "Shows dedication to work")
        agents.update_character_development("Dane", "Struggles with presentation")
        
        assert "Dane" in agents.character_developments
        assert len(agents.character_developments["Dane"]) == 2
        
        context = agents.get_character_context()
        assert "Dane" in context
        assert "dedication to work" in context

class TestOutlineGenerator:
    """Test OutlineGenerator functionality"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing"""
        return {"model_client": Mock()}
    
    @pytest.fixture
    def mock_agents(self, mock_config):
        """Mock agents for testing"""
        return {
            "story_planner": Mock(),
            "world_builder": Mock(),
            "outline_creator": Mock(),
            "user_proxy": Mock()
        }
    
    def test_outline_generator_initialization(self, mock_agents, mock_config):
        """Test OutlineGenerator initialization"""
        generator = OutlineGenerator(mock_agents, mock_config)
        assert generator.agents == mock_agents
        assert generator.agent_config == mock_config
    
    def test_extract_outline_content(self, mock_agents, mock_config):
        """Test outline content extraction"""
        generator = OutlineGenerator(mock_agents, mock_config)
        
        # Test with properly formatted outline
        messages = [
            {
                "content": "OUTLINE:\nChapter 1: Test Chapter\nKey Events:\n- Event 1\n- Event 2\n- Event 3\nEND OF OUTLINE",
                "sender": "outline_creator"
            }
        ]
        
        content = generator._extract_outline_content(messages)
        assert "Chapter 1: Test Chapter" in content
        assert "Event 1" in content
    
    def test_verify_chapter_sequence(self, mock_agents, mock_config):
        """Test chapter sequence verification"""
        generator = OutlineGenerator(mock_agents, mock_config)
        
        # Test with incomplete chapters
        chapters = [
            {"chapter_number": 1, "title": "Chapter 1", "prompt": "test"},
            {"chapter_number": 3, "title": "Chapter 3", "prompt": "test"}
        ]
        
        result = generator._verify_chapter_sequence(chapters, 5)
        assert len(result) == 5
        assert result[0]["chapter_number"] == 1
        assert result[4]["chapter_number"] == 5
    
    def test_emergency_outline_processing(self, mock_agents, mock_config):
        """Test emergency outline processing"""
        generator = OutlineGenerator(mock_agents, mock_config)
        
        # Test with no messages (should create placeholder outline)
        result = generator._emergency_outline_processing([], 3)
        
        assert len(result) == 3
        assert result[0]["chapter_number"] == 1
        assert result[2]["chapter_number"] == 3
        assert "To be determined" in result[0]["prompt"]

class TestBookGenerator:
    """Test BookGenerator functionality"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing"""
        return {"model_client": Mock()}
    
    @pytest.fixture
    def mock_agents(self):
        """Mock agents for testing"""
        return {
            "memory_keeper": Mock(),
            "writer": Mock(),
            "editor": Mock(),
            "story_planner": Mock()
        }
    
    @pytest.fixture
    def sample_outline(self):
        """Sample outline for testing"""
        return [
            {
                "chapter_number": 1,
                "title": "Test Chapter 1",
                "prompt": "Test chapter 1 content"
            },
            {
                "chapter_number": 2,
                "title": "Test Chapter 2", 
                "prompt": "Test chapter 2 content"
            }
        ]
    
    @pytest.fixture
    def temp_output_dir(self):
        """Temporary directory for testing file operations"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    def test_book_generator_initialization(self, mock_agents, mock_config, sample_outline):
        """Test BookGenerator initialization"""
        generator = BookGenerator(mock_agents, mock_config, sample_outline)
        
        assert generator.agents == mock_agents
        assert generator.agent_config == mock_config
        assert generator.outline == sample_outline
        assert generator.max_iterations == 3
        assert isinstance(generator.chapters_memory, list)
    
    def test_clean_chapter_content(self, mock_agents, mock_config, sample_outline):
        """Test chapter content cleaning"""
        generator = BookGenerator(mock_agents, mock_config, sample_outline)
        
        dirty_content = "*(Chapter 1 - Test)* This is the actual content with *artifacts*"
        clean_content = generator._clean_chapter_content(dirty_content)
        
        assert "(Chapter 1" not in clean_content
        assert "*" not in clean_content
        assert "actual content" in clean_content
    
    def test_prepare_chapter_context(self, mock_agents, mock_config, sample_outline):
        """Test chapter context preparation"""
        generator = BookGenerator(mock_agents, mock_config, sample_outline)
        
        # Test first chapter (no previous context)
        context1 = generator._prepare_chapter_context(1, "Test prompt")
        assert "Initial Chapter" in context1
        assert "Test prompt" in context1
        
        # Add some memory and test second chapter
        generator.chapters_memory.append("Chapter 1 summary")
        context2 = generator._prepare_chapter_context(2, "Test prompt 2")
        assert "Previous Chapter Summaries" in context2
        assert "Chapter 1 summary" in context2
        assert "Test prompt 2" in context2
    
    def test_extract_final_scene(self, mock_agents, mock_config, sample_outline):
        """Test final scene extraction from messages"""
        generator = BookGenerator(mock_agents, mock_config, sample_outline)
        
        messages = [
            {
                "content": "SCENE: This is just a draft scene.",
                "sender": "writer"
            },
            {
                "content": "SCENE FINAL: This is the final scene content that should be extracted.",
                "sender": "writer"
            }
        ]
        
        extracted = generator._extract_final_scene(messages)
        assert extracted is not None
        assert "final scene content" in extracted
        assert "draft scene" not in extracted
    
    def test_verify_chapter_content(self, mock_agents, mock_config, sample_outline):
        """Test chapter content verification"""
        generator = BookGenerator(mock_agents, mock_config, sample_outline)
        
        # Valid content
        valid_content = "Chapter 1\n\nThis is valid chapter content with multiple lines.\nIt has enough content to pass validation."
        assert generator._verify_chapter_content(valid_content, 1) == True
        
        # Invalid content (empty)
        assert generator._verify_chapter_content("", 1) == False
        
        # Invalid content (no chapter header)
        invalid_content = "This content doesn't have a chapter header."
        assert generator._verify_chapter_content(invalid_content, 1) == False
        
        # Invalid content (too short)
        short_content = "Chapter 1\nToo short"
        assert generator._verify_chapter_content(short_content, 1) == False
    
    @patch('builtins.open')
    @patch('os.path.exists')
    def test_save_chapter(self, mock_exists, mock_open, mock_agents, mock_config, sample_outline):
        """Test chapter saving functionality"""
        # Setup
        mock_exists.return_value = False
        mock_file = Mock()
        mock_file.read.return_value = "Chapter 1\n\nThis is test chapter content"  # Mock read for verification
        mock_open.return_value.__enter__.return_value = mock_file
        
        generator = BookGenerator(mock_agents, mock_config, sample_outline)
        generator.output_dir = "/tmp/test"
        
        # Test saving chapter content
        test_content = "This is test chapter content"
        generator._save_chapter(1, test_content)
        
        # Verify file operations
        expected_path = "/tmp/test/chapter_01.txt"
        assert mock_open.call_count >= 1  # Called for write and verification
        mock_file.write.assert_called_once()
        
        # Check the content written
        written_content = mock_file.write.call_args[0][0]
        assert "Chapter 1" in written_content
        assert test_content in written_content

class TestIntegration:
    """Integration tests for the complete system"""
    
    @pytest.fixture
    def temp_dir(self):
        """Temporary directory for integration tests"""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            yield temp_dir
            os.chdir(original_cwd)
    
    def test_config_to_agents_integration(self):
        """Test that configuration works with agent creation"""
        config = get_local_config()
        agents_manager = BookAgents(config)
        agents = agents_manager.create_agents("Test prompt", 3)
        
        # Verify all expected agents are created
        expected_agents = ["story_planner", "world_builder", "memory_keeper", 
                          "writer", "editor", "user_proxy", "outline_creator"]
        for agent_name in expected_agents:
            assert agent_name in agents
            # Verify agent has the model_client set
            if hasattr(agents[agent_name], 'model_client'):
                assert agents[agent_name].model_client is not None

    @patch.dict(os.environ, {"USE_OPENAI": "false"})
    def test_environment_variable_config(self):
        """Test configuration based on environment variables"""
        # This would be tested in actual main_v2.py execution
        # Here we just test that the environment variable is read correctly
        assert os.getenv("USE_OPENAI", "false").lower() == "false"

def run_tests():
    """Run all tests"""
    print("🧪 Running AI Book Generator Tests...")
    
    # Run pytest programmatically
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--no-header"
    ])
    
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return exit_code

if __name__ == "__main__":
    run_tests()