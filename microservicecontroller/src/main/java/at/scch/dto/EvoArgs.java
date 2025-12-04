package at.scch.dto;

public class EvoArgs {
    private String args;

    public EvoArgs() {
    }

    public EvoArgs(String args) {
        this.args = args;
    }

    public String getArgs() {
        return args;
    }

    public void setArgs(String args) {
        this.args = args;
    }

    @Override
    public String toString() {
        return args;
    }
}
