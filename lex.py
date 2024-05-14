# import re

# # Function to check if a character is a delimiter
# def is_delimiter(chr):
#     return chr in [' ', '+', '-', '*', '/', ',', ';', '%', '>', '<', '=', '(', ')', '[', ']', '{', '}']

# # Function to check if a character is an operator
# def is_operator(chr):
#     return chr in ['+', '-', '*', '/', '>', '<', '=']

# # Function to check if a string is a valid identifier
# def is_valid_identifier(str):
#     return not (str[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or is_delimiter(str[0]))

# # Function to check if a string is a keyword
# def is_keyword(str):
#     keywords = ["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"]
#     return str in keywords

# # Function to check if a string is an integer
# def is_integer(str):
#     return str.isdigit()

# # Function to get a substring from a given string's start and end position
# def get_substring(str, start, end):
#     return str[start:end+1]

# # This function parses the input
# def lexical_analyzer(input):
#     tokens = re.findall(r'\b(\w+|\d+|[+\-*/<>]=?|[\{\}\[\]()])\b', input)
#     for token in tokens:
#         if is_operator(token):
#             print(f"Token: Operator, Value: {token}")
#         elif is_keyword(token):
#             print(f"Token: Keyword, Value: {token}")
#         elif is_integer(token):
#             print(f"Token: Integer, Value: {token}")
#         elif is_valid_identifier(token):
#             print(f"Token: Identifier, Value: {token}")
#         else:
#             print(f"Token: Unidentified, Value: {token}")

# # Main function
# def main():
#     # Input 01
#     lex_input = "int a = bk + xc - d;"
#     print(f"For Expression \"{lex_input}\":")
#     lexical_analyzer(lex_input)
#     print("\n")
#     # Input 02
#     lex_input01 = "int x=ab+bc+30+switch+ 0y "
#     print(f"For Expression \"{lex_input01}\":")
#     lexical_analyzer(lex_input01)

# if __name__ == "__main__":
#     main()
