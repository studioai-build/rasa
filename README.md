# rasa_medical_bot# Project Name

A brief description of your project.

## Table of Contents

- [rasa\_medical\_bot# Project Name](#rasa_medical_bot-project-name)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Example](#example)
  - [Configuration](#configuration)
  - [Contributing](#contributing)
  - [License](#license)
- [Get Started:](#get-started)
  - [the first terminal (enable API to test via CURL or POSTMAN):](#the-first-terminal-enable-api-to-test-via-curl-or-postman)
  - [the second terminal:](#the-second-terminal)
  - [Open Rasa shell](#open-rasa-shell)
  - [Train the model](#train-the-model)

## Installation

Instructions on how to install and set up your Rasa project.
- pip install rasa

## Usage

Instructions on how to use your Rasa project, including any command-line commands or scripts.
- the first terminal : rasa run --enable-api
- the second terminal : rasa run actions

send post request with json body look like this:

{
    "sender":"sender_id",
    "message": "put your text here"
}

## Example

curl --location 'http://localhost:5005/webhooks/rest/webhook' \
--header 'Content-Type: application/json' \
--data '{
    "sender": "123456789",
    "message": "can you explain my benefits for mri?"
}'

curl --location 'http://localhost:5005/webhooks/rest/webhook' \
--header 'Content-Type: application/json' \
--data '{
    "sender": "123456789",
    "message": "What is the status of my prior auth I submitted for member id"
}'

curl --location 'http://localhost:5005/webhooks/rest/webhook' \
--header 'Content-Type: application/json' \
--data '{
    "sender": "123456789",
    "message": "are there any limitations on my benefits for fitness"
}'


## Configuration

Details about the configuration options available in your Rasa project, such as environment variables or configuration files.

## Contributing

Guidelines for contributing to your Rasa project, including information on how to submit pull requests or report issues.

## License

Information about the license under which your Rasa project is distributed.


1. Rule => define intent+action (rule name can be same with intent) => data/rules.yml
2. are there any [restrictions constraints limitations](limitations) on my benefits for [maternity knee replacement surgery fitness](benefits)
   => inside parentheses => it’s entity 
   => inside bracket => it’s keywords
     data/nlu.yml
 3. domain.yml => define actions inside domain.yml
4. Action convention 
Need to extend from Action Class, and it need to include 2 function: name and run (return followupAction with action name)

# Get Started:

## the first terminal (enable API to test via CURL or POSTMAN):
    
```   
   rasa run --enable-api
```

## the second terminal: 
   
```
    rasa run actions
```

## Open Rasa shell

```
   rasa shell
```

## Train the model

```
   rasa train 
```
