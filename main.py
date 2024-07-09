import sys, re, os, shutil
from utils import syntax_error, snake2pascal
from type import Type
from relation import Relation
from attribute import Attribute
from mapping import Mapping
from factories import DAOfactory, DB2DAOfactory

FILENAME=sys.argv[1]
NODAO=len(sys.argv)>2
REPO=NODAO and sys.argv[2].lower()=="repo"
CARATETRI_INIZIALI="[a-zàèìòùé]"
ALTRI_CARATTERI="[a-z_0-9àèìòùé]"
PAROLA=CARATETRI_INIZIALI+ALTRI_CARATTERI+"*"

def from_file(filename):
    f = open(filename,"r", encoding="utf-8")
    txt = f.read()
    lines = txt.split("\n")
    _relations = {}
    _relation = ""
    mappings = {}
    clean_mappings = {}
    plurals={}
    for line in lines:
        res_relation = re.search("^("+PAROLA+")(/("+PAROLA+")){0,1}$", line)
        res_attribute = re.search("^("+PAROLA+"):("+PAROLA+")$",line)
        res_mappings = re.search("^("+PAROLA+")\*("+PAROLA+")$",line)
        res_empty = re.search("^$",line)
        if res_relation:
            _relation=res_relation.group(1)
            if(res_relation.group(3)==None):
                plurals[_relation]=_relation+"s"
            else:
                plurals[_relation]=res_relation.group(3)
            _relations[_relation]={}
        elif res_attribute and _relation!="":
            _relations[_relation][res_attribute.group(1)]=res_attribute.group(2)
        elif res_mappings:
            if res_mappings.group(1) in mappings:
                mappings[res_mappings.group(1)].append(res_mappings.group(2))
                clean_mappings[res_mappings.group(1)].append(res_mappings.group(2))
            else:
                mappings[res_mappings.group(1)]=[res_mappings.group(2)]
                clean_mappings[res_mappings.group(1)]=[res_mappings.group(2)]
            if res_mappings.group(2) in mappings:
                mappings[res_mappings.group(2)].append(res_mappings.group(1))
            else:
                mappings[res_mappings.group(2)]=[res_mappings.group(1)]
        elif res_empty:
            continue
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
                _type = Type(snake2pascal(type_name), "INT NOT NULL REFERENCES "+plurals[type_name]+"(id)", "Int", False, True)
            else:
                _type = Type(type_name, type_name.upper(), type_name[0].upper()+type_name[1:])
            
            attributes.append(Attribute(name, _type))
        if relation in mappings:
            for mapped in mappings[relation]:
                attributes.append(Attribute(plurals[mapped], Type(snake2pascal(mapped), None, True, True)))

        relations.append(Relation(relation, plurals[relation], attributes, NODAO))

    for relation in clean_mappings:
        for mapping in clean_mappings[relation]:
            relations.append(Mapping(relation, mapping, plurals[relation], plurals[mapping]))

    return relations

relations=from_file(FILENAME)

try:
    shutil.rmtree("out")
except FileNotFoundError:
    pass
os.mkdir("out")
if NODAO:
    for relation in relations:
        if type(relation) is Relation:
            with open("out\\"+relation.java_name()+".java", "w") as f:
                f.write(relation.getDTO())
        if REPO:
            with open("out\\"+relation.java_name()+"Repository.java", "w") as f:
                f.write(relation.getRepository())
        if not REPO:
            with open("out\\"+relation.java_name()+".sql", "w") as f:
                f.write(relation.getCreateDrop())
else:
    for relation in relations:
        if type(relation) is Relation:
            with open("out\\"+relation.java_name()+"DTO.java", "w") as f:
                f.write(relation.getDTO())
        with open("out\\"+relation.java_name()+"DAO.java", "w") as f:
            f.write(relation.getDAO())
        with open("out\\Db2"+relation.java_name()+"DAO.java", "w") as f:
            f.write(relation.getDb2DAO())
    with open("out\\DAOFactory.java", "w") as f:
        f.write(DAOfactory(relations))
    with open("out\\Db2DAOFactory.java", "w") as f:
        f.write(DB2DAOfactory(relations))
