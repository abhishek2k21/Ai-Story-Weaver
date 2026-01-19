"""
Agent integration tests for AI Story Weaver Pro.
Tests the agentic flywheel and inter-agent communication.
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.agents.architect import ArchitectAgent
from app.agents.scribe import ScribeAgent
from app.agents.editor import EditorAgent
from app.agents.causality import CausalityAgent
from app.agents.resonance import ResonanceAgent
from app.agents.tension import TensionAgent
from app.agents.weaving import WeavingAgent
from app.agents.vault import VaultAgent
from app.db.models import Story, User, Agent as AgentModel
from app.core.config import settings


class TestAgentIntegration:
    """Test agent integration and flywheel functionality."""

    @pytest.fixture
    def mock_llm(self):
        """Mock LLM for testing."""
        mock = AsyncMock()
        mock.ainvoke.return_value = Mock(content="Mock response")
        return mock

    @pytest.fixture
    def mock_embeddings(self):
        """Mock embeddings for testing."""
        mock = Mock()
        mock.embed_query.return_value = [0.1] * 384  # Mock embedding vector
        return mock

    @pytest.fixture
    def mock_vectorstore(self):
        """Mock vector store for testing."""
        mock = Mock()
        mock.similarity_search.return_value = []
        mock.add_texts.return_value = ["doc_id_1"]
        return mock

    @pytest.fixture
    def sample_story_request(self):
        """Sample story creation request."""
        return {
            "title": "The Lost Kingdom",
            "genre": "fantasy",
            "themes": ["redemption", "friendship"],
            "target_audience": "young_adult",
            "length_preference": "medium",
            "therapeutic_goals": ["anxiety_management", "self_esteem"],
            "user_preferences": {
                "tone": "hopeful",
                "pacing": "moderate",
                "character_types": ["hero", "mentor"]
            }
        }

    def test_architect_agent_initialization(self, mock_llm, mock_embeddings, mock_vectorstore):
        """Test Architect agent initialization."""
        with patch('app.agents.architect.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.architect.OpenAIEmbeddings', return_value=mock_embeddings), \
             patch('app.agents.architect.PineconeVectorStore', return_value=mock_vectorstore):

            agent = ArchitectAgent()
            assert agent.name == "Architect"
            assert agent.role == "Story Architect"
            assert hasattr(agent, 'llm')
            assert hasattr(agent, 'embeddings')
            assert hasattr(agent, 'vectorstore')

    def test_scribe_agent_initialization(self, mock_llm):
        """Test Scribe agent initialization."""
        with patch('app.agents.scribe.ChatOpenAI', return_value=mock_llm):
            agent = ScribeAgent()
            assert agent.name == "Scribe"
            assert agent.role == "Narrative Scribe"
            assert hasattr(agent, 'llm')

    def test_editor_agent_initialization(self, mock_llm):
        """Test Editor agent initialization."""
        with patch('app.agents.editor.ChatOpenAI', return_value=mock_llm):
            agent = EditorAgent()
            assert agent.name == "Editor"
            assert agent.role == "Story Editor"
            assert hasattr(agent, 'llm')

    def test_causality_agent_initialization(self, mock_llm):
        """Test Causality agent initialization."""
        with patch('app.agents.causality.ChatOpenAI', return_value=mock_llm):
            agent = CausalityAgent()
            assert agent.name == "Causality"
            assert agent.role == "Causal Logic Agent"
            assert hasattr(agent, 'llm')

    def test_resonance_agent_initialization(self, mock_llm, mock_embeddings, mock_vectorstore):
        """Test Resonance agent initialization."""
        with patch('app.agents.resonance.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.resonance.OpenAIEmbeddings', return_value=mock_embeddings), \
             patch('app.agents.resonance.PineconeVectorStore', return_value=mock_vectorstore):

            agent = ResonanceAgent()
            assert agent.name == "Resonance"
            assert agent.role == "Emotional Resonance Agent"
            assert hasattr(agent, 'llm')
            assert hasattr(agent, 'embeddings')
            assert hasattr(agent, 'vectorstore')

    def test_tension_agent_initialization(self, mock_llm):
        """Test Tension agent initialization."""
        with patch('app.agents.tension.ChatOpenAI', return_value=mock_llm):
            agent = TensionAgent()
            assert agent.name == "Tension"
            assert agent.role == "Dramatic Tension Agent"
            assert hasattr(agent, 'llm')

    def test_weaving_agent_initialization(self, mock_llm):
        """Test Weaving agent initialization."""
        with patch('app.agents.weaving.ChatOpenAI', return_value=mock_llm):
            agent = WeavingAgent()
            assert agent.name == "Weaving"
            assert agent.role == "Narrative Weaving Agent"
            assert hasattr(agent, 'llm')

    def test_vault_agent_initialization(self, mock_llm, mock_embeddings, mock_vectorstore):
        """Test Vault agent initialization."""
        with patch('app.agents.vault.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.vault.OpenAIEmbeddings', return_value=mock_embeddings), \
             patch('app.agents.vault.PineconeVectorStore', return_value=mock_vectorstore):

            agent = VaultAgent()
            assert agent.name == "Vault"
            assert agent.role == "Knowledge Vault Agent"
            assert hasattr(agent, 'llm')
            assert hasattr(agent, 'embeddings')
            assert hasattr(agent, 'vectorstore')

    @pytest.mark.asyncio
    async def test_architect_story_planning(self, mock_llm, mock_embeddings, mock_vectorstore, sample_story_request):
        """Test Architect agent story planning."""
        with patch('app.agents.architect.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.architect.OpenAIEmbeddings', return_value=mock_embeddings), \
             patch('app.agents.architect.PineconeVectorStore', return_value=mock_vectorstore):

            agent = ArchitectAgent()
            mock_llm.ainvoke.return_value = Mock(content="""
            {
                "structure": {
                    "acts": ["setup", "confrontation", "resolution"],
                    "scenes": ["introduction", "rising_action", "climax", "falling_action", "denouement"]
                },
                "characters": [
                    {"name": "Alex", "role": "protagonist", "arc": "growth"},
                    {"name": "Sage", "role": "mentor", "arc": "support"}
                ],
                "themes": ["redemption", "friendship"],
                "therapeutic_elements": ["anxiety_management", "self_esteem"]
            }
            """)

            result = await agent.plan_story(sample_story_request)

            assert "structure" in result
            assert "characters" in result
            assert "themes" in result
            assert "therapeutic_elements" in result

    @pytest.mark.asyncio
    async def test_scribe_content_generation(self, mock_llm):
        """Test Scribe agent content generation."""
        with patch('app.agents.scribe.ChatOpenAI', return_value=mock_llm):
            agent = ScribeAgent()
            mock_llm.ainvoke.return_value = Mock(content="""
            In the misty hills of Eldoria, young Alex discovered an ancient map...
            The journey would test courage, forge friendships, and reveal inner strength.
            """)

            story_plan = {
                "structure": {"acts": ["setup"]},
                "characters": [{"name": "Alex"}]
            }

            result = await agent.generate_content(story_plan, "introduction")

            assert isinstance(result, str)
            assert len(result) > 0
            assert "Alex" in result

    @pytest.mark.asyncio
    async def test_editor_content_refinement(self, mock_llm):
        """Test Editor agent content refinement."""
        with patch('app.agents.editor.ChatOpenAI', return_value=mock_llm):
            agent = EditorAgent()
            mock_llm.ainvoke.return_value = Mock(content="""
            Revised content with improved clarity and emotional depth.
            The narrative flows more smoothly and engages the reader effectively.
            """)

            raw_content = "Raw story content here..."
            feedback = {"clarity": "needs_improvement", "engagement": "good"}

            result = await agent.refine_content(raw_content, feedback)

            assert isinstance(result, str)
            assert len(result) > 0
            assert "Revised content" in result

    @pytest.mark.asyncio
    async def test_causality_logic_validation(self, mock_llm):
        """Test Causality agent logic validation."""
        with patch('app.agents.causality.ChatOpenAI', return_value=mock_llm):
            agent = CausalityAgent()
            mock_llm.ainvoke.return_value = Mock(content="""
            {
                "logical_consistency": "high",
                "causal_chains": ["event1 -> consequence1", "event2 -> consequence2"],
                "plot_holes": [],
                "recommendations": ["Strengthen motivation for character decision"]
            }
            """)

            story_content = "Story content with plot elements..."
            story_structure = {"acts": ["setup", "confrontation"]}

            result = await agent.validate_logic(story_content, story_structure)

            assert "logical_consistency" in result
            assert "causal_chains" in result
            assert "plot_holes" in result
            assert "recommendations" in result

    @pytest.mark.asyncio
    async def test_resonance_emotional_analysis(self, mock_llm, mock_embeddings, mock_vectorstore):
        """Test Resonance agent emotional analysis."""
        with patch('app.agents.resonance.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.resonance.OpenAIEmbeddings', return_value=mock_embeddings), \
             patch('app.agents.resonance.PineconeVectorStore', return_value=mock_vectorstore):

            agent = ResonanceAgent()
            mock_llm.ainvoke.return_value = Mock(content="""
            {
                "emotional_arc": ["hope", "doubt", "triumph"],
                "resonance_score": 8.5,
                "therapeutic_alignment": "strong",
                "emotional_triggers": ["loss", "redemption"],
                "recommendations": ["Amplify hope theme"]
            }
            """)

            content = "Emotional story content..."
            therapeutic_goals = ["anxiety_management"]

            result = await agent.analyze_emotional_resonance(content, therapeutic_goals)

            assert "emotional_arc" in result
            assert "resonance_score" in result
            assert "therapeutic_alignment" in result
            assert "emotional_triggers" in result

    @pytest.mark.asyncio
    async def test_tension_dramatic_building(self, mock_llm):
        """Test Tension agent dramatic tension building."""
        with patch('app.agents.tension.ChatOpenAI', return_value=mock_llm):
            agent = TensionAgent()
            mock_llm.ainvoke.return_value = Mock(content="""
            {
                "tension_curve": [0.2, 0.5, 0.8, 0.9, 0.3],
                "conflict_points": ["initial_challenge", "major_setback", "climax"],
                "pacing_suggestions": ["Build suspense gradually"],
                "engagement_score": 7.8
            }
            """)

            content = "Story content with conflicts..."
            story_structure = {"acts": ["setup", "confrontation", "resolution"]}

            result = await agent.build_tension(content, story_structure)

            assert "tension_curve" in result
            assert "conflict_points" in result
            assert "pacing_suggestions" in result
            assert "engagement_score" in result

    @pytest.mark.asyncio
    async def test_weaving_narrative_integration(self, mock_llm):
        """Test Weaving agent narrative integration."""
        with patch('app.agents.weaving.ChatOpenAI', return_value=mock_llm):
            agent = WeavingAgent()
            mock_llm.ainvoke.return_value = Mock(content="""
            {
                "integrated_narrative": "Seamlessly woven story content...",
                "thread_connections": ["character_arc", "theme_development"],
                "continuity_score": 9.2,
                "narrative_flow": "excellent"
            }
            """)

            scene_contents = ["Scene 1 content", "Scene 2 content"]
            story_structure = {"acts": ["setup", "development"]}

            result = await agent.weave_narrative(scene_contents, story_structure)

            assert "integrated_narrative" in result
            assert "thread_connections" in result
            assert "continuity_score" in result
            assert "narrative_flow" in result

    @pytest.mark.asyncio
    async def test_vault_knowledge_storage(self, mock_llm, mock_embeddings, mock_vectorstore):
        """Test Vault agent knowledge storage."""
        with patch('app.agents.vault.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.vault.OpenAIEmbeddings', return_value=mock_embeddings), \
             patch('app.agents.vault.PineconeVectorStore', return_value=mock_vectorstore):

            agent = VaultAgent()
            mock_llm.ainvoke.return_value = Mock(content="""
            {
                "stored_knowledge": ["character_trait", "plot_device", "theme_element"],
                "retrieval_keys": ["hero_journey", "redemption_arc"],
                "storage_score": 9.5,
                "accessibility": "high"
            }
            """)

            content = "Knowledge content to store..."
            metadata = {"type": "character_trait", "story_id": "123"}

            result = await agent.store_knowledge(content, metadata)

            assert "stored_knowledge" in result
            assert "retrieval_keys" in result
            assert "storage_score" in result
            assert "accessibility" in result

    @pytest.mark.asyncio
    async def test_agentic_flywheel_workflow(self, mock_llm, mock_embeddings, mock_vectorstore, sample_story_request):
        """Test complete agentic flywheel workflow."""
        # Mock all agents
        with patch('app.agents.architect.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.scribe.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.editor.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.causality.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.resonance.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.tension.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.weaving.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.vault.ChatOpenAI', return_value=mock_llm), \
             patch('app.agents.architect.OpenAIEmbeddings', return_value=mock_embeddings), \
             patch('app.agents.resonance.OpenAIEmbeddings', return_value=mock_embeddings), \
             patch('app.agents.vault.OpenAIEmbeddings', return_value=mock_embeddings), \
             patch('app.agents.architect.PineconeVectorStore', return_value=mock_vectorstore), \
             patch('app.agents.resonance.PineconeVectorStore', return_value=mock_vectorstore), \
             patch('app.agents.vault.PineconeVectorStore', return_value=mock_vectorstore):

            # Initialize agents
            architect = ArchitectAgent()
            scribe = ScribeAgent()
            editor = EditorAgent()
            causality = CausalityAgent()
            resonance = ResonanceAgent()
            tension = TensionAgent()
            weaving = WeavingAgent()
            vault = VaultAgent()

            # Mock responses for workflow
            mock_responses = {
                "architect": '{"structure": {"acts": ["setup"]}, "characters": [{"name": "Alex"}], "themes": ["redemption"]}',
                "scribe": "Generated story content with character development...",
                "editor": "Refined content with improved clarity...",
                "causality": '{"logical_consistency": "high", "plot_holes": []}',
                "resonance": '{"emotional_arc": ["hope"], "resonance_score": 8.5}',
                "tension": '{"tension_curve": [0.2, 0.8], "conflict_points": ["climax"]}',
                "weaving": '{"integrated_narrative": "Final woven story...", "continuity_score": 9.0}',
                "vault": '{"stored_knowledge": ["character_arc"], "storage_score": 9.5}'
            }

            call_count = 0
            def mock_ainvoke(*args, **kwargs):
                nonlocal call_count
                call_count += 1
                response = list(mock_responses.values())[call_count - 1] if call_count <= len(mock_responses) else "Mock response"
                return Mock(content=response)

            mock_llm.ainvoke.side_effect = mock_ainvoke

            # Execute flywheel workflow
            # 1. Architect plans the story
            plan = await architect.plan_story(sample_story_request)
            assert "structure" in plan

            # 2. Scribe generates initial content
            content = await scribe.generate_content(plan, "introduction")
            assert isinstance(content, str)

            # 3. Editor refines content
            refined = await editor.refine_content(content, {})
            assert isinstance(refined, str)

            # 4. Causality validates logic
            logic_check = await causality.validate_logic(refined, plan["structure"])
            assert "logical_consistency" in logic_check

            # 5. Resonance analyzes emotions
            emotional = await resonance.analyze_emotional_resonance(refined, sample_story_request["therapeutic_goals"])
            assert "emotional_arc" in emotional

            # 6. Tension builds drama
            dramatic = await tension.build_tension(refined, plan["structure"])
            assert "tension_curve" in dramatic

            # 7. Weaving integrates narrative
            final_story = await weaving.weave_narrative([refined], plan["structure"])
            assert "integrated_narrative" in final_story

            # 8. Vault stores knowledge
            stored = await vault.store_knowledge(final_story["integrated_narrative"], {"story_id": "test"})
            assert "stored_knowledge" in stored

            # Verify all agents were called
            assert mock_llm.ainvoke.call_count >= 8