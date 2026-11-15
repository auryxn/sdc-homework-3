package tasks;

public class Task5 {
    public static void main(String[] args) throws InterruptedException {
        int size = args.length > 0 ? Integer.parseInt(args[0]) : 1_000_000;
        int workers = 4;
        long[] values = new long[size];
        for (int i = 0; i < size; i++) {
            values[i] = i + 1L;
        }

        long singleStart = System.nanoTime();
        long singleSum = 0;
        for (long value : values) {
            singleSum += value;
        }
        long singleTime = System.nanoTime() - singleStart;

        long[] partialSums = new long[workers];
        Thread[] threads = new Thread[workers];
        int partSize = (size + workers - 1) / workers;

        long parallelStart = System.nanoTime();
        for (int i = 0; i < workers; i++) {
            int worker = i;
            int from = worker * partSize;
            int to = Math.min(from + partSize, size);
            threads[i] = new Thread(() -> {
                long sum = 0;
                for (int j = from; j < to; j++) {
                    sum += values[j];
                }
                partialSums[worker] = sum;
            }, "SumWorker-" + (i + 1));
            threads[i].start();
        }

        long parallelSum = 0;
        for (int i = 0; i < workers; i++) {
            threads[i].join();
            parallelSum += partialSums[i];
        }
        long parallelTime = System.nanoTime() - parallelStart;

        System.out.println("Single-thread sum: " + singleSum);
        System.out.println("Four-thread sum: " + parallelSum);
        System.out.println("Single-thread time (ms): " + singleTime / 1_000_000.0);
        System.out.println("Four-thread time (ms): " + parallelTime / 1_000_000.0);
    }
}
