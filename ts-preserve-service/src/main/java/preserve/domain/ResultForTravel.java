package preserve.domain;

import java.util.HashMap;


public class ResultForTravel {

    private boolean status;

    private double percent;

    private TrainTypeClass trainType;

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

    public TrainTypeClass getTrainType() {
        return trainType;
    }

    public void setTrainType(TrainTypeClass trainType) {
        this.trainType = trainType;
    }

    public HashMap<String, String> getPrices() {
        return prices;
    }

    public void setPrices(HashMap<String, String> prices) {
        this.prices = prices;
    }
}
