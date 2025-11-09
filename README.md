# Smart-term

[![License](https://img.shields.io/github/license/Lusan-sapkota/smart-term)](https://github.com/Lusan-sapkota/smart-term/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Built With](https://img.shields.io/badge/built%20with-boredom-orange)](https://github.com/Lusan-sapkota/smart-term)
[![Powered By](https://img.shields.io/badge/powered%20by-perplexity-purple)](https://www.perplexity.ai/)

> Smart-term? Yeah, the name sounded weird to me too, but here we are.

> The little brother of [Smart-Shell](https://github.com/Lusan-sapkota/smart-shell) - born from a deadly combination of boredom and an unused Perplexity API subscription.

An AI-powered terminal assistant that actually works. Ask questions, analyze files, get instant answers - all without leaving your terminal (because who needs a browser anyway?).

## Demo

*Demo recording coming soon (I won't upload it!). For now, just trust me bro - it works.*

## Why This Exists

My Perplexity API was sitting there, judging me for not using it. I got bored one weekend. This is what happened.

Now you can ask your terminal anything and it'll answer back. It's like having a really smart friend who:
- Never sleeps
- Never judges your 3 AM "how do I exit vim" questions
- Doesn't ask why you're still debugging at 4 AM
- Won't tell anyone about your Stack Overflow addiction

## Installation

One line. That's literally it. No npm hell, no dependency nightmares, no "works on my machine" excuses.

```bash
curl -fsSL https://raw.githubusercontent.com/Lusan-sapkota/smart-term/main/install.sh | bash
```

The installer will:
- Install dependencies (if you don't have them)
- Set up the `ai` command globally (because typing is hard)
- Ask for your Perplexity API key (politely)
- Get out of your way (unlike most installers)

Get your free API key at: [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)

*Yes, it's free. No, there's no catch. Yes, I'm as surprised as you are.*

### Manual Installation

If you're the "I don't trust curl | bash" type (respect):

```bash
git clone https://github.com/Lusan-sapkota/smart-term.git
cd smart-term
chmod +x install.sh
./install.sh
```

### Updating

Already have smart-term installed? Update to the latest version:

```bash
# Easiest way
ai --update

# Or via curl
curl -fsSL https://raw.githubusercontent.com/Lusan-sapkota/smart-term/main/update.sh | bash

# Or manually
cd ~/.smart-term
git pull origin main
source venv/bin/activate
pip install -e .
```

## Usage

```bash
# Ask anything (quotes optional for simple queries)
ai "What is the capital of France?"
ai What is the capital of France?

# Analyze files
ai document.pdf "Summarize this"
ai document.pdf Summarize this
ai image.png "What's in this image?"
ai script.py "Explain this code"

# Use different models (flags work anywhere)
ai "Complex question" --p          # sonar-pro (enhanced reasoning)
ai What is quantum computing --deep # sonar-deep-research
ai "Quick question" --s            # sonar (default, fast)
ai Solve this problem --r          # sonar-reasoning-pro

# Show source citations (hidden by default)
ai "Research topic" --show-sources # Display clickable source links
ai "Deep research" --deep --show-sources

# Special commands
ai --bored                         # Better try it yourself
ai --update                        # Update to latest version
```

**Pro tips:** 
- Quotes are optional unless your query has weird shell characters. Live dangerously.
- Sources are hidden by default because who actually reads those anyway? Use `--show-sources` if you're feeling academic.
- Model names are color-coded because I got bored: sonar (cyan), sonar-pro (magenta), sonar-reasoning-pro (yellow), sonar-deep-research (blue)
- Citation numbers are clickable when `--show-sources` is used. Yes, your terminal can do that. Welcome to 2025.

## Features

- **File Support**: PDFs, images, text files, code - throw whatever at it
- **Multiple Models**: From "quick answer" to "write my thesis" levels of depth
- **Rich Output**: Syntax-highlighted, color-coded, prettier than your ex
- **Source Citations**: Optional clickable URLs (for when you need to look smart)
- **Clean by Default**: No citation spam unless you ask for it
- **Thinking Animation**: A spinner that says "I'm working, I promise"
- **Configurable**: Tweak everything in `~/.ai_cli_config.json` (if you're into that)
- **Easter Egg**: `ai --bored` for when you need a break (100+ dev memes and quotes)

## Configuration

Config lives at `~/.ai_cli_config.json`. Tweak it if the defaults aren't your vibe:

```json
{
  "default_model": "sonar",
  "default_provider": "perplexity",
  "timeout": 30,
  "max_file_size_mb": 10,
  "output_format": "markdown",
  "show_thinking_animation": true,
  "log_level": "INFO"
}
```

See `docs/example_config.json` for all options and examples. Or don't. The defaults are pretty good.

## Models

Pick your poison:

| Flag | Model | Best For |
|------|-------|----------|
| `--s` | sonar | Quick questions, "what's for dinner" level stuff (default) |
| `--p` | sonar-pro | When you need actual brain power |
| `--r` | sonar-reasoning-pro | Complex problems, existential crises |
| `--deep` | sonar-deep-research | PhD-level research, or when you're really procrastinating |

## API Key Setup

During installation, you'll be prompted for your API key. If you chickened out:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PERPLEXITY_API_KEY='your-api-key-here'

# Or create ~/.smart-term/.env
echo "PERPLEXITY_API_KEY=your-api-key-here" > ~/.smart-term/.env
```

Then restart your terminal. Or don't, and wonder why it doesn't work.

## Requirements

- Python 3.10+ (if you're still on 2.7, we need to talk)
- Internet connection (obviously)
- Perplexity API key (free tier available, no credit card required)
- A terminal (you're a developer, you have one)

## Other Providers?

Currently only Perplexity is supported because that's what I'm paying for. 

Want Gemini, Claude, or something else? Open an issue. I'll probably add Gemini support when:
- My Perplexity subscription ends
- I get bored again (likely)
- Someone asks nicely (very likely)
- I procrastinate on actual work (extremely likely)

## Development

```bash
# Clone the repo
git clone https://github.com/Lusan-sapkota/smart-term.git
cd smart-term

# Install in development mode
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Run
ai "test query"
```

## Project Structure

```
smart-term/
├── smart_term/
│   ├── cli/           # Argument parsing
│   ├── config/        # Configuration management
│   ├── files/         # File handling (PDF, images, text)
│   ├── output/        # Response formatting and display
│   ├── providers/     # AI provider integrations
│   └── utils/         # Logging, errors, helpers
├── docs/              # Documentation and examples
├── install.sh         # One-line installer
└── setup.py           # Package configuration
```

## Contributing

Found a bug? Want a feature? Open an issue or PR. I promise I'm friendly (and I actually read them).

## License

MIT License - do whatever you want with it.

## Author

**Lusan Sapkota**

- Website: [lusansapkota.com.np](https://lusansapkota.com.np)
- GitHub: [@Lusan-sapkota](https://github.com/Lusan-sapkota)
- Email: sapkotalusan@gmail.com

## Related Projects

- [Smart-Shell](https://github.com/Lusan-sapkota/smart-shell) - The big brother. More features, more complexity, more "why did I build this?"

## Acknowledgments

Thanks to:
- Perplexity for the API that was gathering dust
- Boredom, my most productive state
- Coffee, the real MVP
- Stack Overflow, for obvious reasons
- That one person who will actually read this entire README

## FAQ

**Q: Why did you build this?**  
A: Boredom + unused API subscription = this

**Q: Is it production-ready?**  
A: Define "production"

**Q: Can I use this for my startup?**  
A: Sure, but don't blame me when your investors ask questions

**Q: Why is it called Smart-term?**  
A: I was tired when I named it. Don't judge.

---

Made with boredom, a Perplexity subscription, and questionable life choices.
