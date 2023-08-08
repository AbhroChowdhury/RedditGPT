from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

# Set the environment variable
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ".credentials/credentials.json"

# Now you can initialize GoogleDriveLoader
folder_id = '1UkHcjOJUzoFtPX0m1sysFVad5nbHSP4h'
loader = GoogleDriveLoader(
    folder_id=folder_id,
    recursive=False,
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000, chunk_overlap=200, separators=[" ", ",", "\n"]
    )

texts = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(texts, embeddings)
retriever = db.as_retriever()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

while True:
    query = input("> ")
    answer = qa.run(query)
    print(answer)