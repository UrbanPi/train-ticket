package travel.domain;

public class AdminTrip {
    private Trip trip;
    private TrainTypeClass trainTypeClass;
    private Route route;

    public AdminTrip(){

    }

    public Trip getTrip() {
        return trip;
    }

    public void setTrip(Trip trip) {
        this.trip = trip;
    }

    public TrainTypeClass getTrainTypeClass() {
        return trainTypeClass;
    }

    public void setTrainTypeClass(TrainTypeClass trainTypeClass) {
        this.trainTypeClass = trainTypeClass;
    }

    public Route getRoute() {
        return route;
    }

    public void setRoute(Route route) {
        this.route = route;
    }
}
