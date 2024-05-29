public class StudentDTO implements Serializable {

	private static final long serialVersionUID = 1L;

	private int id;
	private String nome;
	private String cognome;
	private Date dataDiNascita;
	private List<Course> courses;

	public StudentDTO() {
		this.courses = new ArrayList<Course>();
	}
	public int getId(){
        return this.id;
	}
    public void setId(int id){
		this.id=id;
	}	public String getNome(){
		return this.nome;
	}
	public void setNome(String nome){
		this.nome = nome;
	}

	public String getCognome(){
		return this.cognome;
	}
	public void setCognome(String cognome){
		this.cognome = cognome;
	}

	public Date getDataDiNascita(){
		return this.dataDiNascita;
	}
	public void setDataDiNascita(Date data_di_nascita){
		this.dataDiNascita = data_di_nascita;
	}

	public List<Course> getCourses(){
		return this.courses;
	}
	public void setCourses(List<Course> courses){
		this.courses = courses;
	}

}