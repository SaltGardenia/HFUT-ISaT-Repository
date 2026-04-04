import java.awt.*;//方便绘图引入的包
import java.awt.event.*;
import java.io.*;//文件输入的IO流
import java.net.*;
import javax.swing.*;

public class Server extends JFrame implements Runnable {
    private JTextArea/*Jtext的作用是用来显示多行文本*/ textArea;
    private JButton startButton;
    private JButton sendButton;
    private JTextField/*用于输入单行的组件*/ inputField;
    private ServerSocket/*提前定一个端口，固定数字方便寻找，等待别人找他*/ serverSocket;
    private Socket/*通信端口，用于建立双向通信*/ clientSocket;
    private PrintWriter/*输出流向Socket发送信息*/ out;
    private BufferedReader/*输入流从Socket接收信息*/ in;

    public Server() {
        setTitle("Socket通信服务器端");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);// 设置关闭窗口时的行为，这里设置为退出程序
        setLayout(new BorderLayout());//一种特殊的布局，将组件按照边界布局的方式添加到窗体中

        textArea = new JTextArea();//使我的内容可以滚动输出
        textArea.setEditable(false);//讲文本区域设置为不可以修改，只可以查看
        add(new JScrollPane(textArea)/*就是使我的输入内容滚动输出*/, BorderLayout.CENTER);//在中间显示文本

        JPanel panel = new JPanel();//设置一个画布，将之后用到的东西放在这一个画布中
        startButton = new JButton("Start");
        sendButton = new JButton("Send");
        inputField = new JTextField(20);//最多放20个字

        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                startServer();//按压Start按键，启动服务器，我的多线程后台启动
            }
        });

        sendButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                sendMessage();//直接输入发送信息，直接按回车键，发送信息
                //我在具体方法里写好了程序
            }
        });

        inputField.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                sendMessage();//检测输入回车也可以
            }
        });

        panel.add(startButton);
        panel.add(sendButton);
        panel.add(inputField);
        add(panel, BorderLayout.SOUTH);

        setVisible(true);
    }

    private void startServer() {
        startButton.setEnabled(false);//禁用按钮,防止重复点击，点一次就好
        textArea.append("Server starting...\n");//提示正在启动服务器
        new Thread(this).start();//创建一个线程，并启动线程，在后台运行，不然我的主程序容易卡死
    }

    private void sendMessage() {
        String message = inputField.getText();//是Swing中的文本框，用于输入信息，
        // 返回值赋值给massage获得信息
        if (message.isEmpty()) return;//如果是空的直接返回
        if (out != null) {//提前创建好的out流，用于输出信息，检查输出流是否为空
            out.println(message);//东西发送在服务器
            textArea.append("Sent: " + message + "\n");//用户可以看到Sent所发的内容
            inputField.setText("");//对于输入框的内容清空，可以输入新的消息
        }
    }

    @Override
    public void run() {
        try {
            serverSocket = new ServerSocket(12345);//设置一个端口号，固定数字方便寻找，等待别人找他
            textArea.append("Waiting for client connection...\n");//显示等待客户端连接

            clientSocket = serverSocket.accept();//表示我的服务器等待客户端连接
            textArea.append("Client connected...\n");

            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()/*获取 Socket 对象的输入流，用于从客户端读取数据
            同时返回一个 InputStream 对象*/));//将 InputStream 转换为 InputStreamReader字符流，自动处理字符编码，以便能够按字符读取数据。
            out = new PrintWriter(clientSocket.getOutputStream()/*获取 Socket 对象的输输出流，用于向客户端发送数据
            同时返回一个 OutputStream 对象*/, true);

            String inputLine;//创建一个字符串变量，用于存储客户端的每一行信息
            while ((inputLine = in/*in在我之前的创造是一个BufferedReader*/.readLine()) != null) {//我利用了 in.readLine()方法，从客户端读取信息
            //如果不返回空就执行这个方案，如果返回空就跳出循环
                textArea.append("Received: " + inputLine + "\n");//打印，可视化，我发的消息
            }
        } catch (IOException e) {
            textArea.append("Error: " + e.getMessage() + "\n");//如果出现错误就打印错误信息
        } finally {//代表无论什么，都会执行这个方案，所以用finally
            try {
                if (in != null) in.close();//检查并关闭输入流，输出流，客户端连接，服务器连接
                if (out != null) out.close();
                if (clientSocket != null) clientSocket.close();
                if (serverSocket != null) serverSocket.close();
            } catch (IOException e) {
                textArea.append("Error closing connections: " + e.getMessage() + "\n");//打印错误信息
            }
            textArea.append("Server stopped.\n");//打印信息
            startButton.setEnabled(true);//表示开始按钮可以再次使用
        }
    }

    public static void main(String[] args) {
        new Server();//主体部分，运行
    }
}