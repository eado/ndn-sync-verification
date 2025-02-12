from llama_index.readers.web import SimpleWebPageReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core import SummaryIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.embed_model = HuggingFaceEmbedding(
	model_name="BAAI/bge-small-en-v1.5"
)

Settings.chunk_size = 1024
Settings.chunk_overlap = 50

documents = SimpleWebPageReader(html_to_text=True).load_data(
	[
		"https://named-data.github.io/StateVectorSync/Specification.html"
	]
)

index = SummaryIndex.from_documents(documents)

retriever = index.as_retriever()
response = retriever.retrieve("A function in C that is able to complete the state vector updated based on a received message.")


context = " ".join([node.dict()['node']['text'] for node in response])
print(context)
