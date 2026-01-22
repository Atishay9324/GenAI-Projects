"""Base agent class for all AI agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ..config import OPENAI_API_KEY, OPENAI_MODEL


class BaseAgent(ABC):
    """Abstract base class for all AI agents."""

    def __init__(self, temperature: float = 0.7):
        """Initialize the agent with LLM configuration.
        
        Args:
            temperature: Creativity level for the LLM (0.0-1.0)
        """
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=OPENAI_MODEL,
            temperature=temperature
        )
        self.output_parser = StrOutputParser()

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the agent's name."""
        pass

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the agent's system prompt."""
        pass

    def create_chain(self, human_template: str):
        """Create a LangChain chain with the given human template.
        
        Args:
            human_template: The template for human messages
            
        Returns:
            A runnable chain
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", human_template)
        ])
        return prompt | self.llm | self.output_parser

    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the agent's main task.
        
        Args:
            **kwargs: Agent-specific parameters
            
        Returns:
            Dictionary containing the agent's output
        """
        pass
