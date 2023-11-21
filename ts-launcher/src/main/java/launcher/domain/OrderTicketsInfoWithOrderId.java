package launcher.domain;

import java.util.Date;

public class OrderTicketsInfoWithOrderId {
    private String contactsId;

    private String tripId;

    private int seatType;

    private Date date;//具体到哪一天

    private String from;

    private String to;

    private String orderId;


    //----------
    private int assurance;

    //food
    private int foodType = 0;

    private String stationName;

    private String storeName;

    private String foodName;

    private double foodPrice;

    //consign
    private String handleDate;

    private String consigneeName;

    private String consigneePhone;

    private double consigneeWeight;

    private boolean isWithin;

    public OrderTicketsInfoWithOrderId(){
        //Default Constructor
    }

    public OrderTicketsInfoWithOrderId(String contactsId, String tripId, int seatType, Date date, String from, String to, String orderId) {
        this.contactsId = contactsId;
        this.tripId = tripId;
        this.seatType = seatType;
        this.date = date;
        this.from = from;
        this.to = to;
        this.orderId = orderId;
    }

    public String getContactsId() {
        return contactsId;
    }

    public void setContactsId(String contactsId) {
        this.contactsId = contactsId;
    }

    public String getTripId() {
        return tripId;
    }

    public void setTripId(String tripId) {
        this.tripId = tripId;
    }

    public int getSeatType() {
        return seatType;
    }

    public void setSeatType(int seatType) {
        this.seatType = seatType;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public String getFrom() {
        return from;
    }

    public void setFrom(String from) {
        this.from = from;
    }

    public String getTo() {
        return to;
    }

    public void setTo(String to) {
        this.to = to;
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }
}
