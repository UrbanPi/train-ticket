package cancel.domain;

//                voucherData = {}
//                        voucherData['voucher_id'] = voucher[0]
//                        voucherData['order_id'] = voucher[1]
//                        voucherData['travelDate'] = voucher[2]
//                        voucherData['contactName'] = voucher[4]
//                        voucherData['train_number'] = voucher[5]
//                        voucherData['seat_number'] = voucher[7]
//                        voucherData['start_station'] = voucher[8]
//                        voucherData['dest_station'] = voucher[9]
//                        voucherData['price'] = voucher[10]

public class GetVoucherEntity {

    private String voucher_id;

    private String order_id;

    private String travelDate;

    private String contactName;

    private String train_number;

    private String seat_number;

    private String start_station;

    private String dest_station;

    private String price;

    public GetVoucherEntity() {
        //Empty Constructor.
    }

    public String getVoucher_id() {
        return voucher_id;
    }

    public void setVoucher_id(String voucher_id) {
        this.voucher_id = voucher_id;
    }

    public String getOrder_id() {
        return order_id;
    }

    public void setOrder_id(String order_id) {
        this.order_id = order_id;
    }

    public String getTravelDate() {
        return travelDate;
    }

    public void setTravelDate(String travelDate) {
        this.travelDate = travelDate;
    }

    public String getContactName() {
        return contactName;
    }

    public void setContactName(String contactName) {
        this.contactName = contactName;
    }

    public String getTrain_number() {
        return train_number;
    }

    public void setTrain_number(String train_number) {
        this.train_number = train_number;
    }

    public String getSeat_number() {
        return seat_number;
    }

    public void setSeat_number(String seat_number) {
        this.seat_number = seat_number;
    }

    public String getStart_station() {
        return start_station;
    }

    public void setStart_station(String start_station) {
        this.start_station = start_station;
    }

    public String getDest_station() {
        return dest_station;
    }

    public void setDest_station(String dest_station) {
        this.dest_station = dest_station;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(String price) {
        this.price = price;
    }
}
