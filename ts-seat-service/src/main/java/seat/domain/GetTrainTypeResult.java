package seat.domain;

public class GetTrainTypeResult {

    private boolean status;

    private String message;

    private TrainTypeClass trainTypeClass;

    public GetTrainTypeResult() {
        //Default Constructor
    }

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public TrainTypeClass getTrainTypeClass() {
        return trainTypeClass;
    }

    public void setTrainTypeClass(TrainTypeClass trainTypeClass) {
        this.trainTypeClass = trainTypeClass;
    }
}
