package cancel.domain;

public class HandleVoucherOfCancelOrderInfo {

    private String orderId;

    private int type;

    private int operation;

    public HandleVoucherOfCancelOrderInfo() {
        //Empty Constructor. Do nothing.
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }

    public int getOperation() {
        return operation;
    }

    public void setOperation(int operation) {
        this.operation = operation;
    }
}
