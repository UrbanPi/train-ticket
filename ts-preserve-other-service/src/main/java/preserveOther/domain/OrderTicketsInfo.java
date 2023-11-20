package preserveOther.domain;

import java.util.Date;

public class OrderTicketsInfo {

    private String contactsId;

    private String tripId;

    private int seatType;

    private Date date;//具体到哪一天

    private String from;

    private String to;

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

    /***************** For Fault Reproduction - Error Normal *********************/
    private String isCreateContacts;

    private String contactsName;

    private int contactsDocumentType;

    private String contactsDocumentNumber;

    private String contactsPhoneNumber;
    /***************************************************************************/

    public OrderTicketsInfo(){
        //Default Constructor
    }

    /***************** For Fault Reproduction - Error Normal *********************/
    public String getIsCreateContacts() {
        return isCreateContacts;
    }

    public void setIsCreateContacts(String isCreateContacts) {
        this.isCreateContacts = isCreateContacts;
    }

    public String getContactsName() {
        return contactsName;
    }

    public void setContactsName(String contactsName) {
        this.contactsName = contactsName;
    }

    public int getContactsDocumentType() {
        return contactsDocumentType;
    }

    public void setContactsDocumentType(int contactsDocumentType) {
        this.contactsDocumentType = contactsDocumentType;
    }

    public String getContactsDocumentNumber() {
        return contactsDocumentNumber;
    }

    public void setContactsDocumentNumber(String contactsDocumentNumber) {
        this.contactsDocumentNumber = contactsDocumentNumber;
    }

    public String getContactsPhoneNumber() {
        return contactsPhoneNumber;
    }

    public void setContactsPhoneNumber(String contactsPhoneNumber) {
        this.contactsPhoneNumber = contactsPhoneNumber;
    }
    /***************************************************************************/

    public int getFoodType() {
        return foodType;
    }

    public void setFoodType(int foodType) {
        this.foodType = foodType;
    }

    public String getStationName() {
        return stationName;
    }

    public void setStationName(String stationName) {
        this.stationName = stationName;
    }

    public String getStoreName() {
        return storeName;
    }

    public void setStoreName(String storeName) {
        this.storeName = storeName;
    }

    public String getFoodName() {
        return foodName;
    }

    public void setFoodName(String foodName) {
        this.foodName = foodName;
    }

    public double getFoodPrice() {
        return foodPrice;
    }

    public void setFoodPrice(double foodPrice) {
        this.foodPrice = foodPrice;
    }

    public String getHandleDate() {
        return handleDate;
    }

    public void setHandleDate(String handleDate) {
        this.handleDate = handleDate;
    }

    public String getConsigneeName() {
        return consigneeName;
    }

    public void setConsigneeName(String consigneeName) {
        this.consigneeName = consigneeName;
    }

    public String getConsigneePhone() {
        return consigneePhone;
    }

    public void setConsigneePhone(String consigneePhone) {
        this.consigneePhone = consigneePhone;
    }

    public double getConsigneeWeight() {
        return consigneeWeight;
    }

    public void setConsigneeWeight(double consigneeWeight) {
        this.consigneeWeight = consigneeWeight;
    }

    public boolean isWithin() {
        return isWithin;
    }

    public void setWithin(boolean within) {
        isWithin = within;
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

    public int getAssurance() {
        return assurance;
    }

    public void setAssurance(int assurance) {
        this.assurance = assurance;
    }
}
