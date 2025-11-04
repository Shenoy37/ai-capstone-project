# BRD Generator

A lightweight Flask application that turns plain-text discovery notes into domain-specific Business Requirements Documents (BRDs) for the Pharma and Finance industries. The generator can leverage GPT-4 (via the OpenAI API) when available and automatically falls back to a deterministic template when an API key is not configured.

## Features

- 📄 Plain-text input form for pasting findings from discovery PDFs or notes.
- 🏥💰 Domain toggles for Pharma and Finance with tailored objectives, compliance, and risks.
- 🤖 GPT-4 integration (optional) that returns structured JSON perfectly suited for BRD outlines.
- 🧱 Offline fallback template that still produces a comprehensive BRD without external APIs.
- 📥 One-click Word document export using `python-docx`.

## Getting Started

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file (or set environment variables manually) with:

```bash
export FLASK_SECRET_KEY="choose-a-strong-secret"
export OPENAI_API_KEY="sk-your-openai-key"  # optional but enables GPT-4 output
```

If `OPENAI_API_KEY` is omitted the app still works, using the domain-specific fallback template.

### 3. Run the app

```bash
flask --app app:create_app --debug run
```

Navigate to `http://localhost:5000` and generate BRDs on demand.

## Project Structure

```
app.py                # Flask entry point and route definitions
app/
  brd_generator.py    # GPT-4 client wrapper and deterministic template builder
  docx_exporter.py    # Helper for exporting BRDs as Word documents
  templates/          # Jinja templates for the UI
  static/css/         # Styling overrides
```

## How GPT-4 Responses Are Used

When an `OPENAI_API_KEY` is present the app calls the `gpt-4o` model with a structured prompt that returns JSON. The JSON maps directly to BRD sections shown on the page and in the exported Word document. Errors or malformed responses automatically trigger the fallback template, guaranteeing a usable BRD every time.

## Extending the Generator

- Add new domains by updating the `domain_specifics` dictionary in `app/brd_generator.py`.
- Modify the BRD schema by changing the JSON prompt and the rendering/export logic.
- Integrate authentication or persistence if multiple teams will collaborate on drafts.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
