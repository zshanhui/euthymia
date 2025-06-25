from ast import parse
import logging
import os
from enum import Enum
from re import search
from typing import Optional

from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from llama_index.core import Document, SimpleDirectoryReader
from openai import OpenAI
from mistralai.client import MistralClient

# from mistralai.models.chat_completion import ChatMessage

# from deepseek.api import DeepSeekAPI

'''
build a component that acts as an llm router that conencts with external llm apis, handles and normalized responses that can be used by agents

'''

# make sure to export api keys in env
# OPENAI_EUTH_DEV_API_KEY
# DEEPSEEK_EUTH_DEV_API_KEY
# MISTRAL_EUTH_DEV_API_KEY
# SEALION_EUTH_DEV_API_KEY

DEEPSEEK_URL = ''

@dataclass
class LLMType(Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    MISTRAL = "mistral"
    SEALION = "sealion"

@dataclass
class LocationContext():
    region: str # free text
    country: str # 2 char ISO code (eg. US, SG, CN)
    city: str # free text

@dataclass
class LlmQueryMessage():
    role: str
    content: str
    name: Optional[str] = None

@dataclass
class DeepSeekModel(Enum):
    chat_chat_v3 = 'deepseek-chat'
    reasoning_r1 = 'deepseek-reasoner'

@dataclass
class OaiModel(Enum):
    gpt_41 = 'gpt-4.1'
    gpt_4o_mini = 'gpt-4o-mini'
    gpt_4o_search = 'gpt-4o-search-preview'


@dataclass
class SeaLionModel(Enum):
    '''
    SEA-LION is rate limited to 10rpm
    '''
    # SOT reasoning model, distilled reasoning from deepseek-r1
    sealion_llama_v35_70b_r     = 'aisingapore/Llama-SEA-LION-v3.5-70B-R'
    # smaller reasoning model
    sealion_llama_v35_8b_r     = 'aisingapore/Llama-SEA-LION-v3.5-8B-R'
    # best performing on SEA-HELM benchmark for similar sized sub-10B models
    sealion_gemma_v30_9b_it     = 'aisingapore/Gemma-SEA-LION-v3-9B-IT'
    # based on Llama3.1 (largest model, 128K context length)
    sealion_llama_v30_70b_it    = 'aisingapore/Llama-SEA-LION-v3-70B-IT'


class LlmGateway():

    selected_llm: LLMType = LLMType.DEEPSEEK
    reasoning: bool = True # use reasoning models by default

    oai_client: OpenAI = None
    deepseek_client: OpenAI = None # deepseek compat with OpenAI SDK
    sealion_client: OpenAI = None # sealion is compat with OpenAI SDK
    mistral_client: MistralClient = None

    default_query = 'state the current date and your model version'
    
    # Cost tracking
    _cost_quota: float = 10.0  # Default quota of $100
    _current_usage: float = 0.0  # Tracks current usage in dollars
    _cost_rates = {
        'deepseek-chat': 0.0005,  # $0.0005 per 1K tokens
        'deepseek-reasoner': 0.001,  # $0.001 per 1K tokens
        'gpt-4.1': 0.03,  # $0.03 per 1K tokens input, $0.06 output (simplified)
        'gpt-4o-mini': 0.01,  # Example rate, adjust as needed
        'gpt-4o-search-preview': 0.02,  # Example rate, adjust as needed
        'aisingapore/Llama-SEA-LION-v3.5-70B-R': 0
    }

    def __init__(self, llm: LLMType = LLMType.DEEPSEEK, cost_quota: Optional[float] = None) -> None:
        self.selected_llm = llm
        
        if cost_quota is not None:
            self._cost_quota = cost_quota
            
        if self.selected_llm == LLMType.OPENAI:
            self.oai_client = OpenAI(api_key=os.getenv('OPENAI_EUTH_DEV_API_KEY'))
        if self.selected_llm == LLMType.DEEPSEEK:
            self._init_deepseek_client()
        if self.selected_llm == LLMType.SEALION:
            self._init_sealion_client()


    def _init_deepseek_client(self):
        """Initialize DeepSeek client if not already initialized."""
        if not self.deepseek_client:
            logging.info('setting deepseek client...')
            self.deepseek_client = OpenAI(
                api_key=os.getenv('DEEPSEEK_EUTH_DEV_API_KEY'),
                base_url="https://api.deepseek.com/v1"  # DeepSeek's API endpoint
            )
        else:
            logging.info('deepseek client already initialized')


    def _init_sealion_client(self):
        """Initialize SEA-LION client if not already initialized."""
        if not self.sealion_client:
            logging.info('setting sealion client...')
            self.sealion_client = OpenAI(
                api_key=os.getenv('SEALION_EUTH_DEV_API_KEY'),
                base_url="https://api.sea-lion.ai/v1"
            )
        else:
            logging.info('sealion client already initialized')


    def choose_optimal_model(self) -> LLMType:
        '''
        route user's query into a reasoning model with context and return model choice
        '''
        raise(NotImplementedError)


    def completion(self, message_template: LlmQueryMessage):
        '''
        primary completion wrapper that decides which models to call based on work needs
        '''
        raise(NotImplementedError)


    def log_cost(self, model: str, prompt_tokens: int, completion_tokens: int = 0) -> float:
        '''
        Calculate and log the cost of an LLM query.
        
        Args:
            model: The model used for the completion
            prompt_tokens: Number of tokens in the prompt
            completion_tokens: Number of tokens in the completion
        '''
        if model not in self._cost_rates:
            logging.warning(f"No cost rate found for model: {model}")
            return 0.0
            
        # Calculate cost (simplified - in a real implementation, you'd use the actual pricing model)
        cost = (prompt_tokens + completion_tokens) / 1000 * self._cost_rates[model]
        self._current_usage += cost
        
        # Log if quota exceeded
        if self._current_usage > self._cost_quota:
            logging.warning(
                f"Cost quota exceeded! Current usage: ${self._current_usage:.4f} "
                f"(Quota: ${self._cost_quota:.2f})"
            )
        else:
            logging.info(
                f"Cost: ${cost:.4f} | "
                f"Total usage: ${self._current_usage:.4f}/{self._cost_quota:.2f} "
                f"({(self._current_usage/self._cost_quota*100):.1f}% of quota)"
            )
            
        return cost


    def get_balance(self):
      raise(NotImplementedError)


    def _deepseekv3_completion(self, message: LlmQueryMessage, stream: bool = False):
        return self._deepseek_completion(
            model=DeepSeekModel.chat_chat_v3, message=message, stream=stream)


    def _deepseekr1_completion(self, message: LlmQueryMessage, stream: bool = False):
        return self._deepseek_completion(
            model=DeepSeekModel.reasoning_r1, message=message, stream=stream)


    def _deepseek_completion(self, model: DeepSeekModel, message: LlmQueryMessage, stream: bool = False):
        '''
        Get completion from DeepSeek V3 model.
        
        Args:
            model: deepseek model id string
            message: The message to send to the model
            stream: Whether to stream the response
            
        Returns:
            The completion response
        '''
        try:
            resp = self.deepseek_client.chat.completions.create(
                model=model.value,
                messages=[{
                    "role": message.role or "user",
                    "content": message.content
                }],
                temperature=0.7,
                # max_tokens=2000,
                stream=stream
            )

            if stream:
                return self._handle_streaming_response(resp)
                
            # Log cost for non-streaming responses
            if resp.usage:
                self.log_cost(
                    model=model.value,
                    prompt_tokens=resp.usage.prompt_tokens,
                    completion_tokens=resp.usage.completion_tokens
                )
                
            return self._parse_llm_response(resp)

        except Exception as err:
            logging.error(f"DeepSeek API error: {str(err)}")
            raise(err)


    def _gpt41_completion(self, message: LlmQueryMessage):
        return self._oai_completion('gpt-4.1', message)


    def _gpt4omini_completion(self, message: LlmQueryMessage):
        return self._oai_completion('gpt-4o-mini', message)


    def _sealion_completion(self, model: SeaLionModel, message: LlmQueryMessage):
        if not self.sealion_client:
            raise('SEA-LION client missing')

        completion = self.sealion_client.chat.completions.create(
            model=model.value,
            messages=[
                {
                    "role": message.role or 'user',
                    "content": message.content or self.default_query,
                }
            ]
        )

        # Log cost for SEA-LION completions
        if completion.usage:
            self.log_cost(
                model=model.value,
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens
            )

        return self._parse_llm_response(completion)


    def _oai_completion(self, model: str, message: LlmQueryMessage):
        if not self.oai_client:
            raise('OpenAI client missing')

        completion = self.oai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": message.role or 'user',
                    "content": message.content or self.default_query,
                }
            ]
        )
        
        # Log cost for OpenAI completions
        if completion.usage:
            self.log_cost(
                model=model,
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens
            )

        return self._parse_llm_response(completion)


    def _gpt4o_websearch(self, location: LocationContext, message: LlmQueryMessage):
        '''
        search the web using openai gpt4o web search tool
        '''
        if not self.oai_client:
            raise('OpenAI client missing')

        if location:
            search_opts = {
                'user_location': {
                    'type': 'approximate',
                    'approximate': {
                        'country': location.country,
                        'city': location.city,
                        'region': location.region,
                    }
                }
            }

        completion = self.oai_client.chat.completions.create(
            model="gpt-4o-search-preview",
            web_search_options=search_opts or {},
            messages=[
                {
                    "role": message.role or "user",
                    "content": message.content,
                    "name": message.name or ''
                }
            ],
        )

        return self._parse_llm_response(completion)


    def _parse_llm_response(self, response):
        logging.info('should parse response: ', response)
        return response


    def _handle_streaming_response(self, response_stream):
        try:
            for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as err:
            logging.error(f'error handling streaming response: {str(err)}')
            raise

    def _ocr_parse(self):
        raise(NotImplementedError)


if __name__ == '__main__':
    print('test llms, openai web search tool')
    # test_message = LlmQueryMessage(role='user', content='what are the top 5 coutries with highest gdp/capita? do not include countries with under 5 million population.')

    # client = OpenAI(api_key=os.getenv('OPENAI_EUTH_DEV_API_KEY'))
    # tech_news_query = 'What are 5 interesting local or regional tech industry news story this past week? summarize it like a newsletter that can be sent as an email.'

    # llms = LlmGateway(llm=LLMType.DEEPSEEK)

    # response = llms._deepseek_completion(model=DeepSeekModel.reasoning_r1, message=test_message)
    # print('Full Response: ', response, '\n\n')
    # print(response.choices[0].message.content, '\n\n')
    # print(f'Usage stats: {response.usage}')

    ## test SEA-LION models
    test_message = LlmQueryMessage(role='user',
        content='what are the top 5 major cities in SEA? why are they significant? then rank them by gdp and growth rate.')
    sealionllm = LlmGateway(llm=LLMType.SEALION)
    resp2 = sealionllm._sealion_completion(model=SeaLionModel.sealion_llama_v35_70b_r, message=test_message)
    print('\n\nFull Response: ', resp2, '\n\n')
    print(resp2.choices[0].message.content, '\n\n')
    print(f'Usage stats: {resp2.usage}')

    # TODO: enable and test out streaming
