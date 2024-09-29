import ast
from typing import Sequence

from image_summary import generate_img_summaries
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from multi_retriever import create_multi_vector_retriever
from prompter import get_promp_holder
from text_retriever import get_chunks
from typing_extensions import Annotated, TypedDict

llm = ChatOpenAI(model_name="gpt-4o")
source = "https://web.stanford.edu/class/archive/cs/cs161/cs161.1168/lecture1.pdf"

vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
chunks = get_chunks()
_, image_summaries = generate_img_summaries("images")
retriever = create_multi_vector_retriever(vectorstore, chunks, source, image_summaries)
prompt = get_promp_holder()
history_aware_retriever = create_history_aware_retriever(llm, retriever, prompt)


system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


class State(TypedDict):
    input: str
    chat_history: Annotated[Sequence[BaseMessage], add_messages]
    context: str
    answer: str


# We then define a simple node that runs the `rag_chain`.
# The `return` values of the node update the graph state, so here we just
# update the chat history with the input message and response.
def call_model(state: State):
    response = rag_chain.invoke(state)
    return {
        "chat_history": [
            HumanMessage(state["input"]),
            AIMessage(response["answer"]),
        ],
        "context": response["context"],
        "answer": response["answer"],
    }


# Our graph consists only of one node:
workflow = StateGraph(state_schema=State)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Finally, we compile the graph with a checkpointer object.
# This persists the state, in this case in memory.
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


config = {"configurable": {"thread_id": "abc123"}}

# result = app.invoke(
#     {"input": "What is the first step of insertion sort algorithm?"},
#     config=config,
# )
# print(result["answer"])


# result = app.invoke(
#     {"input": "What is next step?"},
#     config=config,
# )
# print(result["answer"])


# result = app.invoke(
#     {"input": "What is the computational complexity?"},
#     config=config,
# )
# print(result["answer"])


result = app.invoke(
    {
        "input": "What are the steps of the surgical plan? Give it in a list of dictionaries format, with two keys, title and description, with the title being the key part of the step, and the description having any additional details. The output should be parseable by the ast literal_eval command. Give me a single line output without a newline "
    },
    config=config,
)
print(result["answer"][:100])


ans = result["answer"]


l = ast.literal_eval(ans)

print(type(l))
print(l[0])
