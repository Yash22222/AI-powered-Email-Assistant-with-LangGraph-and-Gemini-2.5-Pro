from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

gemini_2_5_pro_exp = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro-exp-03-25",
)

gemini_2_5_pro_preview = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro-preview-03-25"
)