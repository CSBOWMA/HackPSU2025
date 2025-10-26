**Request Schema**

Must send a json object that matches *QueryRequest* Pydantic model
- Field: question
- Type: string
- Desciption: The user's query for the RAG system.
- Example Value:"What is the TA's email and what is due next week?"

{
  "question": "What example or code he used to explain Mini batch Gradient descent ?"
}

**Response Schema ( what the UI receives)**

The API will return a single JSON object that matches the RAGResponse Pydantic model:
- Field: answer
- Type: string
- Description: The complete, synthesized answer, including the Relevant Code block.
- Example Value: "The formula for the slope derivative is: (-2/batch_size) * np.sum(Xi * (yi - y_pred))..."
- Field: sources
- Type: array of strings
- Description: A list of the unique source documents used to ground the answer.
- Example Value: ["06.ipynb", "PSU_Syllabus_IA651_Spring_2025.pdf"]


{
  "answer": "The instructor explains Mini-Batch Gradient Descent conceptually by stating that... \n\nRelevant Code:\n```python\ndef gradient_descent(X, y, slope, intercept, ...)\n    ...\n```\n",
  "sources": [
    "06.ipynb"
  ]
}

**Endpoint Details**
- Method: POST
- Path: /query-rag 
- Purpose: Runs the vector search (retriever), formats the prompt with the retrieved context, and generates the final, source-aware answer using the Gemini model.
