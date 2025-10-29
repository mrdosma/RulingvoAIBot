# 🇷🇺 Russian Learner Bot

A comprehensive Telegram bot for learning Russian language with AI-powered features, gamification, and interactive exercises.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-green.svg)](https://aiogram.dev/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

### 📚 Learning Modules
- **Vocabulary System**
  - AI-generated word lists by CEFR level (A1-C2)
  - Flashcard review with spaced repetition
  - Track learned/unlearned words
  - 8-stage spaced repetition algorithm

- **Grammar Exercises**
  - Level-appropriate grammar lessons
  - AI-powered evaluation and feedback
  - Progress tracking per topic
  - Instant corrections and explanations

- **Listening Practice**
  - AI-generated audio exercises
  - Multiple difficulty levels
  - Speech recognition evaluation
  - Real Russian pronunciation

- **Speaking Practice**
  - Voice message recognition (Whisper API)
  - Pronunciation feedback
  - Grammar and vocabulary analysis
  - Real-time corrections

- **Free Practice Mode**
  - Write anything in Russian
  - Get detailed feedback
  - Vocabulary suggestions
  - Grammar corrections

### 🎮 Interactive Games
- **Speaking Duel** - 3-round conversation with AI
- **Spy Mission** - Complete role-play scenarios in Russian
- **Word Game** - Multiple-choice vocabulary quiz
- **Voice Support** - All games support voice messages

### 🏆 Gamification
- **XP System** - Earn points for every activity
- **Level Progression** - A1 → A2 → B1 → B2 → C1 → C2
- **Daily Goals** - Set and track daily XP targets
- **Streak Tracking** - Maintain learning streaks
- **12 Achievements** - Unlock badges and milestones
- **Global Leaderboard** - Compete with other learners

### 🌍 Multi-language Support
- Interface in 3 languages: 🇺🇿 Uzbek, 🇷🇺 Russian, 🇬🇧 English
- Switch language anytime in settings
- All buttons and menus translated

### 🔔 Smart Features
- Daily learning reminders
- Spaced repetition notifications
- Progress statistics and analytics
- Automatic streak maintenance
- Performance metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Telegram account
- OpenAI API key
- PostgreSQL (or SQLite for testing)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/russian-learner-bot.git
cd russian-learner-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Create Telegram bot**
- Talk to [@BotFather](https://t.me/botfather)
- Create new bot with `/newbot`
- Copy the token to `.env`

5. **Get OpenAI API key**
- Visit [OpenAI Platform](https://platform.openai.com/api-keys)
- Create new API key
- Add to `.env`

6. **Run the bot**
```bash
python bot.py
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

2. **Start all services**
```bash
docker-compose up -d
```

Services included:
- Bot application
- PostgreSQL database
- Redis cache
- Adminer (database GUI at `localhost:8080`)

3. **View logs**
```bash
docker-compose logs -f bot
```

4. **Stop services**
```bash
docker-compose down
```

### Using Docker only

```bash
# Build image
docker build -t russian-learner-bot .

# Run container
docker run -d \
  --name russian-bot \
  --env-file .env \
  russian-learner-bot
```

## ☁️ Deploy to Railway

1. **Fork this repository**

2. **Create Railway account** at [railway.app](https://railway.app)

3. **Create new project** → Deploy from GitHub

4. **Add PostgreSQL** plugin

5. **Set environment variables**:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`
   - `DATABASE_URL` (auto-filled by Railway)

6. **Deploy** - Railway will automatically deploy!

## 📖 Usage

### Bot Commands

- `/start` - Start the bot and choose language
- Send any Russian text for evaluation
- Send voice messages for pronunciation analysis

### Main Menu Options

1. **👤 Profile** - View your stats, level, XP, and progress
2. **🏆 Leaderboard** - See global rankings
3. **📖 Vocabulary** - Add/review words, flashcards
4. **📝 Grammar** - Practice grammar exercises
5. **🎧 Listening** - Audio comprehension practice
6. **✍️ Practice** - Free-form writing practice
7. **🎮 Games** - Speaking Duel, Spy Mission, Word Game
8. **🎖️ Achievements** - View unlocked achievements
9. **⚙️ Settings** - Change language, notifications

## 🎯 XP Rewards

| Activity | XP Earned |
|----------|-----------|
| Add new words | 10 XP |
| Review words | 5 XP |
| Flashcard correct | 5 XP |
| Grammar exercise | 20 XP |
| Listening exercise | 30 XP |
| Practice session | 25 XP |
| Speaking Duel win | 50 XP |
| Spy Mission complete | 50 XP |
| Word Game correct | 15 XP |
| Voice message | 20 XP |
| Daily login | 10 XP |

## 🏅 Achievements

| Achievement | Requirement | XP Bonus |
|-------------|-------------|----------|
| 🌟 First Word | Learn 1 word | 10 XP |
| 📚 Word Collector | Learn 10 words | 50 XP |
| 📖 Vocabulary Expert | Learn 50 words | 200 XP |
| 🎓 Word Master | Learn 100 words | 500 XP |
| 🔥 On Fire | 3 day streak | 30 XP |
| ⚡ Committed | 7 day streak | 100 XP |
| 💎 Dedicated | 30 day streak | 500 XP |
| 📈 Progress | Reach A2 | 100 XP |
| 🎯 Intermediate | Reach B1 | 300 XP |
| ⭐ Advanced | Reach B2 | 600 XP |
| ⚔️ Duelist | Win 10 duels | 150 XP |
| 🕵️ Agent | Complete 5 missions | 200 XP |

## 📊 Level System

| Level | Total XP Required | Description |
|-------|-------------------|-------------|
| A1 | 0 - 2,000 | Beginner |
| A2 | 2,000 - 5,000 | Elementary |
| B1 | 5,000 - 10,000 | Intermediate |
| B2 | 10,000 - 18,000 | Upper Intermediate |
| C1 | 18,000 - 30,000 | Advanced |
| C2 | 30,000+ | Proficient |

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available options.

**Essential:**
- `TELEGRAM_BOT_TOKEN` - Your bot token
- `OPENAI_API_KEY` - OpenAI API key
- `DATABASE_URL` - Database connection string

**Optional:**
- `REDIS_URL` - Redis for caching
- `SENTRY_DSN` - Error tracking
- `NOTIFICATION_TIME_HOUR` - Daily reminder time
- `DAILY_GOAL_XP` - Default daily goal

### Customization

Edit `config.py` to customize:
- XP rewards per activity
- Spaced repetition intervals
- Daily goals
- Rate limits
- AI parameters

## 🏗️ Architecture

```
russian-learner-bot/
├── bot.py              # Main bot file
├── config.py           # Configuration
├── utils.py            # Utility functions
├── requirements.txt    # Dependencies
├── Dockerfile         # Docker image
├── docker-compose.yml # Docker services
├── .env.example       # Environment template
├── README.md          # This file
└── temp/              # Temporary files
    └── audio/         # Generated audio
```

### Database Schema

- **users** - User profiles and progress
- **vocabulary** - User vocabulary with spaced repetition
- **achievements** - Unlocked achievements
- **grammar_progress** - Grammar topic progress
- **leaderboard** - Global rankings

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 🐛 Known Issues & Troubleshooting

### Voice recognition not working
- Ensure OpenAI Whisper API is accessible
- Check audio file format (OGG/MP3 supported)
- Verify `OPENAI_API_KEY` is valid

### Database connection errors
- Check `DATABASE_URL` format
- Ensure PostgreSQL is running
- Check firewall settings

### Bot not responding
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Check bot is running: `docker-compose ps`
- View logs: `docker-compose logs bot`

### Audio generation fails
- Install ffmpeg: `apt-get install ffmpeg`
- Check gTTS package is installed
- Verify temp directory is writable

## 📈 Roadmap

- [ ] Web dashboard for progress tracking
- [ ] Mobile app companion
- [ ] More language pairs (English→Russian, etc.)
- [ ] Group learning features
- [ ] Live tutoring sessions
- [ ] Certificate generation
- [ ] Integration with language courses
- [ ] Podcast-style lessons
- [ ] Video lessons
- [ ] Community features

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [Aiogram](https://aiogram.dev/) - Telegram Bot framework
- [OpenAI](https://openai.com/) - AI language models
- [gTTS](https://gtts.readthedocs.io/) - Text-to-speech
- Russian language community

## 📞 Support

- 📧 Email: support@example.com
- 💬 Telegram: [@yourusername](https://t.me/yourusername)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/russian-learner-bot/issues)

## 📸 Screenshots

### Main Menu
![Main Menu](screenshots/main_menu.png)

### Profile
![Profile](screenshots/profile.png)

### Flashcards
![Flashcards](screenshots/flashcards.png)

### Leaderboard
![Leaderboard](screenshots/leaderboard.png)

---

Made with ❤️ for Russian language learners worldwide

**Start learning Russian today!** 🇷🇺📚✨