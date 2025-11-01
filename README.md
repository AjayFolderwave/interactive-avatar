# 🎭 Interactive Avatar

A real-time AI-powered interactive avatar web application using Tavus CVI technology.

## ✨ Features

- 🗣️ **Real-time Conversations** - Talk naturally with your AI avatar
- ⚡ **Sub-second Response Time** - Lightning-fast AI responses
- 🎭 **Perfect Lip-Sync** - Flawless facial animations
- 🎨 **Beautiful Modern UI** - Sleek glassmorphism design
- 🌐 **Scalable** - Handle unlimited concurrent conversations

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Tavus API key ([Get one here](https://platform.tavus.io))

### Installation

1. **Clone or navigate to the project:**
```bash
cd /Users/ajaykumarreddy/Desktop/PROJECTS/interactive-avatar
```

2. **Install dependencies:**
```bash
pip3 install -r requirements.txt
```

3. **Set up environment variables:**

Create a `.env` file with:
```env
# Required
TAVUS_API_KEY=your_tavus_api_key_here
TAVUS_REPLICA_ID=r18d46c93e

# Optional
TAVUS_PERSONA_ID=your_persona_id_here
```

### Running the App

Start the server:
```bash
python3 server.py
```

Or with uvicorn:
```bash
uvicorn server:app --reload
```

Then open your browser to: **http://localhost:8000**

## 🎯 Usage

1. Open http://localhost:8000
2. Click **"Start Conversation"**
3. Allow microphone access when prompted
4. Start talking to your avatar!

## 📁 Project Structure

```
interactive-avatar/
├── server.py          # FastAPI server
├── index.html         # Web UI
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (create this)
└── README.md         # This file
```

## 🔧 Configuration

### Change Avatar

Update `TAVUS_REPLICA_ID` in your `.env` file. [Browse available replicas](https://platform.tavus.io/replicas)

### Customize Personality

Edit the `conversational_context` in `server.py`:

```python
"conversational_context": "Your custom personality prompt here..."
```

## 🐛 Troubleshooting

### Port Already in Use

Change the port in `server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed to 8001
```

### Conversation Fails to Start

- Check your Tavus API key is valid
- Ensure you don't have too many active conversations
- Check the server logs for detailed errors

## 📚 Documentation

- [Tavus API Docs](https://docs.tavus.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

## 🎨 Customization

The UI is fully customizable via `index.html`. Modify colors, layout, and styling in the `<style>` section.

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Feel free to submit issues and PRs.

---

Built with ❤️ using Tavus CVI Technology
