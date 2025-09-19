package clock;

import nz.sodium.*;

import static clock.Mode.*;

public class Clock {

    private static final int SEC_MAX = 60;
    private static final int MIN_MAX = 60;
    private static final int HOUR_MAX = 24;

    public final Cell<String> hour;
    public final Cell<String> min;
    public final Cell<String> sec;
    public final Cell<String> separator;

    public Clock(Stream<Unit> timeTicks, Stream<Unit> switchTicks, Stream<Unit> addTicks) {

        Cell<String> empty = new Cell<>("");

        StreamLoop<Unit> minAddTicks = new StreamLoop<>();
        Cell<Mode> mode = switchTicks
                .map(tick -> true)
                .orElse(minAddTicks.map(tick -> false))
                .accum(SHOW_TIME, (bool, md) -> bool ? md.next() : SET_MIN_SEC);

        Cell<Boolean> ticTac = timeTicks.accum(true, (tick, bool) -> !bool);
        Cell<String> blinkingColon = ticTac.map(bool -> bool ? "" : ":");
        Cell<String> firmColon = new Cell<>(":");
        separator = mode.lift(blinkingColon, firmColon,
                (md, blinking, firm) -> md.equals(SHOW_TIME) ? blinking : firm);

        Stream<Unit> secTimeTicks = timeTicks.gate(ticTac);
        Stream<Lambda1<Integer,Integer>> secAdvance = secTimeTicks
                .filter(tick -> !mode.sample().equals(SET_MIN_SEC))
                .map(tick -> sec -> (sec + 1) % SEC_MAX);
        Stream<Lambda1<Integer,Integer>> secReset = addTicks
                .filter(tick -> mode.sample().equals(SET_MIN_SEC))
                .map(tick -> sec -> 0);
        Cell<Integer> secCounter = secAdvance
                .orElse(secReset)
                .accum(0, (f, sec) -> f.apply(sec));
        Cell<String> secString = secCounter.map(sec -> String.format("%02d", sec));
        sec = secString;

        Stream<Unit> minTimeTicks = secTimeTicks
                .gate(secCounter.map(sec -> sec == SEC_MAX - 1))
                .gate(mode.map(md -> md.equals(SHOW_TIME)));
        minAddTicks.loop(addTicks
                .gate(mode.map(md -> md.equals(SET_MIN) || md.equals(SET_MIN_SEC))));
        Cell<Integer> minCounter = minTimeTicks
                .orElse(minAddTicks)
                .accum(0, (tick, min) -> (min + 1) % MIN_MAX);
        Cell<String> minString = minCounter.map(min -> String.format("%02d", min));
        Cell<String> blinkingMin = ticTac
                .lift(minString, empty, (bool, firm, hidden) -> bool ? firm : hidden);
        min = mode.lift(blinkingMin, minString, (md, blinking, firm) ->
                md.equals(SET_MIN) || md.equals(SET_MIN_SEC) ? blinking : firm);

        Stream<Unit> hourTimeTicks = minTimeTicks
                .gate(minCounter.map(min -> min == MIN_MAX - 1))
                .gate(mode.map(md -> md.equals(SHOW_TIME)));
        Stream<Unit> hourAddTicks = addTicks.gate(mode.map(md -> md.equals(SET_HOUR)));
        Cell<Integer> hourCounter = hourTimeTicks
                .orElse(hourAddTicks)
                .accum(0, (tick, hour) -> (hour + 1) % HOUR_MAX);
        Cell<String> hourString = hourCounter.map(hour -> String.format("%02d", hour));
        Cell<String> blinkingHour = ticTac
                .lift(hourString, empty, (bool, firm, empt) -> bool ? empt : firm);
        hour = mode.lift(blinkingHour, hourString,
                (md, blinking, firm) -> md.equals(SET_HOUR) ? blinking : firm);

    }
}
