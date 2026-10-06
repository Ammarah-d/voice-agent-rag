# Real-Time Customer Support Voice AI Agent with RAG

A production-grade, low-latency voice agent capable of natural bi-directional dialogue, interruption handling, and real-time knowledge base lookups using Retrieval-Augmented Generation (RAG).

## Architecture
- **WebRTC & Real-time Media:** LiveKit Cloud
- **Speech-to-Text (STT):** Deepgram Nova-2
- **LLM Reasoning & Function Calling:** Google Gemini Flash
- **Text-to-Speech (TTS):** Deepgram Aura (Asteria)
- **Voice Activity Detection (VAD):** Silero VAD
- **Vector Retrieval (RAG):** Local ChromaDB

## Key Features
- **Sub-Second Latency:** Decoupled streaming inference pipeline delivering conversational responsiveness without dedicated GPU hardware.
- **Dynamic Policy Ingestion:** Grounds answers in enterprise manuals using vector similarity queries triggered via agent tool calls.
- **Interruption Handling (Barge-in):** Instantly cancels TTS playback when user speech is detected mid-sentence.

## Getting Started

1. Clone this repository and configure credentials in `.env`:
   ```env
   LIVEKIT_URL=...
   LIVEKIT_API_KEY=...
   LIVEKIT_API_SECRET=...
   GOOGLE_API_KEY=...
   DEEPGRAM_API_KEY=...
