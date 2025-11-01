'use client';

import { useEffect, useRef, useState } from 'react';
import styles from './page.module.css';
import Mascot from '../components/ui/mascot';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Input } from '../components/ui/input';

export default function Page() {
  const [messages, setMessages] = useState([
    { sender: 'system', text: "Hallo, wie geht's dir heute?" }
  ]);
  const [input, setInput] = useState('');
  const [currentMood, setCurrentMood] = useState('neutral');
  const [moodConfidence, setMoodConfidence] = useState(0.0);
  const [isLoading, setIsLoading] = useState(false);
  const endRef = useRef(null);

  const moodEmojis = {
    'gut': '🙂',
    'schlecht': '😞',
    'neutral': '😐'
  };

  const moodColors = {
    'gut': '#22c55e',
    'schlecht': '#ef4444',
    'neutral': '#6b7280'
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    const userMessage = input.trim();
    setMessages((prev) => [...prev, { sender: 'user', text: userMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      setCurrentMood(data.sentiment);
      setMoodConfidence(data.confidence);
      
      setMessages((prev) => [...prev, { 
        sender: 'system', 
        text: data.response 
      }]);
      
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) => [...prev, { 
        sender: 'system', 
        text: 'Entschuldigung, etwas ist schiefgelaufen. Versuche es nochmal.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <header className={styles.header}>
          <div className={styles.mascotBlock}>
            <Mascot className={styles.mascot} />
            <span className={styles.mascotGlow} />
          </div>
          <div className={styles.brandText}>
            <h1 className={styles.title}>MindMate</h1>
            <p className={styles.subtitle}>Dein KI Kumpel</p>
          </div>
        </header>

        <Card className={`${styles.card} ${styles.chatCard}`}>
          <CardContent className={styles.chatContent}>
            <div className={styles.chatMessages}>
              {messages.map((m, i) => (
                <div
                  key={i}
                  className={m.sender === 'system' ? styles.systemMsg : styles.userMsg}
                >
                  {m.text}
                </div>
              ))}
              {isLoading && (
                <div className={styles.systemMsg}>
                  <span className={styles.typing}>MindMate schreibt...</span>
                </div>
              )}
              <div ref={endRef} />
            </div>

            <form className={styles.inputRow} onSubmit={handleSubmit}>
              <Input
                className={styles.input}
                placeholder="Antwort hier eingeben..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={isLoading}
                autoComplete="off"
                autoCorrect="off"
                autoCapitalize="off"
                spellCheck="false"
              />
              <Button 
                type="submit" 
                className={styles.sendBtn} 
                disabled={isLoading || !input.trim()}
              >
                {isLoading ? '...' : 'Senden'}
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card className={`${styles.card} ${styles.moodCard}`}>
          <CardContent>
            <div className={styles.moodSection}>
              <p className={styles.moodLabel}>
                Deine Stimmung: {currentMood} 
                {moodConfidence > 0 && (
                  <span className={styles.confidence}>
                    ({Math.round(moodConfidence * 100)}% sicher)
                  </span>
                )}
              </p>
              <div className={styles.moodRow}>
                <span className={styles.emojiBadge}>
                  {moodEmojis[currentMood]}
                </span>
                <div className={styles.sliderTrack}>
                  <span 
                    className={styles.sliderFill}
                    style={{ 
                      width: `${Math.max(moodConfidence * 100, 10)}%`,
                      backgroundColor: moodColors[currentMood]
                    }}
                  />
                </div>
              </div>
            </div>
            <Button className={styles.ctaBtn} variant="outline">
              Generate Spotify Playlist
            </Button>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}