package clock;

public enum Mode {
    SHOW_TIME,
    SET_HOUR,
    SET_MIN,
    SET_MIN_SEC;
    public Mode next() {
        switch (this) {
            case SHOW_TIME: return SET_HOUR;
            case SET_HOUR: return SET_MIN;
            default: return SHOW_TIME;
        }
    }
}
