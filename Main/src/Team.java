import java.util.List;

public class Team {
    private List<Driver> members;

    public Team(String name) {
        this.members = null;
    }

    public void addDriver(Driver driver) {
        if (members.size() < 2) {
            this.members.add(driver);
        }
    }

    public int getTeamPoint() {
        int result = 0;
        for (Driver driver : members) {
            result += driver.getPoints();
        }
        return result;
    }
}
