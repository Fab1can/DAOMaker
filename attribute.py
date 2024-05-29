from type import Type
from utils import snake2camel, snake2pascal

class Attribute:
    def __init__(self, name: str, type: Type):
        self.name=name
        self.type=type
    
    def java_name(self):
        return snake2camel(self.name)
    
    def java_signature(self):
        return snake2pascal(self.name)
    
    def static_name(self):
        if self.type.foreign:
            return self.name+"_id"
        else:
            return self.name

    def get_getter_method(self, variable):
        if self.type.sql_name=="DATE":
            return "new java.sql.Date("+variable+".get"+self.java_signature()+"().getTime())"
        elif self.type.java_name=="boolean":
            return variable+".is"+self.java_signature()+"()"
        elif self.type.foreign:
            return variable+".get"+self.java_signature()+"().getId()"
        else:
            return variable+".get"+self.java_signature()+"()"

    def get_setter_method(self):
        if self.type.sql_name=="DATE":
            return "entry.set"+self.java_signature()+"(new java.sql.Date(rs.getDate("+self.name.upper()+").getTime()))"
        elif self.type.java_name=="boolean":
            return "entry.is"+self.java_signature()+"(rs.getBoolean("+self.name.upper()+"))"
        else:
            return "entry.set"+self.java_signature()+"(rs.get"+self.type.prepared_name+"("+self.name.upper()+"))"

    def get_getter(self):
        string = "\tpublic "
        if self.type.array_list:
            string+="List<"+self.type.java_name+"> "
        else:
            string+=self.type.java_name+" "
        if self.type.java_name=="boolean":
            string+="is"+self.java_signature()
        else:
            string+="get"+self.java_signature()
        string += "(){\n\t\t"
        string += "return this."+self.java_name()+";\n\t}\n"
        return string
    
    def get_setter(self):
        string = "\tpublic void "
        if self.type.java_name=="boolean":
            string+="is"+self.java_signature()
        else:
            string+="set"+self.java_signature()
        string += "("
        if self.type.array_list:
            string+="List<"+self.type.java_name+"> "
        else:
            string+=self.type.java_name+" "
        string += self.name
        string += "){\n\t\t"
        string += "this."+self.java_name()+" = "+self.name+";\n\t}\n"
        return string
