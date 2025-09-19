package chat;

import nz.sodium.Stream;
import nz.sodium.StreamSink;

class Session {
    public String nick;
    public Stream<Message> output;
    public StreamSink<String> input = new StreamSink<>();
    public Stream<Message> messages;
    Session(String nick, Chat chat) {
        this.nick = nick;
        messages = input.filter(msg -> !"".equals(msg)).map(msg -> new Message(nick, msg));
        this.output = chat.output;
    }

}
