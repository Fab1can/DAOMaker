from utils import snake2pascal

class Mapping:
    def __init__(self, relation1, relation2):
        self.relation1 = relation1
        self.relation2 = relation2

    def java_name(self):
        return snake2pascal(self.relation1)+snake2pascal(self.relation2)+"Mapping"
    
    def getDAO(self):
        return """
public interface {java_name}DAO {{

	// --- CRUD -------------

	public void create(int id{relation1}, int id{relation2});

	public boolean delete(int id{relation1}, int id{relation2});

	
	// ----------------------------------
	
	public boolean createTable();

	public boolean dropTable();

}}
""".format(java_name=self.java_name(), relation1=snake2pascal(self.relation1), relation2=snake2pascal(self.relation2))
    
    def getDb2DAO(self):
        return """
public class Db2{java_name}DAO implements {java_name}DAO {{

	// === Costanti letterali per non sbagliarsi a scrivere !!! ============================

	public static final String TABLE = "{relation1}_{relation2}";
    
    public static final String TABLE_1 = "{relation1}";
    public static final String TABLE_2 = "{relation2}";

	// -------------------------------------------------------------------------------------

	public static final String ID_1 = "{id1}";
	public static final String ID_2 = "{id2}";

	// == STATEMENT SQL ====================================================================

	static final String insert = "INSERT " +
			"INTO " + TABLE + " ( " +
			ID_1 + ", " + ID_2 + " " +
			") " +
			"VALUES (?,?) ";

	static String read_by_ids = "SELECT * " +
			"FROM " + TABLE + " " +
			"WHERE " + ID_1 + " = ? " +
			"AND " + ID_2 + " = ? ";

	static String read_by_{id1} = "SELECT * " +
			"FROM " + TABLE + " t , " + TABLE_2 + " t2 " +
			"WHERE t." + ID_2 + " = t2."+Db2{relation2_java_name}DAO.ID+" AND t." + ID_1 +" = ?";

	static String read_by_{id2} = "SELECT * " +
			"FROM " + TABLE + " t , " + TABLE_1 + " t1 " +
			"WHERE t." + ID_1 + " = t1."+Db2{relation1_java_name}DAO.ID+" AND t." + ID_2 +" = ?";

	static String read_all = "SELECT * " +
			"FROM " + TABLE + " ";

	static String delete = "DELETE " +
			"FROM " + TABLE + " " +
			"WHERE " + ID_1 + " = ? " +
			"AND " + ID_2 + " = ? ";

	// -------------------------------------------------------------------------------------

	static String create = "CREATE " +
			"TABLE " + TABLE + " ( " +
			ID_1 + " INT NOT NULL, " +
			ID_2 + " INT NOT NULL, " +
			"PRIMARY KEY (" + ID_1 + "," + ID_2 + " ), " +
			"FOREIGN KEY (" + ID_1 + ") REFERENCES {relation1}(id) ON DELETE CASCADE, " +
			"FOREIGN KEY (" + ID_2 + ") REFERENCES {relation2}(id) ON DELETE CASCADE" +
			") ";
	static String drop = "DROP " +
			"TABLE " + TABLE + " ";

	// === METODI DAO =========================================================================

	@Override
	public void create(int {id1}, int {id2}) {{
		Connection conn = Db2DAOFactory.createConnection();
		if ({id1} < 0 || {id2} < 0) {{
			System.err.println("create(): cannot insert an entry with an invalid id");
			return;
		}}
		try {{
			PreparedStatement prep_stmt = conn.prepareStatement(insert);
			prep_stmt.clearParameters();
			prep_stmt.setInt(1, {id1});
			prep_stmt.setInt(2, {id2});
			prep_stmt.executeUpdate();
			prep_stmt.close();
		}} catch (Exception e) {{
			System.err.println("create(): failed to insert entry: " + e.getMessage());
			e.printStackTrace();
		}} finally {{
			Db2DAOFactory.closeConnection(conn);
		}}
	}}

	@Override
	public boolean delete(int {id1}, int {id2}) {{
		boolean result = false;
		if ({id1} < 0 || {id2} < 0) {{
			System.err.println("delete(): cannot delete an entry with an invalid id ");
			return result;
		}}
		Connection conn = Db2DAOFactory.createConnection();
		try {{
			PreparedStatement prep_stmt = conn.prepareStatement(delete);
			prep_stmt.clearParameters();
			prep_stmt.setInt(1, {id1});
			prep_stmt.setInt(2, {id2});
			prep_stmt.executeUpdate();
			result = true;
			prep_stmt.close();
		}} catch (Exception e) {{
			System.err.println(
					"delete(): failed to delete entry with {id1} = " + {id1} + " and {id2} = " + {id2} + ": " + e.getMessage());
			e.printStackTrace();
		}} finally {{
			Db2DAOFactory.closeConnection(conn);
		}}
		return result;
	}}

	@Override
	public boolean createTable() {{
		boolean result = false;
		Connection conn = Db2DAOFactory.createConnection();
		try {{
			Statement stmt = conn.createStatement();
			stmt.execute(create);
			result = true;
			stmt.close();
		}} catch (Exception e) {{
			System.err.println("createTable(): failed to create table '" + TABLE + "': " + e.getMessage());
		}} finally {{
			Db2DAOFactory.closeConnection(conn);
		}}
		return result;
	}}

	@Override
	public boolean dropTable() {{
		boolean result = false;
		Connection conn = Db2DAOFactory.createConnection();
		try {{
			Statement stmt = conn.createStatement();
			stmt.execute(drop);
			result = true;
			stmt.close();
		}} catch (Exception e) {{
			System.err.println("dropTable(): failed to drop table '" + TABLE + "': " + e.getMessage());
		}} finally {{
			Db2DAOFactory.closeConnection(conn);
		}}
		return result;
	}}

}}""".format(java_name=self.java_name(), relation1=self.relation1, relation2=self.relation2, id1=self.relation1+"_id", id2=self.relation2+"_id", relation1_java_name=snake2pascal(self.relation1), relation2_java_name=snake2pascal(self.relation2))
