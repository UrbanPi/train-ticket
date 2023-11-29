package consignprice.domain;

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

    @Override
    public String toString() {
        String ret = String.format("Weight is %f. isWithinRegion is %b. country is %d",this.weight,this.isWithinRegion,this.country);
        return ret;
    }
}
