import json
import re

# File paths
input_file = "Final_maths_variant_batches.js"
output_file = "Final_maths_variant_batches_fixed.js"

# Function to clean and format options
def clean_options(options_string):
    # Convert string to proper list format
    options_string = options_string.strip("[]")
    options_list = re.split(r"(?<!\\)'(?!\\)", options_string)  # Split by unescaped single quotes
    options_list = [
        latex_to_human_readable(opt.strip().lstrip("'"))  # Remove any leading single quotes
        for opt in options_list if opt.strip()
    ]
    return options_list

# Function to make LaTeX and Unicode human-readable
def latex_to_human_readable(text):
    # Remove LaTeX delimiters
    text = text.replace("$$", "").replace("$", "").replace("\\\\", "\\")

    # Replace LaTeX expressions with human-readable math symbols
    text = re.sub(r"\\frac{([^{}]+)}{([^{}]+)}", r"(\1) / (\2)", text)  # Fraction
    text = re.sub(r"\\sqrt{([^{}]+)}", r"√(\1)", text)  # Square root
    text = text.replace("\\times", "×").replace("\\div", "÷")  # Basic math symbols

    # General Unicode replacements
    unicode_replacements = {
        "\u221a": "√",  # Square root
        "\u00d7": "×",  # Multiplication
        "\u00f7": "÷",  # Division
        "\u201c": "\"",  # Left double quotation mark
        "\u201d": "\"",  # Right double quotation mark
        "\u2018": "'",   # Left single quotation mark
        "\u2019": "'",   # Right single quotation mark
        "\u00b1": "±",   # Plus-minus
        "\u2264": "≤",   # Less-than or equal to
        "\u2265": "≥",   # Greater-than or equal to
        "\u2013": "–",   # En dash
        "\u2014": "—",   # Em dash
        "\u2022": "•",   # Bullet point
    }

    # Replace all Unicode symbols based on the dictionary
    for unicode_char, replacement in unicode_replacements.items():
        text = text.replace(unicode_char, replacement)

    # Handle escaped Unicode (e.g., "\\u221a")
    text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda match: chr(int(match.group(1), 16)), text)

    return text

# Read and process the file
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Remove JS variable declaration to isolate the JSON
content = content.replace("var variant_batches = ", "").strip()

# Parse JSON content
variant_batches = json.loads(content)

# Fix issues in "question" and "options"
for variant, batches in variant_batches.items():
    for batch_index, questions in batches.items():
        for question in questions:
            # Make question human-readable
            if "question" in question:
                question["question"] = latex_to_human_readable(question["question"])
            
            # Fix and format options
            if "options" in question:
                question["options"] = clean_options(question["options"])

# Save the fixed content back to a new file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("var variant_batches = ")
    json.dump(variant_batches, f, indent=4, ensure_ascii=False)  # Prevent Unicode escaping

print(f"Fixed variant_batches has been saved to {output_file}")
