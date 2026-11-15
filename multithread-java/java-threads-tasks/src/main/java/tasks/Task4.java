package tasks;

import java.util.Random;

public class Task4 {
    public static void main(String[] args) throws InterruptedException {
        Thread[] athletes = new Thread[3];
        String[] names = {"Alex", "Max", "Sam"};
        Random random = new Random();

        for (int i = 0; i < athletes.length; i++) {
            String name = names[i];
            athletes[i] = new Thread(() -> {
                System.out.println(name + " started the race.");
                int steps = 3 + random.nextInt(4);
                for (int j = 0; j < steps; j++) {
                    try {
                        Thread.sleep(300 + random.nextInt(700));
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                }
                System.out.println(name + " finished the race.");
            }, "Athlete-" + (i + 1));
        }

        for (Thread athlete : athletes) {
            athlete.start();
        }
        for (Thread athlete : athletes) {
            athlete.join();
        }
        System.out.println("All athletes finished. Final results are ready.");
    }
}
