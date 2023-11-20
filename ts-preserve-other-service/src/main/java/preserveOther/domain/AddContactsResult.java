package preserveOther.domain;

public class AddContactsResult {

    private boolean status;

    private String message;

    private Contacts contacts;

    private boolean isExists;

    public AddContactsResult() {
    }

    public AddContactsResult(boolean status, String message, Contacts contacts, boolean isExists) {
        this.status = status;
        this.message = message;
        this.contacts = contacts;
        this.isExists = isExists;
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

    public Contacts getContacts() {
        return contacts;
    }

    public void setContacts(Contacts contacts) {
        this.contacts = contacts;
    }

    public boolean isExists() {
        return isExists;
    }

    public void setExists(boolean exists) {
        isExists = exists;
    }
}
