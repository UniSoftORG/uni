from ply import lex
import uuid

# Token Definitions
tokens = (
    "GEN_ELEMENT",
    "GEN_END",
    "LPAREN",
    "RPAREN",
    "VARIABLE",
    "STATE",
    "EQUALS",
    "LBRACKET",
    "RBRACKET",
    "COMMA",
    "TEXT",
    "STRING",
    "NUMBER",
    "LCURLY",
    "RCURLY",
    "COLON",
)

# Lexer Rules
t_GEN_ELEMENT = r"@gen:element"
t_GEN_END = r"@gen:end"
t_LCURLY = r"\{"
t_RCURLY = r"\}"
t_COLON = r":"
t_EQUALS = r"="
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_COMMA = r","
t_TEXT = r"[a-zA-Z_][a-zA-Z_0-9]*"
t_ignore = " \t"

def t_VARIABLE(t):
    r"@variable"
    return t


def t_STATE(t):
    r"@state"
    return t


def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\" "
    t.value = t.value[1:-1]
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

def generate_uuid():
    return str(uuid.uuid4())
    
lexer = lex.lex()
