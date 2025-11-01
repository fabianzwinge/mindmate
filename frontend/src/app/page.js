'use client';

import { useEffect, useRef, useState } from 'react';
import styles from './page.module.css';
import Mascot from '../components/Mascot';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Input } from '../components/ui/input';

export default function Page() {
  const [messages, setMessages] = useState([
    { sender: 'system', text: 'Hallo, wie geht’s dir heute?' }
  ]);
  const [input, setInput] = useState('');
  const endRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { sender: 'user', text: input.trim() }]);
    setInput('');
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
              <div ref={endRef} />
            </div>

            <form className={styles.inputRow} onSubmit={handleSubmit}>
              <Input
                className={styles.input}
                placeholder="Antwort hier eingeben..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />
              <Button type="submit" className={styles.sendBtn}>
                Senden
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card className={`${styles.card} ${styles.moodCard}`}>
          <CardContent>
            <div className={styles.moodSection}>
              <p className={styles.moodLabel}>Deine Stimmung: gut</p>
              <div className={styles.moodRow}>
                <span className={styles.emojiBadge}>🙂</span>
                <div className={styles.sliderTrack}><span className={styles.sliderFill} /></div>
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

