from ast import While
from pickle import TRUE
import re
from FINAL.syntax import SyntaxAnalyzer

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.keywords = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
            'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed',
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
        }

    def tokenize(self):
        # Tokenize for keywords
        for keyword in self.keywords:
            #whitespace around the keywords
            if re.search(keyword + r'\s+', self.code):
                self.tokens.append(('KEYWORD', keyword))

        # Tokenize for identifiers, excluding keywords
        identifier_pattern = r'\b([a-zA-Z_][a-zA-Z_0-9]*)\b'
        for match in re.finditer(identifier_pattern, self.code):
            if match.group() not in self.keywords:
                self.tokens.append(('IDENTIFIER', match.group()))

        # Tokenize for other patterns (operators, literals, strings, numbers, etc.)
        patterns = [
            (r'\s+', None),  # Ignore whitespace
            (r'[+\-*/%]', 'ARITHMETIC_OPERATOR'),  # Arithmetic Operators
            (r'==|!=|<|>|<=|>=', 'RELATIONAL_OPERATOR'),  # Relational Operators
            (r'&&|\|\|', 'LOGICAL_OPERATOR'),  # Logical Operators
            (r'&|\||\^|\~|\<<|\>>', 'BITWISE_OPERATOR'),  # Bitwise Operators
            (r'=|\+=|-=|\*=|\/=|\%=|&=|\|=|\^=|\<<=|\>>=', 'ASSIGNMENT_OPERATOR'),  # Assignment Operators
            (r'--|\+\+', 'UNARY_OPERATOR'),
            (r'\?', 'OTHER_OPERATOR'),  # Other Operators
            (r'\".*?\"', 'STRING'),  # Strings
            (r'\d+(\.\d+)?', 'NUMBER'),  # Numbers
            (r'\{', 'LBRACE'),  # Left curly brace
            (r'\}', 'RBRACE'),  # Right curly brace
            (r'\(', 'LPAREN'),  # Left parenthesis
            (r'\)', 'RPAREN'),  # Right parenthesis
            (r'\[', 'LBRACKET'),  # Left bracket
            (r'\]', 'RBRACKET'),  # Right bracket
            (r';', 'SEMICOLON'),  # Semicolon
            
        ]
        # for pattern, token_type in patterns:
        #     try:
        #         match = re.search(pattern, self.code)
        #         if match:
        #             if token_type is None:
        #                 continue
        #             self.tokens.append((token_type, match.group()))
        #     except re.error as e:
        #         print(f"Error in pattern '{pattern}': {e}")

        # self.tokens.append(('CODE', self.code))
        last_token_appended = False
        for pattern, token_type in patterns:
            try:
                match = re.search(pattern, self.code)
                if match and not last_token_appended:
                    if token_type is None:
                        continue
                    self.tokens.append((token_type, match.group()))
                    last_token_appended = True
            except re.error as e:
                print(f"Error in pattern '{pattern}': {e}")
            finally:
                last_token_appended = False

    def get_tokens(self):
        return self.tokens
    
    def analyze_code(self):
        # Prompt the user for code input
        user_code = input("Enter the code to analyze: ")
        self.code = user_code
        self.tokenize()
        print("Tokens:")
        for token in self.get_tokens():
            print(token)
            
        analyzer = SyntaxAnalyzer(self.get_tokens())
        result = analyzer.parse()
        if result is not None:
            print(f"Syntax Analysis Result: VALID")
        else:
            print("Syntax is INVALID.")
            
    

# Example usage
while TRUE:
    lexer = Lexer("")
    lexer.analyze_code()

# # Example usage
# lexer = Lexer("string i = 0;")
# lexer.tokenize()
# print(lexer.get_tokens())