import json
import os

from groq import Groq

from core.validator import validate_result
from schemas.document_schema import DocumentResult


class DocumentAgent:
    """LLM extraction agent with validation and one controlled retry."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing. Add it to .env.")

        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    def extract_information(self, context: str) -> dict:
        schema = DocumentResult.model_json_schema()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a document extraction agent. "
                        "Use only facts present in the supplied context. "
                        "Do not invent information. Return only structured JSON "
                        "matching the provided schema."
                    ),
                },
                {
                    "role": "user",
                    "content": f"""
Extract reliable information from this document context.

DOCUMENT CONTEXT:
{context}

Return:
- document title
- document type
- concise summary
- key information
- important entities
- dates
- confidence from 0 to 1
""",
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "document_result",
                    "strict": True,
                    "schema": schema,
                },
            },
            temperature=0,
        )

        return json.loads(response.choices[0].message.content)

    def process(self, context: str) -> dict:
        data = self.extract_information(context)
        valid, result, error = validate_result(data)

        if valid:
            return {"status": "valid", "result": result, "error": None, "attempts": 1}

        retry_context = f"""
The first extraction did not pass Pydantic validation.

Validation feedback:
{error}

Re-process the original context carefully and return corrected structured data.

ORIGINAL CONTEXT:
{context}
"""
        data = self.extract_information(retry_context)
        valid, result, error = validate_result(data)

        if valid:
            return {"status": "valid", "result": result, "error": None, "attempts": 2}

        return {"status": "invalid", "result": None, "error": error, "attempts": 2}
