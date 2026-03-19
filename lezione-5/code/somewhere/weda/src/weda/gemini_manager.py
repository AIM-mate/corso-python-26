from google import genai

class GeminiManager:
    # Class attribute: The shared client instance
    client = genai.Client()

    @classmethod
    def run_prompt(cls, prompt: str):
        # https://ai.google.dev/gemini-api/docs/models?hl=it
        # gemini-3-flash-preview
        # gemini-2.5-flash
        # gemini-2.5-flash-lite
        model = "gemini-2.5-flash-lite"
        print(f"Calling model: {model}")
        response = cls.client.models.generate_content(
            model=model, contents=prompt
        )
        return response.text
