from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from termcolor import colored  # Adiciona cor ao texto
from fpdf import FPDF  # Para gerar PDF

# Desativar notação científica para maior clareza
np.set_printoptions(suppress=True)

# Carregar o modelo
model = load_model("keras_Model.h5", compile=False)

# Carregar os labels
class_names = ["Rachadura", "Infiltração", "Carbonatação"]  # Usei as patologias mencionadas

# Criar array no formato correto para alimentar o modelo keras
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Substitua isto pelo caminho da sua imagem
image = Image.open("<IMAGE_PATH>").convert("RGB")

# Redimensionar a imagem para 224x224 e cortar do centro
size = (224, 224)
image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

# Converter a imagem para array numpy
image_array = np.asarray(image)

# Normalizar a imagem
normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

# Carregar a imagem no array
data[0] = normalized_image_array

# Realizar predição
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]

# Exibir predição e grau de periculosidade
danger_level = confidence_score * 100  # Grau de periculosidade em %
print(colored(f"Patologia: {class_name.strip()}", 'green'))
print(f"Grau de Periculosidade: {danger_level:.2f}%")

# Função para criar o relatório em PDF
def create_pdf(class_name, danger_level):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 128, 0)  # Verde
    
    pdf.cell(200, 10, txt=f"Relatório de Patologia: {class_name.strip()}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_text_color(0, 0, 0)  # Preto
    pdf.cell(200, 10, txt=f"Grau de Periculosidade: {danger_level:.2f}%", ln=True)
    
    # Adicionar mais informações sobre a patologia e soluções específicas
    pdf.ln(10)
    if class_name.strip() == "Rachadura":
        pdf.multi_cell(0, 10, txt="A rachadura é uma abertura ou fissura em uma estrutura. Soluções incluem o reforço da área afetada ou reparo com materiais especiais.")
    elif class_name.strip() == "Infiltração":
        pdf.multi_cell(0, 10, txt="A infiltração indica a presença de água ou umidade em áreas indesejadas. Soluções podem incluir a impermeabilização ou reparo das áreas afetadas.")
    elif class_name.strip() == "Carbonatação":
        pdf.multi_cell(0, 10, txt="A carbonatação é a reação do CO2 com o concreto, afetando a durabilidade. Soluções incluem a aplicação de revestimentos protetores ou reparos.")
    
    # Salvar o PDF
    pdf.output("relatorio_patologia.pdf")

# Criar o PDF após a predição
create_pdf(class_name, danger_level)
