import sys, re

def snake2camel(string : str):
    words = string.split("_")
    if len(words)>1:
        return words[0]+"".join([word[0].upper()+word[1:] for word in words[1:]])
    return string

def snake2pascal(string: str):
    words = string.split("_")
    return "".join([word[0].upper()+word[1:] for word in words])

class Type:
    def __init__(self, java_name, sql_name, array_list=False):
        self.java_name = java_name
        self.sql_name = sql_name
        self.array_list = array_list

class Attribute:
    def __init__(self, name: str, type: Type):
        self.name=name
        self.type=type
    
    def java_name(self):
        return snake2camel(self.name)
    
    def java_signature(self):
        return snake2pascal(self.name)
    
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

class Relation:
    def __init__(self, name: str, attributes: list[Attribute]):
        self.name = name
        self.attributes = attributes
    
    def java_name(self):
        return snake2pascal(self.name)
    
    def getDAO(self):
        return """
public interface """+self.java_name()+"""DAO {

	// --- CRUD -------------

	public void create("""+self.java_name()+"""DTO """+self.name+""");

	public """+self.java_name()+"""DTO read(int id);

	public boolean update("""+self.java_name()+"""DTO """+self.name+""");

	public boolean delete(int id);

	
	// ----------------------------------
	
	public boolean createTable();

	public boolean dropTable();

}
"""

    def DTOconstructor(self):
        string = "\tpublic "
        string += self.java_name()
        string += "DTO() {\n"
        for attribute in self.attributes:
            if attribute.type.array_list:
                string += "\t\tthis."+attribute.java_name()+" = new ArrayList<"+attribute.type.java_name+">();\n"
        string += "\t}"
        return string
        

    def getDTO(self):
        string = "public class "
        string += self.java_name()
        string += "DTO implements Serializable {\n\n\tprivate static final long serialVersionUID = 1L;\n\n"
        string+="\tprivate int id;\n"
        for attribute in self.attributes:
            if attribute.type.array_list:
                string+="\tprivate List<"+attribute.type.java_name+"> "+attribute.java_name()+";\n"
            else:
                string+="\tprivate "+attribute.type.java_name+" "+attribute.java_name()+";\n"
        string += "\n"
        string += self.DTOconstructor()
        string += "\n"

        for attribute in self.attributes:
            string += attribute.get_getter()
            string += attribute.get_setter()
            string +="\n"
        string +="}"
        return string

class Mapping:
    def __init__(self, relation1, relation2):
        self.relation1 = relation1
        self.relation2 = relation2

    def java_name(self):
        return snake2pascal(self.relation1)+snake2pascal(self.relation2)+"Mapping"
    
    def getDAO(self):
        return """
public interface """+self.java_name()+"""DAO {

	// --- CRUD -------------

	public void create(int id"""+snake2pascal(self.relation1)+""", int id"""+snake2pascal(self.relation1)+""");

	public boolean delete(int id"""+snake2pascal(self.relation1)+""", int id"""+snake2pascal(self.relation1)+""");

	
	// ----------------------------------
	
	public boolean createTable();

	public boolean dropTable();

}
"""

def DAOfactory(relations):
    string = """
public abstract class DAOFactory {

	// --- List of supported DAO types ---

	/**
	 * Numeric constant '0' corresponds to explicit DB2 choice
	 */
	public static final int DB2 = 0;
	
	/**
	 * Numeric constant '1' corresponds to explicit Hsqldb choice
	 */
	public static final int HSQLDB = 1;
	
	/**
	 * Numeric constant '2' corresponds to explicit MySQL choice
	 */
	public static final int MYSQL = 2;
	
	
	// --- Actual factory method ---
	
	/**
	 * Depending on the input parameter
	 * this method returns one out of several possible 
	 * implementations of this factory spec 
	 */
	public static DAOFactory getDAOFactory(int whichFactory) {
		switch ( whichFactory ) {
		case DB2:
			return new Db2DAOFactory();
		case HSQLDB:
			return new HsqldbDAOFactory();
		case MYSQL:
			return new MySqlDAOFactory();
		default:
			return null;
		}
	}
	
	
	
"""
    for item in relations:
        string += "\tpublic abstract "+item.java_name()+"DAO get"+item.java_name()+"DAO();\n\n"
    string *= "}"
    return string

def DB2DAOfactory(relations, username, password):
    string = """
public class Db2DAOFactory extends DAOFactory {

	/**
	 * Name of the class that holds the jdbc driver implementation for the DB2 database
	 */
	public static final String DRIVER = "com.ibm.db2.jcc.DB2Driver";
	
	/**
	 * URI of the database to connect to
	 */
	public static final String DBURL = "jdbc:db2://diva.deis.unibo.it:50000/tw_stud";

	public static final String USERNAME = "xxx";
	public static final String PASSWORD = "xxx";
	

	// --------------------------------------------

	// static initializer block to load db driver class in memory
	static {
		try {
			Class.forName(DRIVER);
		} 
		catch (Exception e) {
			System.err.println(Db2DAOFactory.class.getName()+": failed to load DB2 JDBC driver" + "\n" + e.toString());
			e.printStackTrace();
		}
	}

	// --------------------------------------------

	/**
	 * For the sake of simplicity, here we create a brand new connection every time we are asked to.
	 * 
	 * Anyway, this is how things should go in the real world:
	 * 1. 	DB offers a limited number of connections (typically 100) so we can't really afford to 
	 * 		rely on factory invokers to always terminate the connection we have opened
	 * 2. 	At initialization, factory creates a well-defined number of connections (say 20) and put them
	 * 		in a pool
	 * 3.	create and close connection methods actually do not create or close brand new connections, but
	 * 		pick available connections from the pool, each time, and mark them as 'busy'/'free'
	 * 4.	factory does monitoring on the connection pool and force termination of connection in use
	 * 		for a too long time (invoker prob'ly forgot to close it... maybe due to exceptions it didn't handle well)
	 * 5.	terminated connections are replaced by brand new ones
	 */
	public static Connection createConnection() {
		try {
			return DriverManager.getConnection(DBURL,USERNAME,PASSWORD);
		} 
		catch (Exception e) {
			System.err.println(Db2DAOFactory.class.getName() + ".createConnection(): failed creating connection" + "\n" + e.toString());
			e.printStackTrace();
			System.err.println("Was the database started? Is the database URL right?");
			return null;
		}
	}
	
	/**
	 * For the sake of simplicity, here we actually close the connection we are told to.
	 */
	public static void closeConnection(Connection conn) {
		try {
			conn.close();
		}
		catch (Exception e) {
			System.err.println(Db2DAOFactory.class.getName() + ".closeConnection(): failed closing connection" + "\n" + e.toString());
			e.printStackTrace();
		}
	}

	// --------------------------------------------
	
"""
    for item in relations:
        string += "\t@Override\n"
        string += "\tpublic "+item.java_name()+"DAO get"+item.java_name()+"DAO() {\n"
        string += "\t\treturn new Db2"+item.java_name()+"DAO;\n"
        string += "\t}\n\n"
    string += "}"
    return string

def syntax_error():
    print("Syntax error")
    exit(1)

FILENAME="esempio"#sys.argv[0]

f = open(FILENAME,"r")
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
            _type = Type("String", "VARCHAR(50)")
        elif type_name=="int":
            _type = Type("int", "INT")
        elif type_name=="boolean":
            _type = Type("boolean", "BOOL")
        elif type_name=="date":
            _type = Type("Date", "DATE")
        elif type_name in _relations:
            _type = Type(snake2pascal(type_name), None)
        else:
            _type = Type(type_name, type_name.upper())
        
        attributes.append(Attribute(name, _type))
    if relation in mappings:
        for mapped in mappings[relation]:
            attributes.append(Attribute(mapped+"s", Type(snake2pascal(mapped), None, True)))
    else:
        syntax_error()
    relations.append(Relation(relation, attributes))

open("ciao", "w").write(relations[0].getDTO())
