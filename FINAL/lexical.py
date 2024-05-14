from pickle import TRUE
import re

from syntax import SyntaxAnalyzer



# Define helper functions
def is_delimiter(chr):
    return chr in [' ', '+', '-', '*', '/', ',', '%', '>', '<', '=', '(', ')', '[', ']', '{', '}','"','\'']

def is_operator(chr):
    return chr in ['+', '-', '*', '/', '>', '<', '=']

def is_operator(chr):
    return chr in ['+', '-', '*', '/', '>', '<', '=']


def is_valid_identifier(str):
    return str[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and not is_delimiter(str[0])

def is_keyword(str):
    keywords = ["auto", "break", "case", "char", "const", "continue", "default", "printf","scanf","do", "double", "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"]
    return str in keywords

def is_integer(str):
    return str.isdigit()

def is_semicolon(chr):
    return chr in [';']

def get_substring(str, start, end):
    return str[start:end+1]

def lexical_analyzer(input_str):
    tokens = []
    left = 0
    right = 0
    len_input = len(input_str)
    delimiter_stack = []

    # Process tokens until right reaches the end of the string
    while right < len_input:
        if not is_delimiter(input_str[right]):
            right += 1
        elif is_delimiter(input_str[right]) and left == right:
            if is_operator(input_str[right]):
                tokens.append(("Operator", input_str[right]))
            elif input_str[right] in ['(', ')', '[', ']', '{', '}', '"','\'']:  # Check for delimiters
                tokens.append(("Delimiter", input_str[right]))  # Append delimiters as tokens
            right += 1
            left = right
        else:
            sub_str = get_substring(input_str, left, right - 1)
            if is_keyword(sub_str):
                tokens.append(("Keyword", sub_str))
            elif is_integer(sub_str):
                tokens.append(("Integer", sub_str))
                
            elif is_semicolon(sub_str):  # Check if the substring is a semicolon
                tokens.append(("Semicolon", ';'))
                
            elif is_valid_identifier(sub_str) and not is_semicolon(sub_str) and not is_delimiter(input_str[right - 1]):
                tokens.append(("Identifier", sub_str))
            
            else:
                tokens.append(("Unidentified", sub_str))
            left = right

    # Process any remaining tokens after the loop
    if left < len_input:
        sub_str = get_substring(input_str, left, len_input - 1)
        if is_keyword(sub_str):
            tokens.append(("Keyword", sub_str))
        elif is_integer(sub_str):
            tokens.append(("Integer", sub_str))
        
        elif is_semicolon(sub_str):  # Check if the substring is a semicolon
            tokens.append(("Semicolon", sub_str))
            
        elif is_valid_identifier(sub_str) and not is_semicolon(sub_str) and not is_delimiter(input_str[len_input - 1]):
            tokens.append(("Identifier", sub_str))
        else:
            tokens.append(("Unidentified", sub_str))

    return tokens

def analyze_code():
        # Prompt the user for code input
        user_code = input("Enter the code to analyze: ")
        print(f"For Expression \"{user_code}\":")
        tokens =  lexical_analyzer(user_code)
        print("Tokens:")
        for token in tokens:
            print(token)
            
        analyzer = SyntaxAnalyzer(tokens)
        result = analyzer.parse()
        if result is not None:
            print(f"Syntax Analysis Result: VALID")
        else:
            print("Syntax is INVALID.")

while TRUE:
    analyze_code()
# # Example usage
# input_str1 = "int a = b + c"
# for token in lexical_analyzer(input_str1):
#     print(token)