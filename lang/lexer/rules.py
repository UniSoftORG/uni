from ply import yacc
from .definitions import tokens
from .utils import generate_uuid

# Parser Rules
def p_program(p):
    """program : program gen_element
    | gen_element"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_statements(p):
    """statements : statements statement
    | statement"""
    if len(p) == 3:
        statement_type, key, value = p[2]
        if statement_type == "state":
            p[0] = {**p[1], "states": {**p[1].get("states", {}), **{key: value}}}
        else:
            p[0] = {**p[1], "variables": {**p[1].get("variables", {}), **{key: value}}}
    else:
        statement_type, key, value = p[1]
        if statement_type == "state":
            p[0] = {"states": {key: value}}
        else:
            p[0] = {"variables": {key: value}}


def p_gen_element(p):
    """gen_element : GEN_ELEMENT LPAREN gen_params RPAREN COLON statements GEN_END"""
    uuid = generate_uuid()
    p[0] = {
        "uuid": uuid,
        "name": p[3].get("name", ""),
        "type": "Element",
        "element": p[3].get("type", ""),
        **p[6],
    }


def p_gen_params(p):
    """gen_params : gen_params COMMA gen_param
    | gen_param"""
    if len(p) == 4:
        p[0] = {**p[1], **p[3]}
    else:
        p[0] = p[1]


def p_gen_param(p):
    "gen_param : TEXT COLON value"
    p[0] = {p[1]: p[3]}


def p_statement_variable(p):
    "statement : VARIABLE TEXT EQUALS item"
    p[0] = ("variable", p[2], p[4])


def p_statement_state(p):
    "statement : STATE TEXT EQUALS item"
    p[0] = ("state", p[2], p[4])


def p_item(p):
    """item : object
    | list
    | NUMBER
    | STRING"""
    p[0] = p[1]


def p_object(p):
    "object : LCURLY keyvalues RCURLY"
    p[0] = {k: v for k, v in p[2]}


def p_list(p):
    "list : LBRACKET items RBRACKET"
    p[0] = p[2]


def p_items(p):
    """items : items COMMA item
    | item
    |"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_keyvalues(p):
    """keyvalues : keyvalues COMMA keyvalue
    | keyvalue
    |"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_keyvalue(p):
    "keyvalue : TEXT COLON value"
    p[0] = (p[1], p[3])


def p_value(p):
    """value : STRING
    | object
    | NUMBER"""
    p[0] = p[1]


def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value '{p.value}' at line {p.lineno}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc(start="program", debug=True)