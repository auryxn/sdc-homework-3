package tasks;

public class Task1 {
    public static void main(String[] args) throws InterruptedException {
        int n = args.length > 0 ? Integer.parseInt(args[0]) : 10;
        long delay = args.length > 1 ? Long.parseLong(args[1]) : 200;

        Thread up = new Thread(() -> {
            for (int i = 1; i <= n; i++) {
                System.out.println(Thread.currentThread().getName() + ": " + i);
                pause(delay);
            }
        }, "Thread-A");

        Thread down = new Thread(() -> {
            for (int i = n; i >= 1; i--) {
                System.out.println(Thread.currentThread().getName() + ": " + i);
                pause(delay);
            }
        }, "Thread-B");

        up.start();
        down.start();
        up.join();
        down.join();
    }

    private static void pause(long millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
