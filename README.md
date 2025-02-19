# End-to-End-Medical-Chatbot

# How to run?
### Steps?

Clone the repository

<!-- ```bash
Project repo : https://github.com/
``` -->

### STEP 01 - Create a conda environment after opening the repository

```bash
conda create -n medibot python = 3.10 -y
```

```bash
conda activate medibot
```

### STEP 02 - install the requirements

```bash
pip install -r requirements.txt
```

### Create a `.env` file in the root directory and add your pinecone & cohere api key credentials as follows:

```ini
PINECONE_API_KEY = "xxxxx"
COHERE_API_KEY = "xxxx"
```

```bash
# run the following command to store embeddings to pinecone
python store_index.py
```

```bash
# Finally run the following command
python app.py
```


Now, 
```bash
open up localhost:
```

### Techstack Used:

- Python
- Langchain
- Cohere 
- Flask
- Pinecone
