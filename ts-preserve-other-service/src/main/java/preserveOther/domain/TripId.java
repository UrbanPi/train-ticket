package preserveOther.domain;

import classenum.TrainType;

import java.io.Serializable;

public class TripId implements Serializable{
    private TrainType type;
    private String number;

//    public TripId(Type type, String number){
//        this.type = type;
//        this.number = number;
//    }

    public TripId(){}

    public TripId(String trainNumber){
        char type = trainNumber.charAt(0);
        switch(type){
            case 'G': this.type = TrainType.G;
                break;
            case 'D': this.type = TrainType.D;
                break;
            case 'Z': this.type = TrainType.Z;
                break;
            case 'T': this.type = TrainType.T;
                break;
            case 'K': this.type = TrainType.K;
                break;
            default:break;
        }

        this.number = trainNumber.substring(1);
    }


    public TrainType getType() {
        return type;
    }

    public void setType(TrainType type) {
        this.type = type;
    }

    public String getNumber() {
        return number;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    @Override
    public String toString(){
        return type.getName() + number;
    }
}
