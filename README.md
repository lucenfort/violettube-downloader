# VioletTube Downloader

VioletTube Downloader é uma aplicação simples para baixar vídeos e áudios do YouTube. Desenvolvido com Flet, Pytube e MoviePy, este aplicativo facilita o download de conteúdo em várias resoluções e formatos.

## Objetivo

O objetivo do VioletTube Downloader é proporcionar uma forma simples e eficiente de baixar vídeos e áudios do YouTube, seja individualmente ou em playlists, com suporte para múltiplas resoluções e formatos de áudio.

## Como Funciona

O VioletTube Downloader utiliza as seguintes bibliotecas:

- **Flet**: Para construção da interface gráfica.
- **Pytube**: Para gerenciamento e download de vídeos e áudios do YouTube.
- **MoviePy**: Para conversão de formatos de áudio.

## Como Usar

### Pré-requisitos

Certifique-se de ter o Python instalado em seu sistema. Recomendamos utilizar um ambiente virtual para gerenciar as dependências.

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/violettube-downloader.git
   cd violettube-downloader
   ```
2. Crie um ambiente virtual:
   - No Windows:
    ```bash
     python -m venv env
    ```
   - No macOS/Linux:
    ```bash
     python3 -m venv env
    ```

3. Ative o ambiente virtual:
   - No Windows:
    ```bash
     .\env\Scripts\activate
    ```
   - No macOS/Linux:
    ```bash
     source env/bin/activate
    ```

4. Instale as dependências:
   ```bash
   pip install flet pytube moviepy
   ```

5. Instale o pipreqs:
   ```bash
   pip install pipreqs
   ```

6. Gere o arquivo `requirements.txt`:
   ```bash
   pipreqs . --force
   ```

### Executando a Aplicação

Para iniciar a aplicação, execute o seguinte comando no terminal:
    
```bash
    python app.py 
```

### Uso

1. Abra o VioletTube Downloader.
2. Insira a URL do vídeo ou playlist do YouTube.
3. Escolha o tipo de download: `Áudio` ou `Vídeo`.
4. Selecione a resolução ou formato desejado.
5. Clique no botão "Baixar" para iniciar o download.
6. Acompanhe o progresso na barra de progresso e verifique o status do download.

---

![image](https://github.com/lucenfort/violettube-downloader/assets/55037889/4cce489c-63fe-4eb5-8299-ae57f3f65d9d)

