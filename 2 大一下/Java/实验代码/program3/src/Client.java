import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.*;
import javax.swing.*;

public class Client extends JFrame implements Runnable {
    private JTextArea textArea;
    private JTextField inputField;
    private JButton connectButton;
    private JButton sendButton;
    private Socket socket;
    private PrintWriter out;
    private BufferedReader in;

    public Client() {
        setTitle("Socket通信客户端");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        textArea = new JTextArea();
        textArea.setEditable(false);
        add(new JScrollPane(textArea), BorderLayout.CENTER);

        JPanel panel = new JPanel();
        inputField = new JTextField(20);
        connectButton = new JButton("Connect");
        sendButton = new JButton("Send");

        connectButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                connectToServer();
            }
        });

        sendButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                sendMessage();
            }
        });

        inputField.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                sendMessage();
            }
        });

        panel.add(connectButton);
        panel.add(sendButton);
        panel.add(inputField);
        add(panel, BorderLayout.SOUTH);

        setVisible(true);
    }

    private void connectToServer() {
        new Thread(this).start();
        connectButton.setEnabled(false);
        textArea.append("Connecting to server...\n");
    }

    private void sendMessage() {
        String message = inputField.getText();
        if (message.isEmpty()) return;

        if (out != null) {
            out.println(message);
            textArea.append("Sent: " + message + "\n");
            inputField.setText("");
        }
    }

    @Override
    public void run() {
        try {
            socket = new Socket("localhost", 12345);
            textArea.append("Connected to server...\n");

            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new PrintWriter(socket.getOutputStream(), true);

            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                textArea.append("Received: " + inputLine + "\n");
            }
        } catch (IOException e) {
            textArea.append("Error: " + e.getMessage() + "\n");
        } finally {
            try {
                if (in != null) in.close();
                if (out != null) out.close();
                if (socket != null) socket.close();
            } catch (IOException e) {
                textArea.append("Error closing connections: " + e.getMessage() + "\n");
            }
            textArea.append("Client disconnected.\n");
            connectButton.setEnabled(true);
        }
    }

    public static void main(String[] args) {
        new Client();
    }
}