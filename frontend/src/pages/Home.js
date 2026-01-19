import React, { useState } from 'react';
import './Home.css';

function Home() {
  const [storyPrompt, setStoryPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedStory, setGeneratedStory] = useState('');

  const handleGenerateStory = async () => {
    if (!storyPrompt.trim()) return;

    setIsGenerating(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/stories/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: storyPrompt,
          therapeutic_focus: 'general_wellbeing'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setGeneratedStory(data.content);
      } else {
        const errorData = await response.json().catch(() => ({}));
        console.error('Failed to generate story:', errorData);
        setGeneratedStory(`Error: ${errorData.detail || 'Failed to generate story'}. Please check the console for details.`);
      }
    } catch (error) {
      console.error('Error generating story:', error);
      setGeneratedStory('Error: Could not connect to the server. Please make sure the backend is running.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="home">
      <div className="hero-section">
        <h1>AI Story Weaver Pro</h1>
        <p>Create therapeutic stories powered by advanced AI agents</p>
      </div>

      <div className="story-generator">
        <div className="input-section">
          <label htmlFor="story-prompt">What kind of story would you like to create?</label>
          <textarea
            id="story-prompt"
            value={storyPrompt}
            onChange={(e) => setStoryPrompt(e.target.value)}
            placeholder="Describe your story idea, theme, or therapeutic goal..."
            rows={4}
          />
          <button
            onClick={handleGenerateStory}
            disabled={isGenerating || !storyPrompt.trim()}
            className="generate-btn"
          >
            {isGenerating ? 'Weaving Story...' : 'Weave Story'}
          </button>
        </div>

        {generatedStory && (
          <div className="story-output">
            <h3>Your Story:</h3>
            <div className="story-content">
              {generatedStory}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;