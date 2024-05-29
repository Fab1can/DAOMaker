import sys, re
from utils import syntax_error, snake2pascal
from type import Type
from relation import Relation
from attribute import Attribute

FILENAME="esempio"#sys.argv[0]

def from_file(filename):
    f = open(filename,"r")
    txt = f.read()
    lines = txt.split("\n")
    _relations = {}
    _relation = ""
    mappings = {}
    for line in lines:
        res_relation = re.search("^[a-z][a-z_0-9]*$", line)
        res_attribute = re.search("^([a-z][a-z_0-9]*):([a-z][a-z_0-9]*)$",line)
        res_mappings = re.search("^([a-z][a-z_0-9]*)\*([a-z][a-z_0-9]*)$",line)
        if res_relation:
            _relations[line]={}
            _relation=line
        elif res_attribute and _relation!="":
            _relations[_relation][res_attribute.group(1)]=res_attribute.group(2)
        elif res_mappings:
            if res_mappings.group(1) in mappings:
                mappings[res_mappings.group(1)].append(res_mappings.group(2))
            else:
                mappings[res_mappings.group(1)]=[res_mappings.group(2)]
            if res_mappings.group(2) in mappings:
                mappings[res_mappings.group(2)].append(res_mappings.group(1))
            else:
                mappings[res_mappings.group(2)]=[res_mappings.group(1)]
        else:
            syntax_error()

    relations = []

    for relation in _relations:
        attributes = []
        for attribute in _relations[relation]:
            name = attribute
            type_name = _relations[relation][attribute]
            _type = None
            if type_name=="string":
                _type = Type("String", "VARCHAR(50)", "String")
            elif type_name=="int":
                _type = Type("int", "INT", "Int")
            elif type_name=="float":
                _type = Type("float", "FLOAT", "Float")
            elif type_name=="boolean":
                _type = Type("boolean", "BOOL", "Boolean")
            elif type_name=="date":
                _type = Type("Date", "DATE", "Date")
            elif type_name in _relations:
                _type = Type(snake2pascal(type_name), "INT NOT NULL REFERENCES "+type_name+"("+type_name+"_id)", "Int", False, True)
            else:
                _type = Type(type_name, type_name.upper(), type_name[0].upper()+type_name[1:])
            
            attributes.append(Attribute(name, _type))
        if relation in mappings:
            for mapped in mappings[relation]:
                attributes.append(Attribute(mapped+"s", Type(snake2pascal(mapped), None, True, True)))
        else:
            syntax_error()
        relations.append(Relation(relation, attributes))
        return relations

relations=from_file(FILENAME)
open("ciao", "w").write(relations[0].getDTO())
