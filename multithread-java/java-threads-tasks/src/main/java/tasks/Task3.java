package tasks;

import java.util.concurrent.atomic.AtomicInteger;

public class Task3 {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger completed = new AtomicInteger();

        Thread downloader = new Thread(() -> {
            try {
                for (int i = 1; i <= 20; i++) {
                    Thread.sleep(500);
                    completed.incrementAndGet();
                    System.out.println("Downloaded chunk " + i + "/20");
                }
                System.out.println("Download completed.");
            } catch (InterruptedException e) {
                System.out.println("Download cancelled. Chunks completed: " + completed.get());
                Thread.currentThread().interrupt();
            } finally {
                System.out.println("Download resources released.");
            }
        }, "Downloader");

        downloader.start();
        Thread.sleep(3500);
        downloader.interrupt();
        downloader.join();
    }
}
