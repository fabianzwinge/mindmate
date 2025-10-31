'use client';

import { useEffect, useRef, useState } from 'react';
import styles from './page.module.css';

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

        <section className={`${styles.card} ${styles.chatCard}`}>
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
            <input
              className={styles.input}
              placeholder="Antwort hier eingeben..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button type="submit" className={styles.sendBtn}>Senden</button>
          </form>
        </section>

        <section className={`${styles.card} ${styles.moodCard}`}>
          <div className={styles.moodRow}>
            <span className={styles.emojiBadge}>🙂</span>
            <div className={styles.sliderTrack}><span className={styles.sliderFill} /></div>
          </div>
          <button className={styles.ctaBtn}>Generate Spotify Playlist</button>
        </section>
      </div>
    </main>
  );
}

function Mascot({ className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 180 180"
      role="img"
      aria-label="MindMate Mascot"
    >
      <defs>
        <radialGradient id="g1" cx="50%" cy="35%" r="70%">
          <stop offset="0%" stopColor="#BFD4FF" />
          <stop offset="60%" stopColor="#4C83FF" />
          <stop offset="100%" stopColor="#1E60FF" />
        </radialGradient>
      </defs>

      <circle cx="90" cy="105" r="50" fill="url(#g1)" />

      <circle cx="90" cy="65" r="42" fill="url(#g1)" />

      <rect
        x="85"
        y="18"
        width="10"
        height="20"
        rx="5"
        fill="url(#g1)"
      />
      <circle
        cx="90"
        cy="14"
        r="9"
        fill="url(#g1)"
      />

      <circle cx="75" cy="65" r="6" fill="#0F172A" />
      <circle cx="105" cy="65" r="6" fill="#0F172A" />
      <path
        d="M72 78c6 8 30 8 36 0"
        stroke="#0F172A"
        strokeWidth="4"
        strokeLinecap="round"
      />
    </svg>
  );
}

