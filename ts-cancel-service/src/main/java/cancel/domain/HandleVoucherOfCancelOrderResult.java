package cancel.domain;

public class HandleVoucherOfCancelOrderResult {

    private boolean status;

    private String message;

    public HandleVoucherOfCancelOrderResult() {
        //Empty Constructor. Do nothing
    }

    public HandleVoucherOfCancelOrderResult(boolean status, String message) {
        this.status = status;
        this.message = message;
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
}
