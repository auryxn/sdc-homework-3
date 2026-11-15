package tasks;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Task6 {
    public static void main(String[] args) throws InterruptedException {
        boolean graceful = args.length > 0 && args[0].equalsIgnoreCase("graceful");
        ThreadGroup group = new ThreadGroup("ClientRequests");
        List<Thread> workers = new ArrayList<>();
        Random random = new Random();

        System.out.println("Server started.");
        System.out.println("ThreadGroup: " + group.getName());

        for (int i = 1; i <= 5; i++) {
            int client = i;
            int duration = 1000 + random.nextInt(9000);
            Thread worker = new Thread(group, () -> processRequest(client, duration), "Client-" + client);
            workers.add(worker);
            worker.start();
        }

        Thread.sleep(5000);
        System.out.println("Active threads: " + group.activeCount());
        for (Thread worker : workers) {
            System.out.println(worker.getName() + " - " + worker.getState());
        }

        if (graceful) {
            System.out.println("Graceful shutdown initiated.");
            for (Thread worker : workers) {
                worker.join();
            }
        } else {
            System.out.println("Emergency shutdown initiated!");
            group.interrupt();
        }

        for (Thread worker : workers) {
            worker.join();
        }

        System.out.println("All client requests have been terminated.");
        System.out.println("Server shutdown completed.");
    }

    private static void processRequest(int client, int duration) {
        String name = Thread.currentThread().getName();
        System.out.println("[" + name + "] Request processing started.");
        long end = System.currentTimeMillis() + duration;

        try {
            while (System.currentTimeMillis() < end) {
                Thread.sleep(1000);
                System.out.println("[" + name + "] Processing request...");
            }
            System.out.println("[" + name + "] Request completed successfully.");
        } catch (InterruptedException e) {
            System.out.println("[" + name + "] Request cancelled.");
            Thread.currentThread().interrupt();
        }
    }
}
