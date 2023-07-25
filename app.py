import os
from fast_dash import fastdash, FastDash, Fastify, dcc
import dash_mantine_components as dmc
from embedchain import App
from embedchain.config import QueryConfig, AddConfig
from string import Template

# Define app configurations
PROMPT = Template(
    """Use the given context to answer the question at the end.
If you don't know the answer, say so, but don't try to make one up.
At the end of the answer, also give the sources as a bulleted list.
Display the answer as markdown text.

Context: $context

Query: $query

Answer:"""
)
query_config = QueryConfig(template=PROMPT)

# Define components
openai_api_key_component = Fastify(
    dmc.PasswordInput(
        placeholder="API Key",
        description="Get yours at https://platform.openai.com/account/api-keys",
    ),
    "value",
)

web_page_urls_component = Fastify(
    dmc.MultiSelect(
        description="Include all the reference Web URLs",
        placeholder="Enter URLs separated by commas",
        searchable=True,
        creatable=True,
    ),
    "data",
)

text_component = Fastify(
    dmc.Textarea(placeholder="Write your query here", autosize=True, minRows=4), "value"
)

answer_component = Fastify(dcc.Markdown(style={"text-align": "left", "padding": "1%"}), "children")


# Define the callback function
def explore_your_knowledge_base(
    openai_api_key: openai_api_key_component,
    web_page_urls: web_page_urls_component,
    youtube_urls: web_page_urls_component,
    pdf_urls: web_page_urls_component,
    text: text_component,
    query: text_component,
) -> answer_component:
    """
    Input your sources and let GPT3.5 find answers. Built with Fast Dash.
    This app uses embedchain.ai, which abstracts the entire process of loading and chunking datasets, creating embeddings, and storing them in a vector database.
    Embedchain itself uses Langchain and OpenAI's ChatGPT API.
    """
    os.environ["OPENAI_API_KEY"] = openai_api_key
    app = App()

    if web_page_urls:
        [app.add("web_page", url["value"]) for url in web_page_urls]

    if youtube_urls:
        [app.add("youtube_video", url["value"]) for url in youtube_urls]

    if pdf_urls:
        [app.add("pdf_file", url["value"]) for url in pdf_urls]

    if text:
        app.add_local("text", text)

    answer = app.chat(query, query_config)

    return answer

# Build app (this is all it takes!). Fast Dash understands what it needs to do. 
app = FastDash(explore_your_knowledge_base)
server = app.server

if __name__ == "__main__":
    app.run()