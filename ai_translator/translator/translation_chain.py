from langchain_openai import ChatOpenAI
from langchain_community.chat_models.zhipuai import ChatZhipuAI

from utils import LOG
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate


class TranslationChain:
    def __init__(self, model_name: str = "gpt-4o-mini", model_provider: str = "openai", verbose: bool = True):

        # 翻译任务指令始终由 System 角色承担
        template = (
            """You are a translation expert, proficient in various languages. \n
            Use the {style} style to translates from {source_language} to {target_language}."""
        )
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        # 待翻译文本由 Human 角色输入
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # 使用 System 和 Human 角色的提示模板构造 ChatPromptTemplate
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        # 根据不同的模型提供商选择对应的模型
        if model_provider == "openai":
            chat = ChatOpenAI(model_name=model_name, temperature=0, verbose=verbose)
        elif model_provider == "zhipuai":
            chat = ChatZhipuAI(model_name=model_name, temperature=0)
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")

        self.chain = chat_prompt_template | chat

    def run(self, text: str, source_language: str, target_language: str, style: str = "standard") -> (str, bool):
        result = ""
        try:
            result = self.chain.invoke({
                "text": text,
                "source_language": source_language,
                "target_language": target_language,
                "style": style
            })
        except Exception as e:
            LOG.error(f"An error occurred during translation: {e}")
            return result.content, False

        return result.content, True
