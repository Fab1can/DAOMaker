
class Relation:
    def __init__(self, name: str, attributes: list[Attribute]):
        self.name = name
        self.attributes = attributes
    
    def non_list_attributes(self):
        nla = []
        for attribute in self.attributes:
            if not attribute.type.array_list:
                nla.applen(attribute)
        return nla

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

    def getDB2DAO(self):

        return """public class Db2{java_name}DAO implements {java_name}DAO {

	// === Costanti letterali per non sbagliarsi a scrivere !!! ============================

	static final String TABLE = "{sql_name}";

	// -------------------------------------------------------------------------------------

	static final String ID = "id";
{static_names}

	// == STATEMENT SQL ====================================================================

	static final String insert = "INSERT " +
			"INTO " + TABLE + " ( " +
			ID {insert_names} +
			") " +
			"VALUES (?{insert_interrogatives}) ";

	static String read_by_id = "SELECT * " +
			"FROM " + TABLE + " " +
			"WHERE " + ID + " = ? ";

	static String delete = "DELETE " +
			"FROM " + TABLE + " " +
			"WHERE " + ID + " = ? ";

	static String update = "UPDATE " + TABLE + " " +
			"SET " +
{update_names}
			"WHERE " + ID + " = ? ";

	static String query = "SELECT * " +
			"FROM " + TABLE + " ";

	// -------------------------------------------------------------------------------------

	static String create = "CREATE " +
			"TABLE " + TABLE + " ( " +
			ID + " INT NOT NULL PRIMARY KEY" +
{create_names}
			") ";
	static String drop = "DROP " +
			"TABLE " + TABLE + " ";

	// === METODI DAO =========================================================================

	@Override
	public void create({java_name}DTO {sql_name}) {
		Connection conn = Db2DAOFactory.createConnection();
		if (course == null) {
			System.err.println("create(): failed to insert a null entry");
			return;
		}
		try {
			PreparedStatement prep_stmt = conn.prepareStatement(insert);
			prep_stmt.clearParameters();
			prep_stmt.setInt(1, course.getId());
{insert_statement}
			prep_stmt.executeUpdate();
			prep_stmt.close();
			
			//GESTIRE ASSOCIAZIONI
				
			
		} catch (Exception e) {
			System.err.println("create(): failed to insert entry: " + e.getMessage());
			e.printStackTrace();
		} finally {
			Db2DAOFactory.closeConnection(conn);
		}
	}

	@Override
	public {java_name}DTO read(int id) {
		{java_name}DTO result = null;
		if (id < 0) {
			System.err.println("read(): cannot read an entry with a negative id");
			return result;
		}
		Connection conn = Db2DAOFactory.createConnection();
		try {
			PreparedStatement prep_stmt = conn.prepareStatement(read_by_id);
			prep_stmt.clearParameters();
			prep_stmt.setInt(1, id);
			ResultSet rs = prep_stmt.executeQuery();
			if (rs.next()) {
				{java_name}DTO entry = new {java_name}DTO();
				entry.setId(rs.getInt(ID));
{read_statement}
				
				//GESTIRE ASSOCIAZIONI
				result = entry;
			}
			rs.close();
			prep_stmt.close();
		} catch (Exception e) {
			System.err.println("read(): failed to retrieve entry with id = " + id + ": " + e.getMessage());
			e.printStackTrace();
		} finally {
			Db2DAOFactory.closeConnection(conn);
		}
		return result;
	}

	@Override
	public boolean update({java_name}DTO {sql_name}) {
		boolean result = false;
		if (course == null) {
			System.err.println("update(): failed to update a null entry");
			return result;
		}
		Connection conn = Db2DAOFactory.createConnection();
		try {
			PreparedStatement prep_stmt = conn.prepareStatement(update);
			prep_stmt.clearParameters();
			prep_stmt.setInt(1, course.getId());
{insert_statement}
			prep_stmt.executeUpdate();
			result = true;
			prep_stmt.close();
		} catch (Exception e) {
			System.err.println("insert(): failed to update entry: " + e.getMessage());
			e.printStackTrace();
		} finally {
			Db2DAOFactory.closeConnection(conn);
		}
		return result;
	}

	@Override
	public boolean delete(int id) {
		boolean result = false;
		if (id < 0) {
			System.err.println("delete(): cannot delete an entry with an invalid id ");
			return result;
		}
		Connection conn = Db2DAOFactory.createConnection();
		try {
			PreparedStatement prep_stmt = conn.prepareStatement(Db2CourseDAO.delete);
			prep_stmt.clearParameters();
			prep_stmt.setInt(1, id);
			prep_stmt.executeUpdate();
			result = true;
			prep_stmt.close();
		} catch (Exception e) {
			System.err.println("delete(): failed to delete entry with id = " + id + ": " + e.getMessage());
			e.printStackTrace();
		} finally {
			Db2DAOFactory.closeConnection(conn);
		}
		return result;
	}

	@Override
	public boolean createTable() {
		boolean result = false;
		Connection conn = Db2DAOFactory.createConnection();
		try {
			Statement stmt = conn.createStatement();
			stmt.execute(create);
			result = true;
			stmt.close();
		} catch (Exception e) {
			System.err.println("createTable(): failed to create table '" + TABLE + "': " + e.getMessage());
		} finally {
			Db2DAOFactory.closeConnection(conn);
		}
		return result;
	}

	@Override
	public boolean dropTable() {
		boolean result = false;
		Connection conn = Db2DAOFactory.createConnection();
		try {
			Statement stmt = conn.createStatement();
			stmt.execute(drop);
			result = true;
			stmt.close();
		} catch (Exception e) {
			System.err.println("dropTable(): failed to drop table '" + TABLE + "': " + e.getMessage());
		} finally {
			Db2DAOFactory.closeConnection(conn);
		}
		return result;
	}

}""".format(
    java_name=self.java_name(),
    sql_name=self.name, 
    static_names = "\n".join(["\tstatic final "+attribute.type.static_name()+" "+attribute.name.upper()+" = \""+attribute.static_name()+"\";" for attribute in self.attributes]),
    insert_names = "+\",\"+"+"+\",\"+".join([attribute.name.upper() for attribute in self.non_list_attributes()]) if len(self.non_list_attributes())>0 else "",
    insert_interrogatives = ","+",".join(["?" for attribute in self.non_list_attributes()]) if len(self.non_list_attributes())>0 else "",
    update_names = "\n".join(["\t\t\t"+attribute.name.upper()+" + \" = ?, \" +" for attribute in self.non_list_attributes()]),
    create_names = ",\n"+", \" +\n".join(["\t\t\t"+attribute.name.upper()+" + \" "+attribute.type.sql_name for attribute in self.non_list_attributes()]),
    insert_statemement = "\n".join(["\t\t\tprep_stmt.get"+ self.non_list_attributes()[i].type.prepared_name+"("+str(i+1)+", "+self.non_list_attributes()[i].get_getter_method(self.name) for i in range(len(self.non_list_attributes()))]),
    read_statement = "\n".join(["\t\t\t"+attribute.get_setter_method()+";" for attribute in self.non_list_attributes()])
)
        

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
        string += """
	public int getId(){
        return this.id;
	}
    public void setId(int id){
		this.id=id;
	}"""

        for attribute in self.attributes:
            string += attribute.get_getter()
            string += attribute.get_setter()
            string +="\n"
        string +="}"
        return string
