from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal
from ingestion import retriever

llm = ChatOpenAI(temperature=0)

class GradeDocument(BaseModel):
    """
    Binary score for relevance check on retrieved documents.
    """
    binary_score: str = Field(
        description="Documents are relevant to the question. 'yes' or 'no'.",
    )

structured_llm_grader = llm.with_structured_output(GradeDocument)

system_prompt = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Retrieved document: {document} User question: {question} ")
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader


if __name__ == "__main__":
    user_question = "what is prompt engineering?"
    docs = retriever.get_relevant_documents(user_question)
    retrieved_document = docs[0].page_content
    print(retrieval_grader.invoke(
        {"question": user_question, "document": retrieved_document}
    ))
