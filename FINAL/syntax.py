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
            if token_type == 'Keyword' and token_value == 'if':
                self.parse_if_statement()
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
        
    # def parse_if_statement(self):
    #     self.tokens[self.token_index][0] == 'if':
    #         self.consume('if')
    #         if not self.consume('('):
    #             raise Exception("Expected '(', but got something else.")
    #         self.parse_condition()  # Parse the condition
    #         if not self.consume(')'):
    #             raise Exception("Expected ')', but got something else.")
        

    def parse_condition(self):
        # Base case: If the current token is an identifier or an integer, return it as the condition
        if self.consume('Identifier') or self.consume('Integer'):
            return self.tokens[self.token_index - 1][1]  # Return the value of the token

        # Recursive case: Parse a condition that includes logical operators
        left = self.parse_condition()  # Parse the left side of the condition

        # Check for logical operators
        if self.tokens[self.token_index][0] == '&&':
            self.consume('&&')
            right = self.parse_condition()  # Parse the right side of the condition
            return (left, '&&', right)  # Return the combined condition
        elif self.tokens[self.token_index][0] == '||':
            self.consume('||')
            right = self.parse_condition()  # Parse the right side of the condition
            return (left, '||', right)  # Return the combined condition
        else:
            raise Exception("Expected a logical operator, but got something else.")

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
            if open_paren_count < 0:
                raise Exception("Syntax Error: Unbalanced parentheses.")
        if open_paren_count!= 0:
            raise Exception("Syntax Error: Unbalanced parentheses.")

    def parse(self):
        try:
            self.check_balanced_parentheses()  # Check for balanced parentheses
            result = self.parse_expression()
            return result
        except Exception as e:
            print(f"Syntax Error: {e}")
            return None
