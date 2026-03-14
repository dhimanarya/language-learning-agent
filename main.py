import os, asyncio
from typing import Literal
import ollama
from attr.converters import optional
from typing_extensions import TypedDict, Annotated, Optional
from langchain.messages import AnyMessage,AIMessage, SystemMessage, HumanMessage
from langgraph.graph import add_messages, MessagesState
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from agent.tools import get_n_random_words, get_random_words_with_difficulty_levels, translate_words
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_mcp_adapters.client import   MultiServerMCPClient

load_dotenv()

CLANKI_JS=r"C:\Aryan\PythonProject\clanki\build\index.js"

class AgentState(MessagesState):
    source_language: Optional[str]
    number_of_words: Optional [int]
    model_choice: Literal['ollama', 'gemini'] = 'ollama'
    difficulty_level: Optional[str]
    target_language: Optional[str]
        # Optional[Literal['beginners', 'intermediates', 'advanced']]

local_tools= [
    get_n_random_words,
    get_random_words_with_difficulty_levels,
    translate_words,
]
async def setup_tools ():
    client= MultiServerMCPClient(
        {
            "clanki": {
            "command": "node",
            "args": [CLANKI_JS],
            "transport":'stdio'
        }
                }

    )
    mcp_tools= await client.get_tools()
    return [*local_tools, *mcp_tools]

def assistant(state:AgentState):
    #tools description for agentu
    textual_description_of_the_tools='''
def get_n_random_words(language: str,
                       n: int, ) -> list:
    Selects a specified number of random words from a language-specific word list.
The function reads a JSON file containing words for the specified language from
a predefined directory. It then selects 'n' random words from the file and
returns them in a list.
    :param language:A string representing the language for which to fetch the word list.
    :param n: An integer specifying the number of random words to retrieve.
    :return:A list containing 'n' randomly selected words.
  def get_random_words_with_difficulty_levels(
        language: str,
        difficulty_level: str,
        n: int,
) -> list:
        Selects a specified number of random words from a language-specific word list based on a difficulty level.

        The function reads a JSON file containing words for the specified language from
        a predefined directory. It then selects `n` random words from the file based on difficulty level selected
        and returns them in a list. Posssible difficulty levels are: "beginners", "intermediates" and "advanced".

        :param language: A string representing the language for which to fetch the word list.
        :param difficulty_level: A string representing the difficulty level for which to fetch
        :param n: An integer specifying the number of random words to retrieve.
        :return: A list containing `n` randomly selected words.
def translate_words(random_words: list,
                    source_language: str,
                    target_language: str) -> dict:
    """
    Translates a list of words from a source language to a target language using
    a language model. The method ensures output is in the expected JSON format,
    containing translations corresponding to the provided input words.

    :param random_words: A list of words to be translated.
    :param source_language: The language of the input words.
    :param target_language: The language to translate the words into.
    :return: A dictionary containing the translations with the structure:
             {"translations": [{"source": "<original>", "target": "<translated>"}, ...]}.
    
    '''
    system_msg = SystemMessage(content=f'''
You are a helpful language learning assistant that keep things to the point ans very short. you have access to following tools {textual_description_of_the_tools}
 The user is going to give you a command
Your job is to check:
1. Which source language the user wants words from.
2. How many words they want.
3. whether user want a word of specific difficulty level or just random words
4. whether they want to translate these words translated into a target language
5. Whether they want to add these words to an Anki deck. Make sure the 'create-deck' toot is called before •create-card' . 

Here are some example workflows:
input: Get 20 random words in Spanish.
source language: Spanish
number of words: 20
input: Get 10 hard words in German.
source language: German
number of words: 10
word difficulty: advanced

input: Get 15 easy words from English language and translate them into Spanish.
source language: English
number of words: 15
word difficulty: beginner
target language : spanish

 input: Get 20 easy words in Spanish, translate them to English, and create a new Anki deck with them called Spanish::Easy
        source language: Spanish
        target language: English
        number of words: 20
        word difficulty: beginner
        tools workflow: get_n_random_words_by_difficulty_level -> translate_words -> mcp_tools::create_deck -> mcp_tools::create_card

        input: Get 10 random words in German, and create a new Anki deck with them called German::Words
        source language: German
        number of words: 10
        tools workflow: get_n_random_words -> mcp_tools::create_deck -> mcp_tools::create_card
''')
# int agent
    all_tools = assistant.tools  # ← use all tools set in build_graph()

    model_choice = state.get('model_choice', 'ollama')
    if model_choice == 'gemini':
        llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', api_key=os.getenv('google_api_key'))
    else:
        llm = ChatOllama(model='qwen3:4b')

    llm_w_tools = llm.bind_tools(all_tools)

    return {
        'messages': [llm_w_tools.invoke([system_msg] + state['messages'])],
        'source_language': state['source_language'],
        'number_of_words': state['number_of_words'],
        'model_choice': model_choice,
        'difficulty_level': state['difficulty_level'],
        'target_language': state['target_language'],
    }
# bulder graph fun
async  def build_graph():
    ''' Build the state graph with properly initialized tools.'''
    tools= await setup_tools() #pre calling tools
    assistant.tools = tools  #assigning tools to our assitatnt
    builder =StateGraph(AgentState)
    builder.add_node('assistant', assistant)
    builder.add_node('tools', ToolNode(tools))

    builder.add_edge(START, 'assistant')
    builder.add_conditional_edges('assistant', tools_condition)
    builder.add_edge('tools', 'assistant')
    return builder.compile()

async def main(model_choice:Literal['gemini', 'ollama']='ollama'):
    '''Main async function to run the application.'''
    react_agent= await build_graph()
    user_prompt =input('enter the human message and difficulty level:\n')
    messages=[HumanMessage(content=user_prompt)]
    result = await react_agent.ainvoke({
        'messages': messages,
        'source_language': None,
        'model_choice': model_choice,
        'number_of_words': None,
        'difficulty_level': None,
        'target_language':None
})
    print(f'final messsages: {result["messages"][-1].content}')
if __name__ == '__main__':
    asyncio.run(main('gemini'))