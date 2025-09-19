package clock;

import nz.sodium.Stream;
import nz.sodium.StreamLoop;
import nz.sodium.Transaction;
import nz.sodium.Unit;
import nz.sodium.time.SecondsTimerSystem;

import java.util.Optional;

public class Time {
    public static Stream<Unit> timeTicks() {
        SecondsTimerSystem timer = new SecondsTimerSystem();
        return Transaction.run(() -> {
            StreamLoop<Double> ticks = new StreamLoop<>();
            ticks.loop(timer.at(ticks.accum(Optional.of(0.0d), (t1, t2) -> Optional.of(t1 + 0.5))));
            return ticks.map(t -> Unit.UNIT);
        });
    }
}
