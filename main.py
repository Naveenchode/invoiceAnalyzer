from langchain import PromptTemplate
from langchain.chains import LLMChain
import PIL.Image
import google.generativeai as genai
GOOGLE_API_KEY="AIzaSyBAvNAAXJOJ-RU6q1mi5LKUB31zz0b9tow"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro-vision')

input_prompt='''
You are an expert in understanding invoics.we will upload a simple image as invoice and you will have to
answer any question based on the uploaded invoice image
'''
img1 = PIL.Image.open('invoice1.jpg')
input = "invoice date"
response = model.generate_content([input_prompt, img1,input], stream=True)
response.resolve()
print(response.text)