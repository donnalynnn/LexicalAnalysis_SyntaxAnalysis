class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0

    def consume(self, token_type):
        if self.token_index < len(self.tokens) and self.tokens[self.token_index][0] == token_type:
            self.token_index += 1
            return True
        else:
            print(f"Expected {token_type}, but got {self.tokens[self.token_index][0]}")
            return False

    def parse_expression(self):
        left = self.parse_term()
        while self.token_index < len(self.tokens) and self.tokens[self.token_index][0] in ['+', '-', '*', '/']:
            op = self.tokens[self.token_index][0]
            if not self.consume(op):
                break
            right = self.parse_term()
            left = (left, op, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.token_index < len(self.tokens) and self.tokens[self.token_index][0] in ['*', '/']:
            op = self.tokens[self.token_index][0]
            if not self.consume(op):
                break
            right = self.parse_factor()
            left = (left, op, right)
        return left

    def parse_factor(self):
        token_type, token_value = self.tokens[self.token_index]
        if token_type in ['Keyword', 'Identifier']:
            if not self.consume(token_type):
                raise Exception(f"Expected a Keyword or Identifier, but got {token_type}")
            if token_type == 'Keyword' and (token_value == 'int' or token_value == 'float' or token_value == 'char' or token_value == 'bool'):
                self.validate_variable_declaration()
            if token_type == 'Keyword' and token_value == 'printf':
                self.check_printf_usage()
            return token_value
            
        elif token_type == '(':
            if not self.consume(token_type):
                raise Exception(f"Expected '(', but got {token_type}")
            result = self.parse_expression()
            if not self.consume(')'):
                raise Exception(f"Expected ')', but got {token_type}")
            return result
        else:
            raise Exception(f"Error")

    def validate_variable_declaration(self):
        print("val")
        if self.tokens[self.token_index][0] == '=':
            self.consume('=')
            if self.tokens[self.token_index][0] == 'int' or self.tokens[self.token_index][0] == 'float':
                if not self.consume('Integer'):
                    raise Exception("Expected a number after 'int' or 'float'")
            elif self.tokens[self.token_index][0] == 'char':
                if not self.consume("'") or not self.consume(r'\b([a-zA-Z_][a-zA-Z_0-9]*)\b') or not self.consume("'"):
                    raise Exception("Expected a character enclosed in single quotes after 'char'")
            elif self.tokens[self.token_index][0] == 'bool':
                print(self.tokens[self.token_index][0])
                if not self.consume('Identifier'):
                    raise Exception("Expected an Identifier after 'bool'")
                if self.tokens[self.token_index][0] == '=':
                    if not self.consume('true') and not self.consume('false'):
                        raise Exception("Expected 'true' or 'false' after '=' for 'bool'")
        else:
            print("else")
            next_token_index = self.token_index + 1
            if (self.tokens[next_token_index][0] == 'Identifier' or self.tokens[next_token_index][0] == 'Integer'):
                raise Exception("Invalid syntax. No identifier or integer allowed after keyword unless part of a variable declaration.")

    def validate_syntax(self):
        last_token_index = len(self.tokens) - 1
        last_token_type, last_token_value = self.tokens[last_token_index]
        if last_token_value!= ';':
            raise Exception("Syntax is invalid. Expected a semicolon at the end.")
        
    
    def check_printf_usage(self):
        # Initialize counters for specifiers and identifiers
        specifier_count = 0
        identifier_count = 0
        inside_quotes = False
        after_comma = False  # Flag to indicate we're after a comma
    
        # Iterate through tokens
        for token_type, token_value in self.tokens:
            if token_type == 'Keyword' and token_value == 'printf':
                # Found the start of a printf statement
                continue
            elif token_type == 'Delimiter' and token_value == '(':
                # Start of arguments
                continue
            elif token_type == 'Delimiter' and token_value == '"':
                # Inside quotes, toggle state
                inside_quotes = not inside_quotes
                continue
            elif token_type == 'Delimiter' and token_value == ',' and not inside_quotes:
                # Comma outside quotes, reset counts and set flag
                
                identifier_count = 0
                after_comma = True
                continue
            elif token_type == 'Specifier':
                specifier_count += 1
                continue
            elif token_type == 'Identifier' and after_comma:
                # Only count identifiers after a comma
                identifier_count += 1
                after_comma = False  # Reset flag after counting an identifier
                continue
            elif token_type == 'Delimiter' and token_value == ')':
                # End of arguments
                if specifier_count!= identifier_count:
                    raise Exception("Syntax Error: Mismatch in specifier and identifier count.")
                break

    
    def check_balanced_parentheses(self):
        open_paren_count = 0
        open_quot_count = 0
        open_bracket_count = 0
        open_braces_count = 0
        
        
        for token_type, token_value in self.tokens:
            if token_type == 'Delimiter' and token_value == '(':
                open_paren_count += 1
            elif token_type == 'Delimiter' and token_value == ')':
                open_paren_count -= 1
            elif token_type == 'Delimiter' and token_value == '"':
                open_quot_count += 1
            elif token_type == 'Delimiter' and token_value == '"':
                open_quot_count -= 1
            elif token_type == 'Delimiter' and token_value == '[':
                open_bracket_count += 1
            elif token_type == 'Delimiter' and token_value == ']':
                open_bracket_count -= 1
            elif token_type == 'Delimiter' and token_value == '{':
                open_braces_count += 1
            elif token_type == 'Delimiter' and token_value == '{':
                open_braces_count -= 1
            if open_paren_count < 0 and open_quot_count < 0 and open_braces_count < 0 and open_bracket_count < 0:
                raise Exception("Syntax Error: Unbalanced parentheses.")
        if open_paren_count!= 0:
            raise Exception("Syntax Error: Unbalanced parentheses.")

    def parse(self):
        try:
            self.check_balanced_parentheses()  # Check for balanced parentheses
            self.validate_syntax()
            result = self.parse_expression()
            
            return result
        except Exception as e:
            print(f"Syntax Error: {e}")
            return None
