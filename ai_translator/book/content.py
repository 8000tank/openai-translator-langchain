import pandas as pd
import re
from enum import Enum, auto
from PIL import Image as PILImage
from utils import LOG


class ContentType(Enum):
    TEXT = auto()
    TABLE = auto()
    IMAGE = auto()


class Content:
    def __init__(self, content_type, original, translation=None):
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False

    def set_translation(self, translation, status):
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def check_translation_type(self, translation):
        if self.content_type == ContentType.TEXT and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(translation, list):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(translation, PILImage.Image):
            return True
        return False

    def __str__(self):
        return self.original


class TableContent(Content):
    def __init__(self, data, translation=None):
        df = pd.DataFrame(data)

        # Verify if the number of rows and columns in the data and DataFrame object match
        if len(data) != len(df) or len(data[0]) != len(df.columns):
            raise ValueError("The number of rows and columns in the extracted table data and DataFrame object do not match.")

        super().__init__(ContentType.TABLE, df)

    def set_translation(self, translation, status):
        try:
            if not isinstance(translation, str):
                raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")

            # 将中文方括号替换为英文方括号
            translation = translation.replace('【', '[').replace('】', ']')

            LOG.debug(f"[translation]\n{translation}")

            # 提取表头和数据
            parts = translation.split(']')
            if len(parts) < 2:
                raise ValueError("Invalid table format")

            # 处理表头：支持逗号、顿号等多种分隔符
            header = re.split('[,、，]\s*', parts[0][1:].strip())

            # 处理数据行：支持多种分隔符和格式
            data_rows = parts[1:]
            # 清理每行数据并用多种分隔符分割
            data_rows = [re.split('[,、，]\s*', row.strip().strip('[]')) for row in data_rows if row.strip()]

            # 创建 DataFrame
            translated_df = pd.DataFrame(data_rows, columns=header)
            LOG.debug(f"[translated_df]\n{translated_df}")

            self.translation = translated_df
            self.status = status
        except Exception as e:
            LOG.error(f"An error occurred during table translation: {e}")
            self.translation = None
            self.status = False

    def __str__(self):
        return self.original.to_string(header=False, index=False)

    def iter_items(self, translated=False):
        target_df = self.translation if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx, item in enumerate(row):
                yield (row_idx, col_idx, item)

    def update_item(self, row_idx, col_idx, new_value, translated=False):
        target_df = self.translation if translated else self.original
        target_df.at[row_idx, col_idx] = new_value

    def get_original_as_str(self):
        return self.original.to_string(header=False, index=False)
