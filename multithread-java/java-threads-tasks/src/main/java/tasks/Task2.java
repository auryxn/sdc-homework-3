package tasks;

public class Task2 {
    public static void main(String[] args) throws InterruptedException {
        Thread monitor = new Thread(() -> {
            try {
                while (!Thread.currentThread().isInterrupted()) {
                    System.out.println("Monitoring system...");
                    Thread.sleep(1000);
                }
            } catch (InterruptedException e) {
                System.out.println("Monitoring stopped.");
                Thread.currentThread().interrupt();
            }
        }, "Monitor");

        monitor.start();
        Thread.sleep(5000);
        monitor.interrupt();
        monitor.join();
        System.out.println("Main thread finished.");
    }
}
