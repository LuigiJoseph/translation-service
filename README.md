<!--
Hey, thanks for using the awesome-readme-template template.  
If you have any enhancements, then fork this project and create a pull request 
or just open an issue with the label "enhancement".

Don't forget to give this project a star for additional support ;)
Maybe you can mention me or this repo in the acknowledgements too
-->

<br />

<!-- Table of Contents -->
# Table of Contents

- [About the Project](#about-the-project)
  * [Screenshot](#screenshot)
  * [Tech Stack](#Tech-Stack)
- [Getting Started](#getting-started)
  * [Running Tests](#running-tests)
- [Models Used](#models-used)
  
<!-- About the Project -->
## About the Project


<!-- Screenshots -->
### Screenshot

![Alt text](/Screenshots/projectUI.png?raw=true "Project UI")


<!-- TechStack -->
### Tech Stack

- **Backend**: [Flask](https://flask.palletsprojects.com/)
- **Frontend**: [React.js](https://reactjs.org/)
- **Database**: [MongoDB](https://www.mongodb.com/)
- **DevOps**: [Docker](https://www.docker.com/)


<!-- Getting Started -->
## Getting Started
Follow the steps below to set up the project

- Clone the project

```bash
  git clone https://github.com/LuigiJoseph/translation-service.git
```

- Go to the project directory

```bash
  cd translation-service
```

- Launch the services with Docker Compose

```bash
  docker-compose up
```

<!-- Running Tests -->
## Running Tests

- Backend tests can be run using the following command

```bash
  pytest --cov
```

<br>

<details>
<summary> <strong>🚀 Launch the services locally</strong> </summary> 

## For Flask

* Install Dependencies

```bash
   pip install -r requirements.txt
```

*  Set Up Environment Variables
 make sure to update the MongoDB connection URL in the environment variables or configuration file. Replace the Docker service name with `localhost` or the appropriate local MongoDB address.

Example :

``` yaml
 mongodb://localhost:27017/
```

* Start the server by running:

```bash
  python -m python_services.sync.app
```
## For Kafka 

** Note: Kafka requires Docker to be running, and its containers must be started using `docker-compose up -d` **
* Install Dependencies

```bash
   pip install -r requirements.txt
```
* Start the consumer by running:
```bash
  python -m python_services.Kafka.consumer
```
* In a separate terminal, and run the following command

```bash
  python -m python_services.Kafka.producer
```

## For React 


* Install Dependencies

```bash
   npm install
```
* Run the react server by executing the following command:
```bash
  npm run dev
```

</details>

<!-- Usage -->
## Models used 
In this project two types of models are used for translation:

### 1. Transformers Models
We use the following pre-trained models from the Hugging Face library for translation tasks:

1. **[Helsinki-NLP/opus-mt-tc-big-en-ar](https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-ar)**: English to Arabic.
2. **[Turkish-to-English-ft](https://huggingface.co/LuigiJoseph/Turkish-to-English-ft)**: Turkish to English.
3. **[English-to-Turkish-ft](https://huggingface.co/LuigiJoseph/English-to-Turkish-ft)**: English to Turkish.
4. **[LuigiJoseph/Helsinki-ar-en-ft](https://huggingface.co/LuigiJoseph/Helsinki-ar-en-ft)**: Arabic to English.

### 2. Qwen Model
We also use **[qwen2.5:1.5b-instruct](https://ollama.com/library/qwen2.5:1.5b-instruct)** to simplify the translation process across a wide range of languages  



