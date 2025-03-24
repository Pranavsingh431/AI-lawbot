import os
import json
import traceback
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory

from src.config import Config
from src.logger import logger, log_user_interaction, log_api_request, log_exception
from src.utils import extract_text_from_pdf, format_response
from src.exceptions import (
    APIKeyError, 
    PDFExtractionError, 
    ModelResponseError, 
    DocumentTooLargeError,
    handle_exception
)

# Template for the legal expert model
LEGAL_TEMPLATE = """
Text:{text}
### Instruction for Legal Expert Model:

You are a highly trained legal expert with in-depth knowledge of laws, regulations, and case precedents across multiple jurisdictions. Your task is to:
- **Interpret and analyze legal documents, contracts, and agreements.**
- **Explain complex legal jargon and clauses in simple, easy-to-understand language for a non-legal audience.**
- **Provide expert legal advice, suggest potential risks, identify legal loopholes, and recommend actionable steps.**
- **Understand the nuances of various legal systems including but not limited to civil law, common law, contract law, corporate law, intellectual property law, and criminal law.**
- **Identify critical sections such as indemnity clauses, liability, arbitration, jurisdiction, and termination provisions with detailed explanations.**
- **When a document is uploaded, summarize its key points, highlight risks, and offer practical advice to the user.**
- **When asked a legal question, provide detailed expert advice along with relevant case laws, statutes, or precedents, if applicable.**
- **Answer general questions about law and legal concepts in clear, accessible language.**

---

📚 **Document Analysis Capability:**
- When provided with a legal document or contract, you should:
    - Identify the core objective and key provisions of the document.
    - Summarize in plain language, highlighting important clauses.
    - Point out any risks, obligations, liabilities, and possible ambiguities.
    - Suggest revisions or actions to mitigate legal risks.

---

### ⚖️ **Legal Question Capability:**
- When asked a legal question or problem, you should:
    - Analyze the legal query and determine relevant laws.
    - Provide a step-by-step explanation in simple language.
    - Mention any potential remedies, risks, and solutions.
    - Support the answer with applicable laws, sections, and case precedents.

---

### 🎯 **Response Format:**
- **Summary:** [Brief, easy-to-understand summary]
- **Key Clauses and Risks:** [Bullet points with details, if relevant to the query]
- **Expert Legal Advice:** [Detailed advice with references to laws and cases]
- **Recommended Actions:** [Clear, actionable next steps]

---

### 📝 **Special Instructions:**
- Ensure the response is accurate, concise, and formatted for easy reading.
- Simplify complex legal language to ensure accessibility.
- Where necessary, highlight important legal terms with definitions.
- For general knowledge questions about law, provide clear explanations without unnecessary formality.

---

### ⚡️ **Fallback Behavior:**
- If the document is unclear or incomplete, ask for clarification.
- If the legal query involves a jurisdiction-specific issue, mention the applicable jurisdiction and possible variations.

{chat_history}
Human: {human_input}
AI:
"""

class LegalAdvisorBot:
    def __init__(self):
        """Initialize the Legal Advisor Bot with configuration settings."""
        logger.info("Initializing Legal Advisor Bot")
        
        try:
            # Initialize the LLM
            llm_params = Config.get_llm_params()
            self.llm = GoogleGenerativeAI(**llm_params)
            
            # Setup memory based on configuration
            memory_params = Config.get_memory_params()
            if Config.MEMORY_TYPE == "conversation_buffer_window":
                self.memory = ConversationBufferWindowMemory(**memory_params)
            else:
                self.memory = ConversationBufferMemory(**memory_params)
            
            # Setup prompt template
            self.prompt = PromptTemplate(
                input_variables=["text", "chat_history", "human_input"],
                template=LEGAL_TEMPLATE
            )
            
            # Create LLM chain
            self.chain = LLMChain(
                llm=self.llm,
                prompt=self.prompt,
                memory=self.memory,
                verbose=Config.DEBUG_MODE
            )
            
            logger.info("Legal Advisor Bot initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Legal Advisor Bot: {e}")
            raise APIKeyError("Failed to initialize the Legal Advisor Bot") from e
    
    def process_query(self, query, pdf_path=None):
        """
        Process a legal query with or without an accompanying document.
        
        Args:
            query (str): User's legal question
            pdf_path (str, optional): Path to PDF document to analyze
            
        Returns:
            str: Response from the legal advisor
        """
        try:
            # If a PDF is provided, extract its text and include it in the query
            if pdf_path:
                logger.info(f"Processing query with document: {pdf_path}")
                
                # Check file size
                file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
                if file_size_mb > Config.MAX_PDF_SIZE_MB:
                    logger.warning(f"Document too large: {file_size_mb:.2f}MB")
                    raise DocumentTooLargeError(f"Document exceeds the maximum size of {Config.MAX_PDF_SIZE_MB}MB")
                
                # Extract PDF text
                pdf_text = extract_text_from_pdf(pdf_path)
                if not pdf_text:
                    logger.error("Failed to extract text from PDF")
                    raise PDFExtractionError("Could not extract text from the provided PDF")
                
                # Combine the query with the extracted text
                input_text = f"Document Analysis Request: {query}\n\nDocument Content:\n{pdf_text}"
                
            else:
                logger.info(f"Processing general legal query")
                input_text = f"Legal Question: {query}"
            
            # Log the API request
            log_api_request("llm_chain", {"query": query, "has_document": pdf_path is not None}, True)
            
            # Get response from the chain
            response = self.chain.invoke({
                "text": input_text,
                "human_input": query
            })
            
            # Format the response
            formatted_response = format_response(response)
            
            # Log the user interaction
            document_name = os.path.basename(pdf_path) if pdf_path else None
            log_user_interaction(query, len(formatted_response), document_name)
            
            return formatted_response
        
        except (APIKeyError, PDFExtractionError, DocumentTooLargeError) as e:
            # Handle known exceptions
            return handle_exception(e)
        except Exception as e:
            # Handle unexpected exceptions
            log_exception(e, context="process_query")
            return handle_exception(e, "Failed to process your query")
    
    def get_response(self, query):
        """
        Process a user query and get a response.
        
        Args:
            query (str): User's legal question
            
        Returns:
            str: Response from the legal advisor
        """
        logger.info(f"Getting response for query: {query[:50]}...")
        return self.process_query(query)
    
    def analyze_document(self, pdf_path):
        """
        Analyze a legal document and provide a summary.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Analysis of the legal document
        """
        try:
            logger.info(f"Analyzing document: {pdf_path}")
            
            # Check if file exists
            if not os.path.exists(pdf_path):
                logger.error(f"Document not found: {pdf_path}")
                return "Error: Document not found."
            
            # Process the document with a standard analysis query
            query = "Please analyze this legal document and provide a comprehensive summary."
            return self.process_query(query, pdf_path)
        
        except Exception as e:
            return handle_exception(e, "Failed to analyze document")
    
    def reset_conversation(self):
        """Reset the conversation memory"""
        logger.info("Resetting conversation memory")
        self.memory.clear()

# Interactive chat function for testing
def interactive_chat():
    """Simple interactive console chat for testing the legal advisor bot"""
    logger.info("Starting interactive chat")
    
    try:
        bot = LegalAdvisorBot()
        
        print("\n===== INTERACTIVE LEGAL ADVISOR CHAT =====")
        print("Type 'exit' to end the conversation.")
        print("Type 'reset' to clear conversation history.")
        print("Type 'analyze: [pdf_path]' to analyze a document.\n")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() == 'exit':
                print("Ending conversation.")
                logger.info("Interactive chat ended by user")
                break
                
            if user_input.lower() == 'reset':
                bot.reset_conversation()
                print("Conversation history cleared.")
                continue
            
            # Check if the user wants to analyze a document
            if user_input.lower().startswith('analyze:'):
                pdf_path = user_input[8:].strip()
                if os.path.exists(pdf_path):
                    print(f"Analyzing document: {pdf_path}")
                    response = bot.analyze_document(pdf_path)
                else:
                    response = f"Error: File not found at {pdf_path}"
            else:
                response = bot.process_query(user_input)
            
            print(f"\nLegal Advisor: {response}\n")
    
    except Exception as e:
        error_message = handle_exception(e, "Failed to run interactive chat")
        print(f"Error: {error_message}")
        logger.error(f"Interactive chat terminated due to error: {e}")

if __name__ == "__main__":
    interactive_chat() 