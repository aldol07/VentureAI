"""
LLM Client - Centralized LangChain + OpenRouter wrapper.
All AI calls go through this module.
Uses OpenRouter API for access to multiple models including DeepSeek.
"""

import os
import json
import re
from typing import Optional
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()


class LLMClient:
    """Centralized client for all LangChain + OpenRouter interactions."""
    
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        # Initialize OpenRouter via LangChain's ChatOpenAI
        self.llm = ChatOpenAI(
            model="deepseek/deepseek-r1",
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.7,
            default_headers={
                "HTTP-Referer": "https://venturepilot.app",
                "X-Title": "VenturePilot AI"
            }
        )
        
        self.str_parser = StrOutputParser()
    
    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7
    ) -> dict:
        """
        Generate a structured JSON response.
        Handles DeepSeek R1's thinking tags and extracts clean JSON.
        """
        # Build the prompt template
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "{system_prompt}\n\nCRITICAL: Respond with valid JSON only. No markdown, no code blocks, no explanations outside the JSON."
            ),
            HumanMessagePromptTemplate.from_template("{user_prompt}")
        ])
        
        # Create the chain with temperature
        llm_with_temp = self.llm.bind(temperature=temperature)
        chain = prompt | llm_with_temp | self.str_parser
        
        # Execute
        result = chain.invoke({
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        })
        
        # Clean and parse JSON
        return self._parse_json(result)
    
    def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate a plain text response."""
        # Build prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("{system_prompt}"),
            HumanMessagePromptTemplate.from_template("{user_prompt}")
        ])
        
        # Create chain with settings
        bind_kwargs = {"temperature": temperature}
        if max_tokens:
            bind_kwargs["max_tokens"] = max_tokens
        
        llm_configured = self.llm.bind(**bind_kwargs)
        chain = prompt | llm_configured | self.str_parser
        
        # Execute
        result = chain.invoke({
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        })
        
        # Clean thinking tags from response
        return self._clean_thinking_tags(result)
    
    def generate_code(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3
    ) -> str:
        """
        Generate code with lower temperature for consistency.
        Cleans up response to return only the code.
        """
        result = self.generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature
        )
        
        # Additional cleaning for code responses
        return self._clean_code_response(result)
    
    def _clean_thinking_tags(self, text: str) -> str:
        """Remove DeepSeek R1's <think>...</think> tags from response."""
        text = text.strip()
        
        # Remove thinking tags
        if "<think>" in text:
            # Find all thinking blocks and remove them
            pattern = r'<think>.*?</think>'
            text = re.sub(pattern, '', text, flags=re.DOTALL)
        
        return text.strip()
    
    def _clean_code_response(self, text: str) -> str:
        """Clean code response by removing markdown blocks."""
        text = self._clean_thinking_tags(text)
        
        # Remove markdown code blocks
        if text.startswith("```"):
            # Find the language identifier line
            first_newline = text.find('\n')
            if first_newline != -1:
                text = text[first_newline + 1:]
        
        if text.endswith("```"):
            text = text[:-3]
        
        return text.strip()
    
    def _parse_json(self, text: str) -> dict:
        """Clean and parse JSON from LLM response."""
        text = text.strip()
        
        # Remove thinking tags first
        text = self._clean_thinking_tags(text)
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        
        # Try to find JSON object in the text
        # Look for the outermost { }
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = text[start_idx:end_idx + 1]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Try parsing the whole text
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # Last resort: try to fix common JSON issues
            fixed_text = self._fix_json(text)
            return json.loads(fixed_text)
    
    def _fix_json(self, text: str) -> str:
        """Attempt to fix common JSON formatting issues."""
        # Remove any trailing commas before } or ]
        text = re.sub(r',\s*}', '}', text)
        text = re.sub(r',\s*]', ']', text)
        
        # Ensure proper quoting of keys
        # This is a simple fix and may not work for all cases
        
        return text


# Singleton instance
_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create the singleton LLM client."""
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
