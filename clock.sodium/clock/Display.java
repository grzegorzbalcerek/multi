package clock;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;

public class Display {
    private final Scene scene;
    private final Label hour;
    private final Label separator;
    private final Label minute;
    private final Label second;

    public Display(Runnable onSwitch, Runnable onAdd) {
        Button switchButton = button("Switch");
        switchButton.addEventHandler(ActionEvent.ACTION, event -> onSwitch.run());
        Button addButton = button("Add");
        addButton.addEventHandler(ActionEvent.ACTION, event -> onAdd.run());
        hour = label("", 100, 110);
        separator = label("", 100, 22);
        minute = label("", 100, 110);
        second = label("", 60, 70);
        HBox digits = new HBox(hour, separator, minute, second);
        digits.setAlignment(Pos.BASELINE_CENTER);
        HBox buttons = new HBox(switchButton, new Label(" "), addButton);
        buttons.setAlignment(Pos.CENTER);
        VBox layout = new VBox(digits, buttons);
        scene = new Scene(layout);
    }

    public Scene getScene() {
        return scene;
    }

    public void setSecond(String value) {
        Platform.runLater(() -> this.second.setText(value));
    }

    public void setMinute(String value) {
        Platform.runLater(() -> this.minute.setText(value));
    }

    public void setSeparator(String value) {
        Platform.runLater(() -> this.separator.setText(value));
    }

    public void setHour(String value) {
        Platform.runLater(() -> this.hour.setText(value));
    }

    Label label(String text, int size, int width) {
        Label label = new Label(text);
        label.setFont(new Font(size));
        label.setMinWidth(width);
        label.setMaxWidth(width);
        return label;
    }

    Button button(String text) {
        Button button = new Button(text);
        button.setMinSize(100, 50);
        return button;
    }

}
