package chat;

import java.net.ServerSocket;
import java.net.Socket;

public class App {
    public static void main(String[] args) throws Exception {
        new App().serverLoop();
    }

    private void serverLoop() throws Exception {
        System.out.println("Starting Chat Application");
        Chat chat = new Chat();
        ServerSocket serverSocket = new ServerSocket(5555);
        while (true) {
            Socket socket = serverSocket.accept();
            Thread t = new Thread(new Connection(socket, chat));
            t.start();
        }
    }

}

