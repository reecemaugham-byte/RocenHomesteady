import re
import os
import tempfile
import edge_tts


def clean_text_for_audio(text):
    """Remove emojis, markdown and special characters for TTS."""
    if not text:
        return ""
    # Remove emojis and symbols
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"
        "\u3030"
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub("", text)
    # Remove markdown
    text = text.replace("**", "").replace("*", "")
    text = text.replace("###", "").replace("##", "").replace("#", "")
    # Remove brackets and special chars
    text = re.sub(r"[\[\](){}<>]", "", text)
    # Clean up whitespace
    text = " ".join(text.split())
    return text.strip()


def generate_voice(text, voice="en-GB-SoniaNeural"):
    """Generate audio file from text using Edge TTS. Works in Streamlit."""
    try:
        cleaned = clean_text_for_audio(text)
        if not cleaned:
            return None

        # Use a temp file that Streamlit can access
        temp_dir = tempfile.gettempdir()
        output_file = os.path.join(temp_dir, "rocen_pronunciation.mp3")

        # Run edge_tts synchronously using its CLI-style interface
        # This avoids the asyncio event loop conflict with Streamlit
        import subprocess
        import sys

        result = subprocess.run(
            [
                sys.executable, "-m", "edge_tts",
                "--voice", voice,
                "--text", cleaned,
                "--write-media", output_file,
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

        if result.returncode == 0 and os.path.exists(output_file):
            return output_file
        else:
            # Fallback: try async method with nest_asyncio
            return _generate_voice_async(cleaned, voice)

    except Exception as e:
        print(f"TTS Error: {e}")
        # Try async fallback
        try:
            return _generate_voice_async(cleaned, voice)
        except Exception as e2:
            print(f"TTS Async Fallback Error: {e2}")
            return None


def _generate_voice_async(text, voice="en-GB-SoniaNeural"):
    """Fallback async method using nest_asyncio."""
    try:
        import nest_asyncio
        nest_asyncio.apply()
    except ImportError:
        pass

    import asyncio

    async def _speak(t, v, filename):
        communicate = edge_tts.Communicate(t, v)
        await communicate.save(filename)
        return filename

    temp_dir = tempfile.gettempdir()
    output_file = os.path.join(temp_dir, "rocen_pronunciation.mp3")

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're inside Streamlit's loop, create a new one
            import threading
            result = [None]
            def run_in_thread():
                new_loop = asyncio.new_event_loop()
                result[0] = new_loop.run_until_complete(_speak(text, voice, output_file))
                new_loop.close()
            t = threading.Thread(target=run_in_thread)
            t.start()
            t.join(timeout=15)
            if result[0] and os.path.exists(output_file):
                return output_file
        else:
            loop.run_until_complete(_speak(text, voice, output_file))
            if os.path.exists(output_file):
                return output_file
    except Exception as e:
        print(f"Async TTS Error: {e}")

    return None


def is_tts_available():
    """Check if TTS is working."""
    try:
        result = generate_voice("test")
        return result is not None
    except:
        return False
