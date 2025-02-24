from llama_index.readers.web import SimpleWebPageReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.readers.file import PyMuPDFReader
from llama_index.core import SummaryIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.embed_model = HuggingFaceEmbedding(
	model_name="BAAI/bge-small-en-v1.5"
)

Settings.chunk_size = 1024
Settings.chunk_overlap = 50


loader = PyMuPDFReader()
# d1 = loader.load(file_path="./ndn-context.txt")

d2 = SimpleWebPageReader(html_to_text=True).load_data([ "https://named-data.github.io/StateVectorSync/Specification.html" ])

documents = [d2]

index = SummaryIndex.from_documents(documents)

retriever = index.as_retriever()
response = retriever.retrieve("A function in C that is able to complete the state vector updated based on a received message.")


context = " ".join([node.dict()['node']['text'] for node in response])
print(context)
