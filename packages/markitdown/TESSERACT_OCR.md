# 🆓 图片文字提取 —— 免费离线方案

> 本 Fork 在 [microsoft/markitdown](https://github.com/microsoft/markitdown) 基础上增加了 **Tesseract OCR** 能力。
> **命令不变、无需 LLM、完全免费、离线可用。**

---

## 解决的问题

原版 MarkItDown 将 jpg/png 转换为 Markdown 时，只能提取 EXIF 元数据（拍摄参数等），
**无法提取图片里的文字**。要提取文字需要配置 LLM（如 GPT-4o），需要 API Key 且收费。

本改进提供了第三种选择：**Tesseract OCR**，免费、离线。

## 三种图片转换方式对比

| 方式 | 命令 | 需要什么 | 费用 |
|------|------|------|:---:|
| EXIF 元数据 | `markitdown image.jpg` | 无（默认） | 免费 |
| LLM 多模态 | Python API 传 `llm_client` | OpenAI API Key | 付费 |
| **🆕 Tesseract OCR** | **`markitdown image.jpg`** | **Tesseract 引擎** | **免费** ✅ |

---

## 安装（一次性）

### 1. 安装 Python 包

```bash
pip install markitdown[tesseract]
```

### 2. 安装 Tesseract-OCR 引擎

**Windows**：下载安装 [UB-Mannheim/Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
安装时勾选 **Chinese (Simplified)** 语言包。

**macOS**：`brew install tesseract tesseract-lang`

**Linux**：`sudo apt install tesseract-ocr tesseract-ocr-chi-sim`

---

## 使用

### 命令完全不变

```bash
# 图片 OCR → 提取文字为 Markdown
markitdown photo.jpg -o output.md

# 支持多张批量
markitdown screenshot.png -o notes.md

# PDF/Word 等其他文件 → 原版功能不受影响
markitdown document.pdf -o document.md
```

**自动判断**：jpg/jpeg/png/webp/bmp → Tesseract OCR，其他文件 → 原版转换。

### Python API

```python
from markitdown import MarkItDown
from markitdown.converters import TesseractConverter

md = MarkItDown()
md.register_converter(TesseractConverter())

result = md.convert("photo.jpg")
print(result.text_content)
```

---

## 支持的功能

- ✅ jpg / jpeg / png / webp / bmp 图片格式
- ✅ 中文 + 英文混合识别
- ✅ 自动修复 CJK 字符间多余空格
- ✅ 完全离线，无需 API Key
- ✅ 命令语法不变
- ✅ 原版所有功能不受影响

---

## 基于 Microsoft MarkItDown

本 Fork 完全兼容原版 [microsoft/markitdown](https://github.com/microsoft/markitdown)，所有原版功能保持不变。Tesseract OCR 作为增强功能叠加。

- 上游项目: https://github.com/microsoft/markitdown
- 许可证: MIT
