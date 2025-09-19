package chat;

import javaslang.collection.HashMap;
import javaslang.collection.Map;
import javaslang.collection.Seq;
import nz.sodium.Cell;
import nz.sodium.Lambda1;
import nz.sodium.Stream;
import nz.sodium.StreamSink;

public class Chat {

    public final StreamSink<Session> joins = new StreamSink<>();
    public final StreamSink<Session> leaves = new StreamSink<>();
    public final Stream<Message> output;

    Chat() {
        Cell<Map<String, Session>> sessions = joins
                .<Lambda1<Map<String, Session>, Map<String, Session>>>map(session -> map -> map.put(session.nick, session))
                .orElse(leaves.map(leave -> map -> map.remove(leave.nick)))
                .accum(HashMap.empty(), (f, map) -> f.apply(map));
        Cell<Stream<Message>> mergedMessages =
                sessions.map(m -> mergeStreams(m.values().map(session -> session.messages)));
        Stream<Message> messages = Cell.switchS(mergedMessages);
        this.output = messages
                .orElse(joins.map(session -> new Message(session.nick, "joins")))
                .orElse(leaves.map(session -> new Message(session.nick, "leaves")));
    }

    public static <T> Stream<T> mergeStreams(Seq<Stream<T>> streams) {
        Stream<T> acc = new Stream<>();
        for (Stream<T> stream : streams) {
            acc = acc.orElse(stream);
        }
        return acc;
    }

}
