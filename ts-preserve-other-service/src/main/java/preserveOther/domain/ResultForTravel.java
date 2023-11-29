package preserveOther.domain;

import java.util.HashMap;


public class ResultForTravel {

    private boolean status;

    private double percent;

    private TrainTypeClass trainTypeClass;

    private HashMap<String,String> prices;

    public ResultForTravel(){
        //Default Constructor
    }

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    public double getPercent() {
        return percent;
    }

    public void setPercent(double percent){
        this.percent = percent;
    }

    public TrainTypeClass getTrainTypeClass() {
        return trainTypeClass;
    }

    public void setTrainTypeClass(TrainTypeClass trainTypeClass) {
        this.trainTypeClass = trainTypeClass;
    }

    public HashMap<String, String> getPrices() {
        return prices;
    }

    public void setPrices(HashMap<String, String> prices) {
        this.prices = prices;
    }
}
