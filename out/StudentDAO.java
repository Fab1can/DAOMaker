
public interface StudentDAO {

	// --- CRUD -------------

	public void create(StudentDTO student);

	public StudentDTO read(int id);

	public boolean update(StudentDTO student);

	public boolean delete(int id);

	
	// ----------------------------------
	
	public boolean createTable();

	public boolean dropTable();

}
