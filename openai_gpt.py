import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # You'll insert this later

def generate_comic_book(synopsis):
    openai.api_key = OPENAI_API_KEY

    messages=[
      {
        "role": "system",
        "content": "# My Comic Book\nVocê receberá a sinopse de uma história em quadrinhos.\nSua tarefa é criar essa história, gerando a narração e descrições de imagens para um livro de quadrinhos com até 10 painéis.\n\n1. Crie a história a partir da sinopse\n1.1 A história deve ter classificação indicativa para 10 anos e não deve conter violência, sexo ou referência à drogas\n1.2 A história deve ser envolvente, divertida e emocionante\n2. Divida a história em segmentos menores que serão usados em cada painel do quadrinho.\n3. Escreva a narração para cada painel de forma que complemente as ilustrações que serão geradas. O texto deve seguir as diretrizes:\n3.1. Linguagem Simples\n3.2. Usar emojis para facilitar a compreensão\n3.3. TODAS AS LETRAS EM MAIÚSCULA\n3.4 A narração deve ser criada em Português\n4. Para cada painel, inclua também uma descrição de imagem para ser gerada pelo Stable Diffusion\n4.1 A descrição deve ser criada em inglês\n4.2 As descrições das imagens devem considerar que o Stable Diffusion não tem o contexto geral. Ele vai gerar uma imagem de cada vez, sem conhecimento das anteriores.\n4.3 Evite termos como \"is seen\" ou \"are seen\" nas descrições da imagens. O Stable Diffusion interpreta isso como se houvesse mais personagens na cena.\n4.4 Sempre descreva o cenário de forma consistente entre os painéis.\n4.5 Sempre descreva que o gênero, idade e características dos personagens de forma consistente entre os painéis.\n5. Certifique-se de que a narração e as descrições de imagem fluam bem e façam sentido como uma história em quadrinhos.\n6. Indique claramente onde começa e termina a narração e a descrição de cada painel, para facilitar a montagem posterior.\n6.1 Use \"NARRAÇÃO\" e \"DESCRIÇÃO DE IMAGEM\" de forma consistente em cada painel\n\nResponda apenas com a narração e descrições de imagem formatadas para os painéis."
      },
      {
        "role": "user",
        "content": synopsis  
      }
    ]    

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0,
            max_tokens=4776,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return {"error in generate_comic_book": str(e)}        
      
def create_dalle_images(prompt, n=1, size="512x512"):
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=n,
            size=size
        )
        if response and response.get('data'):
            return [img['url'] for img in response['data']]
        else:
            return {"error in create_dalle_images": "No images generated"}
    except Exception as e:
        return {"error in create_dalle_images": str(e)}