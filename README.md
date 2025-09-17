# CompactaImagem

CompactaImagem é uma ferramenta simples para comprimir e otimizar imagens (JPEG, PNG, HEIC) com uma interface gráfica amigável construída em `customtkinter`.

## Objetivo
O projeto tem como objetivo permitir que usuários reduzam o tamanho de imagens rapidamente sem a necessidade de conhecimento técnico. É ideal para reduzir espaço em disco ou preparar imagens para envio na web.

## Recursos
- Interface gráfica com tema escuro (`customtkinter`).
- Seleção múltipla de arquivos (JPG, JPEG, PNG, HEIC).
- Slider de compressão (1 a 10 — 10 = maior compressão).
- Barra de progresso e previsão de tempo durante o processamento.
- Saída em pasta `comprimidas` ao lado dos arquivos originais.

## Como usar (Windows / PowerShell)

### 1) Criar e ativar um ambiente virtual (recomendado)

Abra o PowerShell no diretório do projeto e execute:

```powershell
# Cria o ambiente virtual (apenas uma vez)
python -m venv .\venv

# Ativa o ambiente virtual (PowerShell)
.\venv\Scripts\Activate
```

Após a ativação o prompt deve exibir `(venv)` no início.

### 2) Instalar dependências a partir do `requirements.txt`

Com o ambiente virtual ativado, rode:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Executar o programa

Com o ambiente ativo e dependências instaladas:

```powershell
python compressor.py
```

### 4) Usar a interface

- Clique em `Selecionar Imagens` e escolha os arquivos (JPG, JPEG, PNG, HEIC).
- Ajuste o slider para escolher o nível de compressão (1-10).
- Clique em `Comprimir` para iniciar.
- As imagens comprimidas serão salvas na pasta `comprimidas`.

## Observações e recomendações
- Para HEIC é utilizada a biblioteca `pillow-heif` (converte HEIC para JPG antes de comprimir).
- Para PNG o compressão é feita com Pillow convertendo para modo paletizado (`P`) para reduzir tamanho sem dependência de binários externos.
- Se desejar compressão PNG ainda mais agressiva, instale `optipng` e eu posso reativar essa opção (requer instalação do executável no Windows).

## Licença
Projeto livre para uso pessoal e estudos.

----

Se quiser que eu ajuste o nome do projeto ou adicione um `logo`/icones, posso incluir também um `LICENSE` e `CONTRIBUTING.md` simples.
