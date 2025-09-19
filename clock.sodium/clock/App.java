package clock;

import javafx.application.Application;
import javafx.stage.Stage;
import nz.sodium.StreamSink;
import nz.sodium.Transaction;
import nz.sodium.Unit;

import static clock.Time.timeTicks;

public class App extends Application {
    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) throws Exception {
        primaryStage.setTitle("Clock");

        StreamSink<Unit> switchTicks = new StreamSink<>();
        StreamSink<Unit> addTicks = new StreamSink<>();
        Clock clock = Transaction.run(() ->
                new Clock(timeTicks(), switchTicks, addTicks));
        Display display = new Display(
                () -> switchTicks.send(Unit.UNIT),
                () -> addTicks.send(Unit.UNIT));
        clock.hour.listen(display::setHour);
        clock.min.listen(display::setMinute);
        clock.sec.listen(display::setSecond);
        clock.separator.listen(display::setSeparator);

        primaryStage.setScene(display.getScene());
        primaryStage.show();
    }

}
