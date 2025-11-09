# Smart-term

[![License](https://img.shields.io/github/license/Lusan-sapkota/smart-term)](https://github.com/Lusan-sapkota/smart-term/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Built With](https://img.shields.io/badge/built%20with-boredom-orange)](https://github.com/Lusan-sapkota/smart-term)
[![Powered By](https://img.shields.io/badge/powered%20by-perplexity-purple)](https://www.perplexity.ai/)

> Smart-term? Yeah, the name sounded weird to me too, but here we are.

> The little brother of [Smart-Shell](https://github.com/Lusan-sapkota/smart-shell) - because my Perplexity API subscription was gathering dust and I was bored.

An AI-powered terminal assistant that actually works. Ask questions, analyze files, get instant answers - all from your command line.

## Demo

*Demo recording coming soon. For now, just install it and see the magic yourself.*

## Why This Exists

My Perplexity API was going to waste. I got bored. This happened.

Now you can ask your terminal anything and it'll answer back. It's like having a really smart friend who never sleeps and doesn't judge your 3 AM coding questions.

## Installation

One line. That's it.

```bash
curl -fsSL https://raw.githubusercontent.com/Lusan-sapkota/smart-term/main/install.sh | bash
```

The installer will:
- Install dependencies (if needed)
- Set up the `ai` command globally
- Ask for your Perplexity API key
- Get out of your way

Get your free API key at: [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)

### Manual Installation

If you prefer to clone and install manually:

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

# Special commands
ai --bored                         # Better try it yourself
ai --update                        # Update to latest version
```

**Pro tip:** Quotes are only needed if your query has special shell characters. Otherwise, just type naturally!

## Features

- **File Support**: PDFs, images (PNG, JPG, JPEG), text files, code files
- **Multiple Models**: Choose based on your needs (speed vs depth)
- **Rich Output**: Syntax-highlighted, formatted responses with source citations
- **Source Citations**: Automatically displays source URLs from Perplexity responses
- **Thinking Animation**: See when the AI is working (disable in config if you prefer silence)
- **Configurable**: Customize everything via `~/.ai_cli_config.json`
- **Easter Egg**: `ai --bored` for when you need a break (dev memes and quotes)

## Configuration

Config lives at `~/.ai_cli_config.json`. Edit it to your liking:

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

See `docs/example_config.json` for all options and examples.

## Models

| Flag | Model | Best For |
|------|-------|----------|
| `--s` | sonar | Quick questions, general use (default) |
| `--p` | sonar-pro | Enhanced reasoning, better answers |
| `--r` | sonar-reasoning-pro | Complex problems, deep thinking |
| `--deep` | sonar-deep-research | Research, comprehensive analysis |

## API Key Setup

During installation, you'll be prompted for your API key. If you skip it:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PERPLEXITY_API_KEY='your-api-key-here'

# Or create ~/.smart-term/.env
echo "PERPLEXITY_API_KEY=your-api-key-here" > ~/.smart-term/.env
```

## Requirements

- Python 3.10+
- Internet connection
- Perplexity API key (free tier available)

## Other Providers?

Currently only Perplexity is supported because that's what I'm paying for. Want Gemini, Claude, or something else? Open an issue. I'll probably add Gemini support when my Perplexity subscription ends (or when I get bored again).

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

Found a bug? Want a feature? Open an issue or PR. I'm friendly.

## License

MIT License - do whatever you want with it.

## Author

**Lusan Sapkota**

- Website: [lusansapkota.com.np](https://lusansapkota.com.np)
- GitHub: [@Lusan-sapkota](https://github.com/Lusan-sapkota)
- Email: sapkotalusan@gmail.com

## Related Projects

- [Smart-Shell](https://github.com/Lusan-sapkota/smart-shell) - The big brother. More features, more complexity.

## Acknowledgments

Thanks to Perplexity for the API that was going to waste anyway.

---

Made with boredom and a Perplexity subscription.
