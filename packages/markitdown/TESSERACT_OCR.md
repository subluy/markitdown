# Tesseract OCR 增强（基于 Microsoft MarkItDown）

> 本 Fork 在 [microsoft/markitdown](https://github.com/microsoft/markitdown) 基础上增加了 **Tesseract OCR** 图片文字提取能力。

---

## 解决的问题

原版 MarkItDown 对 jpg/png 图片的转换仅提取 EXIF 元数据（拍摄参数等），无法提取图片中的文字内容。  
本增强为 MarkItDown 增加了真正的 OCR（光学字符识别）能力。

## 新增功能

- **TesseractConverter**：将 jpg / jpeg / png / webp / bmp 图片中的文字提取为 Markdown
- 支持中英文混合识别（及其他 100+ 语言）
- 自动处理 CJK 字符间空格（Tesseract 中文模型已知问题）
- 完全离线、免费、无需 API Key

## 安装

```bash
# 安装基础包 + Tesseract 依赖
pip install markitdown[tesseract]

# 安装 Tesseract-OCR 引擎（Windows）
# 下载: https://github.com/UB-Mannheim/tesseract/wiki
# 安装时勾选中文语言包
```

## 使用

### Python API

```python
from markitdown import MarkItDown
from markitdown.converters import TesseractConverter

md = MarkItDown()
md.register_converter(TesseractConverter())
result = md.convert("photo.jpg")
print(result.text_content)
```

### 自定义语言和路径

```python
converter = TesseractConverter()
md.register_converter(converter)

result = md.convert(
    "image.jpg",
    tesseract_lang="chi_sim+eng",           # 识别语言
    tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe",  # 引擎路径
    tesseract_tessdata_dir=r"C:\path\to\tessdata",  # 语言包路径
)
```

## 与原版对比

| 功能 | 原版 MarkItDown | 本 Fork |
|------|:---:|:---:|
| 提取 EXIF 元数据 | ✓ | ✓ |
| 多模态 LLM 图片描述 | ✓ | ✓ |
| **Tesseract OCR 文字提取** | ✗ | **✓** |
| 离线可用 | ✗ | **✓** |
| 免费 | ✗ | **✓** |
| 中文支持 | ✗ | **✓** |

## 基于原项目

本增强完全兼容原版 Microsoft MarkItDown，所有原版功能保持不变。
TesseractConverter 作为可选转换器，需手动注册后使用。

- 原项目: [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown)
- 许可证: MIT
