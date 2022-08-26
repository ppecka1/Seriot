import java.net.*;
import java.io.*;

public class MNServer {
    private ServerSocket serverSocket;
    private Socket clientSocket;
    private PrintWriter out;
    private BufferedReader in;

    public void start(int port) {
    try {
        serverSocket = new ServerSocket(port);
        clientSocket = serverSocket.accept();
        System.out.println("Connection accepted");
        out = new PrintWriter(clientSocket.getOutputStream(), true);
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        
        String inputLine;
        int sleeptime = 1;
        System.out.println("Waiting...");
        //while ((inputLine = in.readLine()) != null) {
        while (true) {
	    inputLine = in.readLine();
            if (".".equals(inputLine)) {
                out.println("good bye");
                break;
            }
            System.out.println("Received: " + inputLine);
            
	    // tutaj karmimy siec neuronowa i tworzymy odpowiedz
            System.out.println("Now sleeping " + sleeptime + " s");
            Thread.sleep(sleeptime * 1000);
            out.println("Java answered: " + inputLine);
            sleeptime++;
	}
    }
    catch(Exception e) {
    	System.out.println("IOException!");
    }
    }
    
    public void stop() {
    try {
        in.close();
        out.close();
        clientSocket.close();
        serverSocket.close();
    }
    catch(IOException e) {
    	System.out.println("IOException!");
    }
    }
    public static void main(String[] args) {
    // tu uruchamiamy sieci neuronowe i wszystko co trzeba
    // jak juz mamy wszystkie struktury danych, mozemy uruchomic serwer i czekac na dane
        MNServer server=new MNServer();
        server.start(65432);
        System.out.println("Hello");
    }
}
