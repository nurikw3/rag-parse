import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="prompt_engineering",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

bs4_strainer = bs4.SoupStrainer(class_=('post-title', 'post-header', 'post-content'))
loader = WebBaseLoader(
    web_path=("https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",),
    bs_kwargs={'parse_only':bs4_strainer},
)

docs = loader.load()
print(f'Total ch: {len(docs[0].page_content)}')

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,add_start_index=True)
all_splits = text_splitter.split_documents(docs)
print(f'Total splitsL {len(all_splits)}')

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="prompt_engineering",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

ids = vector_store.add_documents(all_splits)
print(f'Total vectors: {len(ids)}')