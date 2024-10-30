from translator import PDFTranslator, TranslationConfig
from utils import ArgumentParser, LOG
import sys
import os
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def translation(input_file, source_language, target_language, style, model_name, model_provider):
    LOG.debug(f"[翻译任务]\n源文件: {input_file.name}\n源语言: {source_language}\n目标语言: {target_language}\n翻译风格: {style}\n模型: {model_name}\n提供商: {model_provider}")

    global Translator
    Translator = PDFTranslator(
        model_name=model_name,
        model_provider=model_provider
    )

    output_file_path = Translator.translate_pdf(
        input_file.name,
        source_language=source_language,
        target_language=target_language,
        style=style
    )

    return output_file_path


def launch_gradio():

    iface = gr.Interface(
        fn=translation,
        title="LLM-Translator v2.2（PDF翻译工具）",
        inputs=[
            gr.File(label="上传PDF文件"),
            gr.Textbox(label="源语言（默认：英文）", placeholder="English", value="English"),
            gr.Textbox(label="目标语言（默认：中文）", placeholder="Chinese", value="Chinese"),
            gr.Dropdown(
                label="翻译风格",
                choices=["standard", "novel", "press_release", "academic", "casual"],
                value="standard"
            ),
            gr.Dropdown(
                label="模型选择",
                choices=["gpt-4o-mini", "glm-4"],
                value="gpt-4o-mini"
            ),
            gr.Dropdown(
                label="模型提供商",
                choices=["openai", "zhipuai"],
                value="openai"
            )
        ],
        outputs=[
            gr.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )

    iface.launch(share=True, server_name="0.0.0.0")


def initialize_translator():
    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    config = TranslationConfig()
    config.initialize(args)
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    global Translator
    Translator = PDFTranslator(
        model_name=config.model_name,
        model_provider=config.model_provider
    )


if __name__ == "__main__":
    # 初始化 translator
    initialize_translator()
    # 启动 Gradio 服务
    launch_gradio()
