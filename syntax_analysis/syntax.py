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
        if token_type in ['KEYWORD', 'IDENTIFIER']:
            if not self.consume(token_type):
                raise Exception(f"Expected a keyword or identifier, but got {token_type}")
            if token_type == 'IDENTIFIER':
                self.validate_variable_declaration()
            return token_value
        elif token_type == '(':
            if not self.consume(token_type):
                raise Exception(f"Expected '(', but got {token_type}")
            result = self.parse_expression()
            if not self.consume(')'):
                raise Exception(f"Expected ')', but got {token_type}")
            return result
        else:
            raise Exception(f"Expected a keyword, identifier, or '(', but got {token_type}")

    def validate_variable_declaration(self):
        if self.tokens[self.token_index][0] == '=':
            self.consume('=')
            if self.tokens[self.token_index][0] == 'int' or self.tokens[self.token_index][0] == 'float':
                if not self.consume('NUMBER'):
                    raise Exception("Expected a number after 'int' or 'float'")
            elif self.tokens[self.token_index][0] == 'char':
                if not self.consume("'") or not self.consume('CHARACTER') or not self.consume("'"):
                    raise Exception("Expected a character enclosed in single quotes after 'char'")
            else:
                raise Exception("Unexpected type after variable declaration")
        else:
            if not self.consume(';'):
                raise Exception("Expected a semicolon after variable declaration")

    def parse(self):
        try:
            result = self.parse_expression()
            if self.token_index == len(self.tokens) - 1 and not self.consume(';'):
                raise Exception("Syntax is invalid. Expected a semicolon at the end.")
            return result
        except Exception as e:
            print(f"Syntax Error: {e}")
            return None
