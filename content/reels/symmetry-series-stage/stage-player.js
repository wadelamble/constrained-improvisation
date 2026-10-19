'use strict';

// Local review player. All media and captions come from the staged manifest.
// Embedded soundtracks play through the reel; YouTube is a preview-only fallback.
const q = id => document.getElementById(id);
const video = q('video');
let trackId = null;
let musicAPIRequested = false;
let trackDuration = 0;
let items = [];
let selected = -1;
let musicEnabled = true;
let musicBaked = false;
let musicReady = false;
let musicFailed = false;
let musicBlocked = false;
let player = null;
let buffering = false;
let commandedPauseUntil = 0;
let lastDriftCheck = 0;
let lastMusicSeek = 0;
let lastVolume = -1;
let apiTimer = null;
let copyTimer = null;
let startCheckTimer = null;

const current = () => items[selected];
const timeLabel = seconds => {
  const whole = Math.max(0, Math.floor(Number(seconds) || 0));
  return Math.floor(whole / 60) + ':' + String(whole % 60).padStart(2, '0');
};
const assetURL = (entry, key) => {
  const url = new URL(entry[key], location.href);
  const hash = entry[key + '_sha256'] || (entry.sha256 && entry.sha256[key]);
  if (hash) url.searchParams.set('v', String(hash).slice(0, 12));
  return url.href;
};
const wantsMusic = () => !musicBaked && Boolean(trackId) && musicEnabled && !musicFailed && selected >= 0 &&
  !video.paused && !video.ended && !video.seeking && !buffering &&
  video.playbackRate === 1 && video.readyState >= 2;
const musicPosition = () => {
  const elapsed = Math.max(0, (Number(current()?.music_start_seconds) || 0) + (video.currentTime || 0));
  return trackDuration > 0 ? elapsed % trackDuration : elapsed;
};

function refreshTrackDuration() {
  if (!musicReady || typeof player.getDuration !== 'function') return;
  const duration = Number(player.getDuration());
  if (Number.isFinite(duration) && duration > 0) trackDuration = duration;
}

function musicStatus(message) {
  q('music-status').textContent = musicBaked ? 'Soundtrack included in the videos.' : message;
}

function pauseMusic() {
  if (!musicReady) return;
  commandedPauseUntil = performance.now() + 1600;
  player.pauseVideo();
}

function updateVolume() {
  if (!musicReady) return;
  const duration = Number(current()?.duration_seconds) || video.duration || 0;
  const t = video.currentTime || 0;
  let fade = Math.max(0, Math.min(1, t / 1.5, (duration - t) / 2));
  if (trackDuration > 0) {
    // A gentle fade at the recording seam, rather than a simulated crossfade.
    const musicTime = Number(player.getCurrentTime());
    if (Number.isFinite(musicTime)) {
      fade *= Math.max(0, Math.min(1, musicTime / .75, (trackDuration - musicTime) / 1.2));
    }
  }
  const volume = wantsMusic() ? Math.round(Number(q('music-volume').value) * fade) : 0;
  if (lastVolume !== volume) {
    player.setVolume(volume);
    lastVolume = volume;
  }
}

function positionMusic() {
  if (!musicReady || !current()) return;
  refreshTrackDuration();
  if (wantsMusic()) {
    player.seekTo(musicPosition(), true);
    lastMusicSeek = performance.now();
  } else {
    pauseMusic();
    // Cueing selects the excerpt without starting playback.
    player.cueVideoById({ videoId: trackId, startSeconds: musicPosition() });
  }
}

function startMusic(force = false) {
  if (!wantsMusic()) { pauseMusic(); updateVolume(); return; }
  if (musicBlocked && !force) return;
  if (!musicReady) {
    if (!musicFailed) musicStatus('Music is loading. The reel can play while you wait.');
    return;
  }
  musicBlocked = false;
  q('retry-music').hidden = true;
  player.unMute();
  updateVolume();
  positionMusic();
  player.playVideo();
  musicStatus('Starting the music…');
  clearTimeout(startCheckTimer);
  startCheckTimer = setTimeout(() => {
    if (wantsMusic() && musicReady && player.getPlayerState() !== 1 && !musicFailed) {
      musicStatus('Music has not started. You can enable it here or continue without it.');
      q('retry-music').hidden = false;
    }
  }, 6000);
}

function setMusicEnabled(enabled) {
  if (musicBaked) return;
  musicEnabled = enabled;
  q('music-toggle').setAttribute('aria-pressed', String(enabled));
  q('music-toggle').textContent = enabled ? 'Music on' : 'Music off';
  if (!enabled) {
    pauseMusic(); updateVolume();
    musicStatus('Music off.');
    q('retry-music').hidden = true;
  } else if (musicFailed) {
    musicStatus('The recording is unavailable in this preview. The reels still play.');
  } else if (wantsMusic()) {
    startMusic(true);
  } else {
    musicStatus('Music will start with the reel.');
  }
}

function musicError(code) {
  musicFailed = true;
  pauseMusic();
  q('retry-music').hidden = true;
  const reasons = {
    2: 'YouTube could not open this recording.',
    5: 'The browser could not play the recording.',
    100: 'The recording is unavailable.',
    101: 'This recording cannot play in an embedded player.',
    150: 'This recording cannot play in an embedded player.',
    153: 'YouTube could not verify this preview page.'
  };
  musicStatus((reasons[code] || 'YouTube could not play the recording.') + ' The reels still play without music.');
}

window.onYouTubeIframeAPIReady = () => {
  clearTimeout(apiTimer);
  if (musicBaked || !trackId) return;
  player = new YT.Player('youtube-player', {
    width: '100%', height: 225, videoId: trackId,
    playerVars: { autoplay: 0, controls: 1, playsinline: 1, origin: location.origin },
    events: {
      onReady: event => {
        if (musicBaked || !trackId) return;
        musicReady = true;
        musicFailed = false;
        event.target.setVolume(0);
        lastVolume = 0;
        refreshTrackDuration();
        positionMusic();
        if (wantsMusic()) startMusic();
        else musicStatus(musicEnabled ? 'Music will start with the reel.' : 'Music off.');
      },
      onStateChange: event => {
        if (event.data === 1) {
          if (!wantsMusic()) { pauseMusic(); updateVolume(); return; }
          refreshTrackDuration();
          musicBlocked = false;
          q('retry-music').hidden = true;
          updateVolume();
          musicStatus('Playing softly with the reel.');
        } else if (event.data === 3 && wantsMusic()) {
          musicStatus('Music buffering…');
        } else if (event.data === 0 && wantsMusic()) {
          // Follow the reel's running timeline through every repeat of the track.
          refreshTrackDuration();
          startMusic();
        } else if (event.data === 2 && wantsMusic()) {
          musicStatus('Music paused.');
          // A pause through YouTube's own controls is also respected.
          if (performance.now() > commandedPauseUntil) setMusicEnabled(false);
        }
      },
      onError: event => musicError(event.data),
      onAutoplayBlocked: () => {
        musicBlocked = true;
        musicStatus('Your browser needs a click to start the music.');
        q('retry-music').hidden = false;
      }
    }
  });
};

function loadMusicAPI() {
  if (musicBaked || !trackId) return;
  if (window.YT && typeof window.YT.Player === 'function') {
    window.onYouTubeIframeAPIReady();
    return;
  }
  if (musicAPIRequested) return;
  musicAPIRequested = true;
  const script = document.createElement('script');
  script.id = 'youtube-iframe-api';
  script.src = 'https://www.youtube.com/iframe_api';
  script.async = true;
  script.onerror = () => {
    clearTimeout(apiTimer);
    if (musicBaked) return;
    musicFailed = true;
    musicStatus('The music player could not load. The reels still play without music.');
  };
  apiTimer = setTimeout(() => {
    if (!musicReady) musicStatus('The music player is taking longer to load. The reels can play without it.');
  }, 15000);
  document.head.append(script);
}

function configureMusic(config) {
  const baked = config?.baked_into_exports === true;
  const requestedId = config?.video_id || config?.youtube_video_id || config?.trackId ||
    config?.track_id || config?.videoId || config?.trackID;
  const pending = !baked && (config?.status === 'pending' || !/^[A-Za-z0-9_-]{11}$/.test(requestedId || ''));
  const nextId = baked || pending ? null : requestedId;
  const modeChanged = baked !== musicBaked;
  musicBaked = baked;
  if (nextId !== trackId || pending || modeChanged) {
    pauseMusic();
    clearTimeout(startCheckTimer);
    clearTimeout(apiTimer);
    if (player && typeof player.destroy === 'function') player.destroy();
    player = null;
    musicReady = false;
    musicFailed = false;
    musicBlocked = false;
    lastVolume = -1;
    trackDuration = 0;
    trackId = nextId;
    // The API replaces this element with its iframe, so restore it for a new track.
    const holder = document.createElement('div');
    holder.id = 'youtube-player';
    document.querySelector('.music-player').replaceChildren(holder);
  }
  q('music-pending').hidden = !pending;
  q('music-controls').hidden = pending;
  q('music-toggle').hidden = baked;
  q('music-volume-row').hidden = baked;
  q('music-player').hidden = baked;
  q('retry-music').hidden = true;
  q('music-note').textContent = baked
    ? 'Use the reel player’s volume control.'
    : 'Music plays in this preview. MP4 exports are silent until an audio source is supplied.';
  if (pending) {
    musicEnabled = false;
    q('music-pending').textContent = 'Music selection pending.';
    return;
  }
  q('music-title').textContent = config.title || 'Selected recording';
  const source = config.source_url || (trackId ? 'https://www.youtube.com/watch?v=' + trackId : '');
  q('music-artist').textContent = config.artist ? config.artist + (source ? ' ·' : '') : '';
  q('music-source').href = source;
  q('music-source').hidden = !source;
  if (baked) {
    musicEnabled = false;
    video.defaultMuted = false;
    video.muted = false;
    // The exported audio already has its quiet mix level applied.
    video.volume = 1;
    musicStatus();
    return;
  }
  const volume = Math.max(0, Math.min(30, Number(config.volume_percent ?? 10)));
  q('music-volume').value = String(Number.isFinite(volume) ? volume : 10);
  q('volume-value').textContent = q('music-volume').value + '%';
  musicEnabled = config.enabled !== false;
  q('music-toggle').setAttribute('aria-pressed', String(musicEnabled));
  q('music-toggle').textContent = musicEnabled ? 'Music on' : 'Music off';
  musicStatus(musicEnabled ? 'Music will start with the reel.' : 'Music off.');
  if (!musicReady) loadMusicAPI();
}

function updateElapsed() {
  q('elapsed').textContent = timeLabel(video.currentTime) + ' / ' + timeLabel(current()?.duration_seconds || video.duration);
}

async function playReel() {
  try {
    if (video.ended) video.currentTime = 0;
    await video.play();
  } catch (error) {
    q('video-status').textContent = error.name === 'NotAllowedError' ? 'Press Play reel to start playback.' : 'This reel could not start. Try the MP4 link.';
  }
}

function choose(index, autoplay = false) {
  if (!items.length) return;
  video.pause();
  pauseMusic();
  buffering = false;
  selected = Math.max(0, Math.min(items.length - 1, index));
  const entry = current();
  video.poster = assetURL(entry, 'cover');
  video.src = assetURL(entry, 'video');
  q('title').textContent = String(entry.order).padStart(2, '0') + ' · ' + entry.title;
  q('caption').textContent = entry.caption;
  q('count').textContent = entry.duration_seconds + ' seconds · ' + entry.caption_buffer_count + ' / 2,196 caption characters';
  q('mp4').href = assetURL(entry, 'video');
  q('cover').href = assetURL(entry, 'cover');
  q('txt').href = assetURL(entry, 'caption_file');
  q('previous').disabled = selected === 0;
  q('next').disabled = selected === items.length - 1;
  q('copy').textContent = 'Copy caption';
  q('play').textContent = 'Play reel';
  q('video-status').textContent = '';
  clearTimeout(copyTimer);
  document.querySelectorAll('#nav button').forEach((button, i) => {
    button.classList.toggle('active', i === selected);
    if (i === selected) button.setAttribute('aria-current', 'true');
    else button.removeAttribute('aria-current');
  });
  history.replaceState(null, '', '#' + entry.order);
  updateElapsed();
  positionMusic();
  if (!musicFailed && !musicBlocked) musicStatus(musicEnabled ? 'Music will start with the reel.' : 'Music off.');
  if (autoplay) playReel();
}

function chooseHash() {
  const number = Number(location.hash.slice(1));
  const index = items.findIndex(entry => Number(entry.order) === number);
  choose(index < 0 ? 0 : index);
}

async function loadSeries() {
  q('reload').hidden = true;
  q('load-status').textContent = 'Loading the series…';
  try {
    const response = await fetch('manifest.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('Manifest unavailable');
    const manifest = await response.json();
    if (!Array.isArray(manifest.episodes) || !manifest.episodes.length) throw new Error('No reels');
    items = manifest.episodes;
    q('nav').replaceChildren();
    items.forEach((entry, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      const number = document.createElement('span');
      number.className = 'number';
      number.textContent = String(entry.order).padStart(2, '0');
      const title = document.createElement('span');
      title.textContent = entry.title;
      button.append(number, title);
      button.addEventListener('click', () => choose(index));
      q('nav').append(button);
    });
    q('playlist-label').textContent = 'All ' + items.length + ' reels';
    q('series-description').textContent = items.length + ' reels from the pool table to complex waves, with the latest titles and captions.';
    q('load-status').textContent = '';
    q('stage').hidden = false;
    chooseHash();
    configureMusic(manifest.music);
  } catch (error) {
    q('load-status').textContent = 'The stage is still being prepared, or the series could not be loaded. Try again shortly.';
    q('reload').hidden = false;
  }
}

q('previous').addEventListener('click', () => choose(selected - 1));
q('next').addEventListener('click', () => choose(selected + 1));
q('play').addEventListener('click', () => video.paused ? playReel() : video.pause());
q('restart').addEventListener('click', () => { video.currentTime = 0; playReel(); });
q('reload').addEventListener('click', loadSeries);
q('music-toggle').addEventListener('click', () => setMusicEnabled(!musicEnabled));
q('retry-music').addEventListener('click', () => {
  if (!musicEnabled) setMusicEnabled(true);
  if (video.paused) musicStatus('Press Play reel to start the music with it.');
  else startMusic(true);
});
q('music-volume').addEventListener('input', () => {
  q('volume-value').textContent = q('music-volume').value + '%';
  updateVolume();
});
q('copy').addEventListener('click', async () => {
  if (!current()) return;
  try {
    await navigator.clipboard.writeText(current().caption);
    q('copy').textContent = 'Copied';
    copyTimer = setTimeout(() => { q('copy').textContent = 'Copy caption'; }, 1800);
  } catch {
    const range = document.createRange();
    range.selectNodeContents(q('caption'));
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    q('copy').textContent = 'Selected — press Ctrl+C';
  }
});
video.addEventListener('play', () => { q('play').textContent = 'Pause reel'; startMusic(); });
video.addEventListener('playing', () => {
  buffering = false;
  q('video-status').textContent = '';
  startMusic();
});
video.addEventListener('pause', () => {
  q('play').textContent = 'Play reel';
  pauseMusic(); updateVolume();
  if (!musicFailed && !musicBlocked && musicEnabled) musicStatus('Paused with the reel.');
});
video.addEventListener('waiting', () => { buffering = true; pauseMusic(); updateVolume(); });
video.addEventListener('seeking', () => { pauseMusic(); updateVolume(); });
video.addEventListener('seeked', () => {
  buffering = false;
  updateElapsed();
  if (wantsMusic()) startMusic();
  else positionMusic();
});
video.addEventListener('timeupdate', () => { updateElapsed(); updateVolume(); });
video.addEventListener('loadedmetadata', updateElapsed);
video.addEventListener('error', () => {
  pauseMusic();
  q('video-status').textContent = 'This video is unavailable. It may still be rendering. Try again shortly.';
});
video.addEventListener('ended', () => {
  pauseMusic(); updateVolume();
  q('play').textContent = 'Replay reel';
  if (q('auto-next').checked && selected < items.length - 1) choose(selected + 1, true);
});
video.addEventListener('ratechange', () => {
  if (musicBaked) return;
  // Respect the viewer's chosen speed without chopping or accelerating the music.
  if (video.playbackRate !== 1) {
    pauseMusic(); updateVolume();
    if (musicEnabled && !musicFailed) musicStatus('Music pauses while the reel plays at an altered speed.');
  } else if (wantsMusic()) startMusic();
});
window.addEventListener('hashchange', chooseHash);
window.addEventListener('pagehide', pauseMusic);

setInterval(() => {
  if (!musicReady) return;
  refreshTrackDuration();
  if (!wantsMusic()) {
    if (player.getPlayerState() === 1) pauseMusic();
    updateVolume();
    return;
  }
  updateVolume();
  const now = performance.now();
  if (now - lastDriftCheck > 1500 && now - lastMusicSeek > 3000 && player.getPlayerState() === 1) {
    lastDriftCheck = now;
    if (Math.abs(player.getCurrentTime() - musicPosition()) > 2.5) positionMusic();
  }
}, 250);

loadSeries();
