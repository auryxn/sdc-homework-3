package tasks;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class Task11 {
    private final ThreadGroup group = new ThreadGroup("FileSearch");
    private final List<Thread> workers = new ArrayList<>();
    private final AtomicInteger threadNumber = new AtomicInteger();
    private final AtomicInteger filesProcessed = new AtomicInteger();
    private final AtomicInteger matchesFound = new AtomicInteger();
    private final ThreadFactory threadFactory = task ->
            new Thread(group, task, "FileSearch-" + threadNumber.incrementAndGet());

    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java tasks.Task11 <directory> <regex>");
            return;
        }

        Task11 manager = new Task11();
        try {
            manager.search(Path.of(args[0]), Pattern.compile(args[1]));
        } catch (IOException e) {
            System.out.println("Could not search directory: " + e.getMessage());
        }
    }

    private void search(Path root, Pattern pattern) throws IOException {
        System.out.println("Starting search in: " + root);
        System.out.println("Search pattern: " + pattern);

        try (Stream<Path> paths = Files.walk(root)) {
            paths.filter(Files::isRegularFile).forEach(path -> startWorker(path, pattern));
        }

        try {
            for (Thread worker : workers) {
                worker.join();
            }
            System.out.println("Search completed!");
            System.out.println("Files processed: " + filesProcessed.get());
            System.out.println("Total matches: " + matchesFound.get());
        } catch (InterruptedException e) {
            for (Thread worker : workers) {
                worker.interrupt();
            }
            for (Thread worker : workers) {
                try {
                    worker.join();
                } catch (InterruptedException ignored) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
            Thread.currentThread().interrupt();
            System.out.println("Search cancelled.");
        }
    }

    private void startWorker(Path path, Pattern pattern) {
        Thread worker = threadFactory.newThread(() -> searchFile(path, pattern));
        workers.add(worker);
        worker.start();
    }

    private void searchFile(Path path, Pattern pattern) {
        String name = Thread.currentThread().getName();
        System.out.println("[" + name + "] Searching in file: " + path.getFileName());

        try (Stream<String> lines = Files.lines(path, StandardCharsets.UTF_8)) {
            lines.forEach(line -> {
                if (Thread.currentThread().isInterrupted()) {
                    return;
                }
                Matcher matcher = pattern.matcher(line);
                while (matcher.find()) {
                    System.out.println("[" + name + "] Match found: " + line);
                    matchesFound.incrementAndGet();
                }
            });
            filesProcessed.incrementAndGet();
        } catch (IOException e) {
            System.out.println("[" + name + "] Could not read file: " + e.getMessage());
            filesProcessed.incrementAndGet();
        }
    }
}
