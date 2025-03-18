<!--
Hey, thanks for using the awesome-readme-template template.  
If you have any enhancements, then fork this project and create a pull request 
or just open an issue with the label "enhancement".

Don't forget to give this project a star for additional support ;)
Maybe you can mention me or this repo in the acknowledgements too
-->
<div align="center">
  
  
   
<h4>
    <a href="https://github.com/Louis3797/awesome-readme-template/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/Louis3797/awesome-readme-template">Documentation</a>
  <span> · </span>
    <a href="https://github.com/Louis3797/awesome-readme-template/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/Louis3797/awesome-readme-template/issues/">Request Feature</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->
# Table of Contents

- [About the Project](#about-the-project)
  * [Screenshots](#screenshots)
  * [Tech Stack](#tech-stack)
  * [Features](#features)
- [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Running Tests](#running-tests)
  * [Setup](#Setup)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Acknowledgements](#acknowledgements)
  

<!-- About the Project -->
## About the Project


<!-- Screenshots -->
### Screenshots

<div align="center"> 
  <img src="https://placehold.co/600x400?text=Your+Screenshot+here" alt="screenshot" />
</div>


<!-- TechStack -->
### Tech Stack

<details>
  <summary>Client</summary>
  <ul>
    <li><a href="https://reactjs.org/">React.js</a></li>
  </ul>
</details>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="https://flask.palletsprojects.com/en/stable/">Flask</a>![Flask]</li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://www.mongodb.com/">MongoDB</a></li>
  </ul>
</details>

<details>
<summary>DevOps</summary>
  <ul>
    <li><a href="https://www.docker.com/">Docker</a></li>
  </ul>
</details>

<!-- Features -->
### Features

- Feature 1
- Feature 2
- Feature 3

<!-- Getting Started -->
## Getting Started

<!-- Prerequisites -->
### Prerequisites

This project uses Yarn as package manager

```bash
 
```

<!-- Installation -->
### Installation

Install my-project with npm

```bash
  
```
   
<!-- Running Tests -->
### Running Tests

To run tests, run the following command

```bash
  pytest --cov
```

<!-- Setup -->
### Setup

Clone the project

```bash
  git clone https://github.com/LuigiJoseph/translation-service.git
```

Go to the project directory

```bash
  cd translation-service
```

Launch the services with Docker Compose

```bash
  docker-compose up
```
Note

<details>
<summary> Launch the services locally </summary> 

## For Flask

### Install Dependencies

```bash
   pip install -r requirements.txt
```

### Set Up Environment Variables
 make sure to update the MongoDB connection URL in the environment variables or configuration file. Replace the Docker service name with `localhost` or the appropriate local MongoDB address.

Example 

``` yaml
 mongodb://localhost:27017/
```

Start the server by running:

```bash
  python -m python_services.sync.app
```
## For Kafka 

** Note: Kafka requires Docker to be running, and its containers must be started using `docker-compose up -d` **
### Install Dependencies

```bash
   pip install -r requirements.txt
```
Start the consumer by running:
```bash
  python -m python_services.Kafka.consumer
```
</details>

<!-- Usage -->
## Usage

Use this space to tell a little more about your project and how it can be used. Show additional screenshots, code samples, demos or link to other resources.


```
 
```


<!-- Acknowledgments -->
## Acknowledgements

Use this section to mention useful resources and libraries that you have used in your projects.

 - [Awesome README](https://github.com/matiassingers/awesome-readme)

