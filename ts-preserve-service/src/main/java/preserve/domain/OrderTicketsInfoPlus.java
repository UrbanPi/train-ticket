package preserve.domain;

/**
 * Created by fdse-jichao on 2018/1/25.
 */
public class OrderTicketsInfoPlus {

    private OrderTicketsInfo info;

    private String loginId;

    private String loginToken;

    public OrderTicketsInfoPlus() {
    }

    public OrderTicketsInfo getInfo() {
        return info;
    }

    public void setInfo(OrderTicketsInfo info) {
        this.info = info;
    }

    public String getLoginId() {
        return loginId;
    }

    public void setLoginId(String loginId) {
        this.loginId = loginId;
    }

    public String getLoginToken() {
        return loginToken;
    }

    public void setLoginToken(String loginToken) {
        this.loginToken = loginToken;
    }
}
