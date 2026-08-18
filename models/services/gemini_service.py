# # """
# # Gemini AI Service
# # ==================
# # Calls Google Gemini API to:
# # 1. Find errors in code
# # 2. Correct the code
# # 3. Optimize the code
# # 4. Generate explanations

# # Uses google-generativeai SDK.
# # """

# # import os
# # import json
# # import re
# # import ast
# # from typing import Optional
# # from dotenv import load_dotenv

# # BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# # ENV_PATH = os.path.join(BASE_DIR, ".env")

# # load_dotenv(ENV_PATH)

# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


# # # ─────────────────────────────────────────────
# # # Initialize Gemini client
# # # ─────────────────────────────────────────────
# # try:
# #     import google.generativeai as genai

# #     if GEMINI_API_KEY:
# #         genai.configure(api_key=GEMINI_API_KEY)
# #         gemini_model = genai.GenerativeModel("gemini-pro")

# #         # 🔥 REAL TEST (safe)
# #         try:
# #             gemini_model.generate_content("Hello")
# #             GEMINI_AVAILABLE = True
# #             print("✅ Gemini fully working")
# #         except Exception as e:
# #             GEMINI_AVAILABLE = False
# #             print("❌ Gemini API failed:", e)
# #     else:
# #         GEMINI_AVAILABLE = False
# #         gemini_model = None
# #         print("❌ No API key found")

# # except ImportError:
# #     GEMINI_AVAILABLE = False
# #     gemini_model = None
# #     print("⚠️ Install: pip install google-generativeai")

# # # ─────────────────────────────────────────────
# # # Python Static Analysis (no AI needed)
# # # ─────────────────────────────────────────────

# # def static_analyze_python(code: str) -> list[dict]:
# #     """
# #     Use Python's built-in AST to detect syntax errors.
# #     Returns list of error dicts.
# #     """
# #     errors = []
# #     try:
# #         ast.parse(code)
# #     except SyntaxError as e:
# #         errors.append({
# #             "line":     e.lineno,
# #             "type":     "SyntaxError",
# #             "message":  str(e.msg),
# #             "severity": "error",
# #         })
# #     return errors


# # # ─────────────────────────────────────────────
# # # Gemini Analysis
# # # ─────────────────────────────────────────────

# # def _clean_json_response(text: str) -> str:
# #     """Strip markdown code fences from Gemini JSON responses."""
# #     text = re.sub(r"```(?:json)?\s*", "", text)
# #     text = re.sub(r"```", "", text)
# #     return text.strip()


# # def _clean_code_response(text: str) -> str:
# #     """Strip markdown code fences from code responses."""
# #     text = re.sub(r"```[\w]*\n?", "", text)
# #     text = re.sub(r"```", "", text)
# #     return text.strip()


# # async def analyze_with_gemini(
# #     code: str,
# #     language: str,
# #     title: str = "",
# # ) -> dict:
# #     """
# #     Send code to Gemini for full analysis.
# #     Returns dict with: errors, corrected_code, optimized_code, suggestions, explanation, quality_score
# #     Falls back to static analysis if Gemini unavailable.
# #     """

# #     # Static analysis for Python regardless
# #     static_errors = []
# #     if language == "python":
# #         static_errors = static_analyze_python(code)

# #     if not GEMINI_AVAILABLE:
# #         return _fallback_analysis(code, language, static_errors)

# #     prompt = f"""
# # You are an expert {language} code reviewer. Analyze the following {language} code thoroughly.

# # CODE TITLE: {title or 'Untitled'}
# # LANGUAGE: {language}
# # CODE:
# # ```{language}
# # {code}
# # ```

# # Respond ONLY with a valid JSON object (no markdown fences, no explanation outside JSON):
# # {{
# #   "errors": [
# #     {{
# #       "line": <line number or null>,
# #       "type": "<error type e.g. IndexError, SyntaxError, LogicError>",
# #       "message": "<clear description of the error>",
# #       "severity": "<error|warning|info>"
# #     }}
# #   ],
# #   "corrected_code": "<fully corrected {language} code with all bugs fixed>",
# #   "optimized_code": "<performance and readability optimized version of the corrected code>",
# #   "suggestions": "<3-5 actionable improvement suggestions as plain text bullet points>",
# #   "explanation": "<plain English explanation of what was wrong and what was changed>",
# #   "quality_score": <integer 0-100 representing code quality BEFORE fixes>
# # }}

# # Rules:
# # - If no errors exist, return empty errors array and original code for corrected_code
# # - quality_score: 0=broken, 50=average, 80=good, 100=perfect
# # - corrected_code and optimized_code must be complete, runnable code
# # - Do not truncate any code
# # """

# #     try:
# #         response = gemini_model.generate_content(prompt)
# #         raw = _clean_json_response(response.text)
# #         result = json.loads(raw)

# #         # Merge static errors that Gemini may have missed
# #         existing_lines = {e.get("line") for e in result.get("errors", [])}
# #         for se in static_errors:
# #             if se["line"] not in existing_lines:
# #                 result["errors"].append(se)

# #         return result

# #     except json.JSONDecodeError as e:
# #         print(f"⚠️  Gemini returned invalid JSON: {e}")
# #         # Try to extract code blocks at minimum
# #         return _fallback_analysis(code, language, static_errors)

# #     except Exception as e:
# #         print(f"⚠️  Gemini API error: {e}")
# #         return _fallback_analysis(code, language, static_errors)


# # def _fallback_analysis(code: str, language: str, static_errors: list) -> dict:
# #     """
# #     Used when Gemini is unavailable.
# #     Returns basic static analysis result.
# #     """
# #     return {
# #         "errors":          static_errors,
# #         "corrected_code":  code,
# #         "optimized_code":  code,
# #         "suggestions":     "• Install google-generativeai and set GEMINI_API_KEY for AI suggestions.\n• Run pylint or flake8 for Python linting.",
# #         "explanation":     "Gemini API not configured. Static Python syntax check performed only.",
# #         "quality_score":   None,
# #     }


# """
# Gemini AI Service
# ==================
# Calls Google Gemini API to:
# 1. Find errors in code
# 2. Correct the code
# 3. Optimize the code
# 4. Generate explanations
# """

# import os
# import json
# import re
# import ast
# from dotenv import load_dotenv

# # ─────────────────────────────────────────────
# # Load ENV properly
# # ─────────────────────────────────────────────
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ENV_PATH = os.path.join(BASE_DIR, "backend", ".env")

# load_dotenv(ENV_PATH)

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# # ─────────────────────────────────────────────
# # Initialize Gemini safely
# # ─────────────────────────────────────────────
# GEMINI_AVAILABLE = False
# gemini_model = None

# try:
#     import google.generativeai as genai

#     if GEMINI_API_KEY:
#         genai.configure(api_key=GEMINI_API_KEY)

#         # ✅ SAFE MODEL
#         gemini_model = genai.GenerativeModel("gemini-2.5-flash")

#         # ✅ REAL CONNECTION TEST
#         try:
#             test = gemini_model.generate_content("Hello")
#             if test:
#                 GEMINI_AVAILABLE = True
#                 print("✅ Gemini fully working")
#         except Exception as e:
#             GEMINI_AVAILABLE = False
#             print("❌ Gemini API failed:", e)
#     else:
#         print("❌ No GEMINI_API_KEY found in .env")

# except ImportError:
#     print("⚠️ Run: pip install google-generativeai")

# # ─────────────────────────────────────────────
# # Static Python Analysis
# # ─────────────────────────────────────────────
# def static_analyze_python(code: str):
#     errors = []
#     try:
#         ast.parse(code)
#     except SyntaxError as e:
#         errors.append({
#             "line": e.lineno,
#             "type": "SyntaxError",
#             "message": str(e.msg),
#             "severity": "error",
#         })
#     return errors


# # ─────────────────────────────────────────────
# # Helpers
# # ─────────────────────────────────────────────
# def _clean_json_response(text: str) -> str:
#     text = re.sub(r"```(?:json)?\s*", "", text)
#     text = re.sub(r"```", "", text)
#     return text.strip()


# # ─────────────────────────────────────────────
# # MAIN ANALYSIS FUNCTION
# # ─────────────────────────────────────────────
# def analyze_with_gemini(code: str, language: str, title: str = "") -> dict:

#     # Static analysis always for Python
#     static_errors = []
#     if language.lower() == "python":
#         static_errors = static_analyze_python(code)

#     # If Gemini not working → fallback
#     if not GEMINI_AVAILABLE or not gemini_model:
#         return _fallback_analysis(code, language, static_errors)

#     prompt = f"""
# You are an expert {language} code reviewer.

# Analyze the following code:

# TITLE: {title or "Untitled"}
# LANGUAGE: {language}

# CODE:
# {code}

# Return ONLY valid JSON:
# {{
#   "errors": [],
#   "corrected_code": "",
#   "optimized_code": "",
#   "suggestions": "",
#   "explanation": "",
#   "quality_score": 0
# }}
# """
# try:
#     response = await gemini_model.generate_content_async(prompt)

#     raw = _clean_json_response(response.text)
#     result = json.loads(raw)

#     # Merge static errors
#     existing_lines = {e.get("line") for e in result.get("errors", [])}
#     for se in static_errors:
#         if se["line"] not in existing_lines:
#             result["errors"].append(se)

#     return result

# except Exception as e:
#     print(f"⚠️ Gemini API error: {e}")
#     return _fallback_analysis(code, language, static_errors)


# # ─────────────────────────────────────────────
# # FALLBACK
# # ─────────────────────────────────────────────
# def _fallback_analysis(code: str, language: str, static_errors: list) -> dict:
#     return {
#         "errors": static_errors,
#         "corrected_code": code,
#         "optimized_code": code,
#         "suggestions": (
#             "• Gemini API not working\n"
#             "• Check API key\n"
#             "• Run: pip install google-generativeai\n"
#             "• Use pylint/flake8 for linting"
#         ),
#         "explanation": "Only static analysis available.",
#         "quality_score": None,
#     }

"""
Gemini AI Service
==================
Handles:
1. Error detection
2. Code correction
3. Optimization
4. Explanation
"""

import os
import json
import re
import ast
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# Load ENV
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, "backend", ".env")

load_dotenv(ENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ─────────────────────────────────────────────
# Initialize Gemini
# ─────────────────────────────────────────────
GEMINI_AVAILABLE = False
gemini_model = None

try:
    import google.generativeai as genai

    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel("gemini-2.5-flash")
        GEMINI_AVAILABLE = True
        print("✅ Gemini ready")
    else:
        print("❌ GEMINI_API_KEY missing")

except ImportError:
    print("⚠️ Install: pip install google-generativeai")


# ─────────────────────────────────────────────
# Static Python Analysis
# ─────────────────────────────────────────────
def static_analyze_python(code: str):
    errors = []
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append({
            "line": e.lineno,
            "type": "SyntaxError",
            "message": str(e.msg),
            "severity": "error",
        })
    return errors


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def _clean_json_response(text: str) -> str:
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()


# ─────────────────────────────────────────────
# MAIN FUNCTION (FIXED ✅)
# ─────────────────────────────────────────────
async def analyze_with_gemini(code: str, language: str, title: str = "") -> dict:

    # Static analysis
    static_errors = []
    if language.lower() == "python":
        static_errors = static_analyze_python(code)

    # If Gemini unavailable
    if not GEMINI_AVAILABLE or not gemini_model:
        return _fallback_analysis(code, language, static_errors)

    prompt = f"""
You are an expert {language} code reviewer.

Analyze the code below and return ONLY JSON:

CODE:
{code}

FORMAT:
{{
  "errors": [],
  "corrected_code": "",
  "optimized_code": "",
  "suggestions": "",
  "explanation": "",
  "quality_score": 0
}}
"""

    try:
        # ✅ ASYNC CALL FIXED
        response = await gemini_model.generate_content_async(prompt)

        raw = _clean_json_response(response.text)
        result = json.loads(raw)

        # Merge static errors
        existing_lines = {e.get("line") for e in result.get("errors", [])}
        for se in static_errors:
            if se["line"] not in existing_lines:
                result["errors"].append(se)

        return result

    except Exception as e:
        print(f"⚠️ Gemini API error: {e}")
        return _fallback_analysis(code, language, static_errors)


# ─────────────────────────────────────────────
# FALLBACK
# ─────────────────────────────────────────────
def _fallback_analysis(code: str, language: str, static_errors: list) -> dict:
    return {
        "errors": static_errors,
        "corrected_code": code,
        "optimized_code": code,
        "suggestions": (
            "• Gemini not working\n"
            "• Check API key\n"
            "• Install google-generativeai\n"
        ),
        "explanation": "Fallback: only static analysis used",
        "quality_score": None,
    }