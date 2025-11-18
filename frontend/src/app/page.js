'use client';

import { useEffect, useRef, useState } from 'react';
import styles from './page.module.css';
import Mascot from '../components/ui/mascot';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { toast } from 'sonner';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export default function Page() {
  const [messages, setMessages] = useState([
    { sender: 'system', text: "Hi there! How are you feeling today? What have you been up to?" }
  ]);
  const [input, setInput] = useState('');
  const [currentMood, setCurrentMood] = useState('neutral');
  const [moodConfidence, setMoodConfidence] = useState(0.0);
  const [isLoading, setIsLoading] = useState(false);
  const [isGeneratingPlaylist, setIsGeneratingPlaylist] = useState(false);
  const [lastPlaylist, setLastPlaylist] = useState(null);
  const endRef = useRef(null);

  const moodEmojis = {
    'good': '🙂',
    'bad': '😞',
    'neutral': '😐'
  };

  const moodColors = {
    'good': '#22c55e',
    'bad': '#ef4444',
    'neutral': '#6b7280'
  };

  useEffect(() => {
   
    const checkPopupClosed = (popup) => {
      const timer = setInterval(() => {
        if (popup.closed) {
          clearInterval(timer);
          
          setTimeout(() => {
            setIsGeneratingPlaylist(true);
            handleGeneratePlaylistAfterAuth();
          }, 1500);
        }
      }, 1000);
    };
  
    window.checkPopupClosed = checkPopupClosed;
    
    const urlParams = new URLSearchParams(window.location.search);
    
    if (window.opener) {
      setTimeout(() => {
        window.close();
      }, 500);
      return;
    }
  
    if (urlParams.get('playlist_created') === 'true') {
      const playlistName = urlParams.get('playlist_name');
      const tracksAdded = urlParams.get('tracks_added');
      const playlistUrl = urlParams.get('playlist_url');
      
      console.log('Playlist created successfully:', playlistName);
      toast.success(`Playlist "${playlistName}" was successfully created`);
      
      setLastPlaylist({
        playlist_name: playlistName,
        playlist_url: playlistUrl,
        tracks_added: parseInt(tracksAdded)
      });
      
      setIsGeneratingPlaylist(false);
      
    } else if (urlParams.get('playlist_error') === 'true') {
      const errorMessage = urlParams.get('error_message') || 'Unknown error';
      console.log('Error creating playlist:', errorMessage);
      toast.error(`Error creating playlist: ${errorMessage}`);
      setIsGeneratingPlaylist(false);

        } else if (urlParams.get('spotify_auth') === 'success') {
      console.log('Spotify authentication successful');
      toast.success('Spotify authentication successful');

        } else if (urlParams.get('spotify_auth') === 'error') {
      const errorMessage = urlParams.get('error_message') || 'Unknown error';
      console.log('Spotify authentication failed:', errorMessage);
      toast.error(`Spotify authentication failed: ${errorMessage}`);
        }
   
    if (urlParams.toString()) {
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  const handleGeneratePlaylistAfterAuth = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/spotify/generatePlaylist`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          mood: currentMood,
          tracks_count: 20
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.action === 'playlist_created') {
    
        setLastPlaylist(data);
        setIsGeneratingPlaylist(false);
        console.log('Playlist created successfully:', data.playlist_name);
        toast.success(`Playlist "${data.playlist_name}" was successfully created`);
      } 
      else if (data.action === 'open_popup') {
        console.log('Authentication failed');
        toast.error('Authentication failed');
        setIsGeneratingPlaylist(false);
      }
    } catch (error) {
      console.error('Error creating playlist after authentication:', error);
      toast.error('Error creating playlist after authentication');
      setIsGeneratingPlaylist(false);
    }
  };

  const handleGeneratePlaylist = async () => {
    setIsGeneratingPlaylist(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/spotify/generatePlaylist`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          mood: currentMood,
          tracks_count: 20
        })
      });

      const data = await response.json();

      if (data.action === 'open_popup') {
        
        const popup = window.open(
          data.popup_url, 
          'spotify-auth',
          'width=500,height=600,scrollbars=yes,resizable=yes,centerscreen=yes'
        );
        
        if (popup) {
          popup.focus();
          window.checkPopupClosed(popup);
        }
        
      } else if (data.action === 'playlist_created') {
      
        setLastPlaylist(data);
        setIsGeneratingPlaylist(false);
        console.log('Playlist created successfully:', data.playlist_name);
        toast.success(`Playlist "${data.playlist_name}" was successfully created`);
      } 
    } catch (error) {
      console.error('Error creating playlist:', error);
      toast.error('Error creating playlist');
      setIsGeneratingPlaylist(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    const userMessage = input.trim();
    setMessages((prev) => [...prev, { sender: 'user', text: userMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/sentiment`, {
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
        text: 'Sorry, something went wrong. Please try again.' 
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
            <p className={styles.subtitle}>Your AI Buddy</p>
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
                  <span className={styles.typing}>MindMate is typing...</span>
                </div>
              )}
              <div ref={endRef} />
            </div>

            <form className={styles.inputRow} onSubmit={handleSubmit}>
              <Input
                className={styles.input}
                placeholder="Enter your answer here..."
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
                {isLoading ? '...' : 'Send'}
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card className={`${styles.card} ${styles.moodCard}`}>
          <CardContent>
            <div className={styles.moodSection}>
              <p className={styles.moodLabel}>
                Your mood: {currentMood} 
                {moodConfidence > 0 && (
                  <span className={styles.confidence}>
                    ({Math.round(moodConfidence * 100)}% sure)
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

            <Button 
              className={styles.ctaBtn} 
              variant="outline"
              onClick={handleGeneratePlaylist}
              disabled={isGeneratingPlaylist}
            >
              {isGeneratingPlaylist ? 'Creating playlist...' : '🎵 Generate Spotify Playlist'}
            </Button>

            {lastPlaylist && (
              <div className={styles.playlistCardWrapper}>
                <Card className={styles.moodCard}>
                  <CardContent>
                    <div className={styles.playlistCard}>
                      <img
                        src="/mindmate.jpeg"
                        alt="Playlist Cover"
                        className={styles.playlistImage}
                        onError={e => { e.target.src = "/mindmate.jpeg"; }}
                      />
                      <div className={styles.playlistInfo}>
                        <h3 className={styles.playlistTitle}>{lastPlaylist.playlist_name}</h3>
                        <p className={styles.playlistSongs}>{lastPlaylist.tracks_added} songs added</p>
                        <Button
                          type="button"
                          onClick={() => window.open(lastPlaylist.playlist_url, '_blank', 'noopener,noreferrer')}
                          className={styles.playlistOpenBtn}
                        >
                          Open in Spotify
                      </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </main>
  );
}