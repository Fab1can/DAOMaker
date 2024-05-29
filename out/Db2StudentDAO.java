public class Db2StudentDAO implements StudentDAO {

	// === Costanti letterali per non sbagliarsi a scrivere !!! ============================

	static final String TABLE = "student";

	// -------------------------------------------------------------------------------------

	static final String ID = "id";
	static final String NOME = "nome";
	static final String COGNOME = "cognome";
	static final Date DATA_DI_NASCITA = "data_di_nascita";
	static final Course COURSES = "courses";

	// == STATEMENT SQL ====================================================================

	static final String insert = "INSERT " +
			"INTO " + TABLE + " ( " +
			ID +","+NOME+","+COGNOME+","+DATA_DI_NASCITA +
			") " +
			"VALUES (?,?,?,?) ";

	static String read_by_id = "SELECT * " +
			"FROM " + TABLE + " " +
			"WHERE " + ID + " = ? ";

	static String delete = "DELETE " +
			"FROM " + TABLE + " " +
			"WHERE " + ID + " = ? ";

	static String update = "UPDATE " + TABLE + " " +
			"SET " +
			NOME + " = ?, " +
			COGNOME + " = ?, " +
			DATA_DI_NASCITA + " = ?, " +
			"WHERE " + ID + " = ? ";

	static String query = "SELECT * " +
			"FROM " + TABLE + " ";

	// -------------------------------------------------------------------------------------

	static String create = "CREATE " +
			"TABLE " + TABLE + " ( " +
			ID + " INT NOT NULL PRIMARY KEY" +
,
			NOME + " VARCHAR(50), " +
			COGNOME + " VARCHAR(50), " +
			DATA_DI_NASCITA + " DATE
			") ";
	static String drop = "DROP " +
			"TABLE " + TABLE + " ";

	// === METODI DAO =========================================================================

	@Override
	public void create(StudentDTO student) {
		Connection conn = Db2DAOFactory.createConnection();
		if (course == null) {
			System.err.println("create(): failed to insert a null entry");
			return;
		}
		try {
			PreparedStatement prep_stmt = conn.prepareStatement(insert);
			prep_stmt.clearParameters();
			prep_stmt.setInt(1, course.getId());
			prep_stmt.getString(1, student.getNome()
			prep_stmt.getString(2, student.getCognome()
			prep_stmt.getDate(3, new java.sql.Date(student.getDataDiNascita().getTime())
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
	public StudentDTO read(int id) {
		StudentDTO result = null;
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
				StudentDTO entry = new StudentDTO();
				entry.setId(rs.getInt(ID));
			entry.setNome(rs.getString(NOME));
			entry.setCognome(rs.getString(COGNOME));
			entry.setDataDiNascita(new java.sql.Date(rs.getDate(DATA_DI_NASCITA).getTime()));
				
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
	public boolean update(StudentDTO student) {
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
			prep_stmt.getString(1, student.getNome()
			prep_stmt.getString(2, student.getCognome()
			prep_stmt.getDate(3, new java.sql.Date(student.getDataDiNascita().getTime())
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

}