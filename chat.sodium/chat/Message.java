package chat;

public class Message {
    private final String source;
    private final String text;

    public Message(String source, String text) {
        this.source = source;
        this.text = text;
    }

    public String toString() {
        return "[" + source + "] " + text;
    }
}
