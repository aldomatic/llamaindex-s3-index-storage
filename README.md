# Llamaindex S3 Index Storage

  

Using [Llamaindex](https://www.llamaindex.ai/) to query an vector index stored in S3. The new [LLM Stack](https://a16z.com/2023/06/20/emerging-architectures-for-llm-applications/). Yay!

  
### How to install a virtual environment using venv

```bash
pip  install  virtualenv
```
To use venv in your project, in your terminal, create a new project folder, cd to the project folder in your terminal, and run the following command:
```bash
mkdir  llamaindex-s3-index-storage
cd  llamaindex-s3-index-storage

python3  -m  venv  env
```

### How to activate the virtual environment

You can then activate your new python virtual environment running the command below.
```bash
source  ./venv/bin/activate
```

### Install python packages

Install the packages the application requires 
```bash
pip install -r requirements.txt
```
### Environment variables
You will need a few secrets for this to work. You will have to rename `.env.dev` to .`env` for them to load into the application
```bash
OPENAI_API_KEY=
AWS_KEY=
AWS_SECRET=
BUCKET=
```
### S3 bucket
You will need to have a public S3 bucket to use as storage for the index/vectors. 
**Note:** I used a pubic bucket i have not tested it with a private one. 
```bash
llamaindex-demo/storage
```

### Running the app
This command will run the [steamlit](https://streamlit.io/) app and open it in a new tab.
```bash
streamlit run app.py
```