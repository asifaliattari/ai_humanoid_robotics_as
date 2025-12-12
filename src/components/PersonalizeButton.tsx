/**
 * PersonalizeButton Component
 *
 * Adapts content based on user's hardware, experience, and preferences
 * Shows alternative instructions for different setups (cloud GPU, Jetson, etc.)
 */
import React, { useState } from 'react';
import { API_ENDPOINTS } from '../config/api';
import './PersonalizeButton.css';

interface PersonalizeButtonProps {
  sectionId: string;
  userId: string | null;
  onPersonalize: (adaptedContent: string, adaptations: any[]) => void;
  onReset: () => void;
}

export const PersonalizeButton: React.FC<PersonalizeButtonProps> = ({
  sectionId,
  userId,
  onPersonalize,
  onReset,
}) => {
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [adaptationSummary, setAdaptationSummary] = useState<string[]>([]);

  const handlePersonalize = async () => {
    if (!userId) {
      setError('Please sign in to personalize content');
      return;
    }

    if (isPersonalized) {
      // Reset to original
      setIsPersonalized(false);
      setAdaptationSummary([]);
      onReset();
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Call personalization API
      const response = await fetch(API_ENDPOINTS.adaptContent, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          section_id: sectionId,
          user_id: userId,
        }),
      });

      if (!response.ok) {
        throw new Error('Personalization failed');
      }

      const data = await response.json();

      // Extract adaptation reasons
      const reasons = data.adaptations.map((a: any) => a.reason);
      setAdaptationSummary(reasons);

      // Update UI with personalized content
      setIsPersonalized(true);
      onPersonalize(data.adapted_content, data.adaptations);

      console.log(
        `Applied ${data.adaptations.length} adaptations: ${reasons.join(', ')}`
      );
    } catch (err) {
      setError('Personalization failed. Please try again.');
      console.error('Personalization error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="personalize-button-container">
      <button
        onClick={handlePersonalize}
        disabled={isLoading}
        className={`personalize-button ${isPersonalized ? 'active' : ''} ${
          isLoading ? 'disabled' : ''
        }`}
        title={
          isPersonalized
            ? 'Reset to original content'
            : 'Adapt content for your setup'
        }
      >
        <span className="icon">{isPersonalized ? '✓' : '⚙️'}</span>
        <span className="label">
          {isPersonalized ? 'Personalized' : 'Personalize for Me'}
        </span>
      </button>

      {isLoading && (
        <div className="personalize-loading">
          <span className="spinner">⏳</span> Analyzing your profile...
        </div>
      )}

      {error && <div className="personalize-error">⚠️ {error}</div>}

      {isPersonalized && adaptationSummary.length > 0 && (
        <div className="personalize-summary">
          <div className="summary-header">
            <strong>📝 Adaptations Applied:</strong>
          </div>
          <ul className="summary-list">
            {adaptationSummary.map((reason, index) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
          <div className="summary-hint">
            Content has been customized based on your hardware and experience.
          </div>
        </div>
      )}
    </div>
  );
};

export default PersonalizeButton;
 