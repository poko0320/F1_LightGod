public class Driver {
    private String name;
    private int driver_number;
    private Team team;
    private int points;

    public Driver(String name, int driver_number, Team team) {
        this.name = name;
        this.team = team;
        this.driver_number = driver_number;
        this.points = 0;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getDriver_number() {
        return driver_number;
    }

    public void setDriver_number(int driver_number) {
        this.driver_number = driver_number;
    }

    public Team getTeam() {
        return team;
    }

    public void setTeam(Team team) {
        this.team = team;
    }

    public void addPoints(int points) {
        this.points += points;
    }

    public int getPoints() {
        return points;
    }
}
