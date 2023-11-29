package consign.domain;

public class GetPriceDomain {
    private double weight;
    private boolean isWithinRegion;
    private int country;

    public GetPriceDomain(){

    }

    public double getWeight() {
        return weight;
    }

    public void setWeight(double weight) {
        this.weight = weight;
    }

    public boolean isWithinRegion() {
        return isWithinRegion;
    }

    public void setWithinRegion(boolean withinRegion) {
        isWithinRegion = withinRegion;
    }

    public int getCountry() {
        return country;
    }

    public void setCountry(int country) {
        this.country = country;
    }
}
