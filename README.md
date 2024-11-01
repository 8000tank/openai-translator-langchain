# LLM-Translator

<p align="center">
    <br> English | <a href="README-CN.md">中文</a>
</p>
<p align="center">
    <em>Most code and documentations are generated by OpenAI's GPT-4 and Anthropic's Claude-3.5-sonnet Model</em>
</p>

## Introduction

LLM Translator is an AI-powered translation tool designed to translate English PDF books to Chinese. The tool leverages large language models (LLMs) like ChatGLM and OpenAI's gpt-4o-mini for translation. It's built in Python and has a flexible, modular, and object-oriented design. The project is based on the [original project](https://github.com/DjangoPeng/openai-quickstart/tree/main/langchain/openai-translator), Based on it, LCEL transformation and functional improvements (adding the ZhiPu AI model and style translation) are carried out.

## Why this project

In the current landscape, there's a lack of non-commercial yet efficient PDF translation tools. Many users have PDF documents with sensitive data that they prefer not to upload to public commercial service websites due to privacy concerns. This project was developed to address this gap, providing a solution for users who need to translate their PDFs while maintaining data privacy.

### Sample Results

The LLM Translator is still in its early stages of development, and I'm actively working on adding more features and improving its performance. We appreciate any feedback or contributions!

![The_Gradio_GUI](images/sample_image_2.png)

<p align="center">
    <em>Gradio Interface</em>
</p>

![The_Old_Man_of_the_Sea](images/sample_image_0.png)

<p align="center">
    <em>"The Old Man and the Sea"</em>
</p>

## Features

- [x] Translation of English PDF books to Chinese using LLMs.
- [x] Support for both [ChatGLM](https://github.com/THUDM/ChatGLM-6B) and [OpenAI](https://platform.openai.com/docs/models) models.
- [x] Flexible configuration through a YAML file or command-line arguments.
- [x] Timeouts and error handling for robust translation operations.
- [x] Modular and object-oriented design for easy customization and extension.
- [x] Add support for other languages and translation directions.
- [x] Implement a graphical user interface (GUI) for easier use.
- [x] Create a web service or API to enable usage in web applications.
- [ ] Add support for batch processing of multiple PDF files.
- [ ] Add support for preserving the original layout and formatting of the source PDF.
- [ ] Improve translation quality by using custom-trained translation models.

## Getting Started

### Environment Setup

1.Clone the repository `git clone https://github.com/8000tank/openai-translator-langchain.git`.

2.The `LLM-Translator` requires Python 3.10 or later. Install the dependencies with `pip install -r requirements.txt`.

3.Set up your OpenAI API key(`$OPENAI_API_KEY`) and GLM API key(`$ZHIPUAI_API_KEY`). You can either add it to your environment variables or specify it in the config.yaml file.

### Usage

You can use LLM-Translator either by specifying a configuration file or by providing command-line arguments.

#### Using a configuration file:

Adapt `config.yaml` file with your settings:

```yaml
model_name: "gpt-4o-mini"
model_provider: "openai"
input_file: "tests/test.pdf"
output_file_format: "markdown"
source_language: "English"
target_language: "Chinese"
style: "standard"
```

Then run the tool:

```bash
python ai_translator/main.py
```

![sample_out](images/sample_image_1.png)

#### Using command-line arguments:

You can also specify the settings directly on the command line. Here's an example of how to use the OpenAI model:

```bash
# Set your api_key as an env variable
export OPENAI_API_KEY="sk-xxx"
python ai_translator/main.py --model_name "gpt-4o-mini" --input_file "your_input.pdf" --output_file_format "markdown" --source_language "English" --target_language "Chinese"
```

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.
