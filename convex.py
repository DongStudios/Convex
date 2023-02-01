# Convex 面向过程语言
# 当前版本：Alpha 0.1.1.4
# 发行版：尚未发行

# 令牌名称
class TokenTypes:
    INTEGER = 0
    
    # 加减乘除
    PLUS = 1
    MINUS = 2
    MUL = 3
    DIV = 4
    
    # 左右括号
    LPAREN = 5
    RPAREN = 6
    
    EOF = -1

# 语法错误
class CoSyntaxError(Exception):
    # 错误表达式
    error_exp = None
    def __init__(self) -> None:
        super().__init__()

# 令牌类
class Token:
    # 初始化令牌
    # value_type: 令牌种类
    # value: 值
    def __init__(self, value_type, value) -> None:
        self.value_type = value_type
        self.value = value
    
    # 令牌内容（字符串）
    def __str__(self) -> str:
        return f"<Token type={self.value_type} value={self.value}>"
    __repr__ = __str__

# 词法分析器
class Lexer:
    # 初始化分析器
    # exp: 表达式
    def __init__(self, exp: str) -> None:
        self.exp: str = exp
        self.position: int = 0 # 当前分析的字符
        self.current_char: str = self.exp[self.position]
        
    # 语法错误
    def error(self) -> None:
        error = CoSyntaxError()
        error.error_exp = self.exp
        raise error
    
    # 推进下一个字符
    def advance(self) -> None:
        self.position += 1
        if self.position >= len(self.exp):
            self.current_char = None
        else:
            self.current_char = self.exp[self.position]
            
    # 跳过多个空格
    def skip_whitespace(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.advance()    
                    
    # 获取数字
    def integer(self) -> int:
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char 
            self.advance()
        return int(result)
    
    # 获取下一个令牌
    def get_next_token(self):
        while self.current_char is not None:
            # 跳过空格
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # 整数
            if self.current_char.isdigit():
                return Token(TokenTypes.INTEGER, self.integer())
            
            # 加减乘除
            if self.current_char == "+":
                self.advance()
                return Token(TokenTypes.PLUS, "+")
            if self.current_char == "-":
                self.advance()
                return Token(TokenTypes.MINUS, "-")
            if self.current_char == "*":
                self.advance()
                return Token(TokenTypes.MUL, "*")
            if self.current_char == "/":
                self.advance()
                return Token(TokenTypes.DIV, "/")
            if self.current_char == "(":
                self.advance()
                return Token(TokenTypes.LPAREN, "(")
            if self.current_char == ")":
                self.advance()
                return Token(TokenTypes.RPAREN, ")")
            
            # 都不是，则报错
            self.error()
        
        return Token(TokenTypes.EOF, None)


# 解释器
class Interpreter:
    # 初始化解释器
    # lexer: 一个词法分析器
    def __init__(self, lexer:Lexer) -> None:
        self.lexer: Lexer = lexer
        # 直接获取第一个令牌
        self.current_token: Token = self.lexer.get_next_token()

    # 如果当前令牌是指定类型，则推进一个令牌
    # 如果不是指定类型将报错，需提前判断
    def eat(self, token_type: int) -> None:
        if self.current_token.value_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.lexer.error()
    
    # 根据当前的令牌获取整数
    # 与token_integer不同的是，该函数在确定下一个令牌是整数时在计算表达式中使用
    # 而token_integer用来从表达式中获取数字，进而得到Token
    def factor(self) -> int:
        token = self.current_token
        # 整数
        if token.value_type == TokenTypes.INTEGER:
            self.eat(TokenTypes.INTEGER)
            return token.value
        # 左括号
        elif token.value_type == TokenTypes.LPAREN:
            self.eat(TokenTypes.LPAREN)
            result = self.expr() # 括号里面的表达式值
            self.eat(TokenTypes.RPAREN)
            return result
    
    # 乘除法语法分析与计算
    def term(self) -> int:
        result = self.factor()
        while self.current_token.value_type in (TokenTypes.MUL, TokenTypes.DIV):
            token = self.current_token
            if token.value_type == TokenTypes.MUL:
                self.eat(TokenTypes.MUL)
                result *= self.factor()
            else:
                self.eat(TokenTypes.DIV)
                result /= self.factor()
        return result
    
    # 计算结果
    def expr(self):
        # 获取第一个整数
        result = self.term()
        
        # 循环计算加减（顶层），调用term计算乘除法
        while self.current_token.value_type in (TokenTypes.PLUS, TokenTypes.MINUS):
            token = self.current_token
            if token.value_type == TokenTypes.PLUS:
                self.eat(TokenTypes.PLUS)
                result += self.term()
            elif token.value_type == TokenTypes.MINUS:
                self.eat(TokenTypes.MINUS)
                result -= self.term()
        
        return result
    
if __name__ == "__main__":
    print("Convex 0.1 交互式解释器 [MSVC 14.29.30013 x64]")
    print("注意：当前正使用 Alpha 版本 0.1.1.4")
    while True:
        try:
            exp = input(">>> ")
        # 输入结束：退出
        except EOFError:
            break
        # 没有输入：继续
        if not exp:
            continue
        
        try:
            lexer = Lexer(exp)
            interpreter = Interpreter(lexer)
            result = interpreter.expr()
        except CoSyntaxError as e:
            print("语法错误：无效的语法")
            print(f"    位于：{e.error_exp}\n")
            continue
        print(result)