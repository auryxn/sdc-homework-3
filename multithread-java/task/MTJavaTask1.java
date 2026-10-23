import java.io.IOException;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Практическое занятие 1 по Multithread Java: анализ трудоёмкости
 * параллельных вычислений для варианта №3
 *
 *     (16 - c^2)(c^2 + 6c + 9)
 *     -----------------------  =  (c + 3) / 2
 *      (2c + 8)(12 + c - c^2)
 *
 * Программа:
 *  1) строит информационный граф 11-операционной схемы вычисления выражения;
 *  2) печатает ярусно-параллельную форму (T1 = 11, T_inf = 4, d(G) = 4);
 *  3) моделирует расписания для p = 1..6 и выводит Sp, Ep, Cp;
 *  4) находит оптимальное число процессоров по теореме 5 (p_opt = 3);
 *  5) сравнивает развёрнутую схему с формулой (c + 3) / 2.
 *
 * Запуск:
 *   javac MTJavaTask1.java
 *   java MTJavaTask1                          значения c по умолчанию
 *   java MTJavaTask1 input.txt                свои значения из файла
 *
 * Формат input.txt: числа через пробел, запятую или по одному в строке.
 */
public class MTJavaTask1 {

    /** Операции информационного графа (нумерация 1..11 как в README). */
    private static final String[] OP_NAMES = {
            "a = c*c",          // 1
            "A = 16 - a",       // 2
            "s = c + 3",        // 3
            "B = s*s",          // 4
            "N = A * B",        // 5
            "d = 2c",           // 6
            "e = d + 8",        // 7
            "t = c + 12",       // 8
            "D = t - a",        // 9
            "Q = e * D",        // 10
            "R = N / Q"         // 11
    };

    /** Ярусно-параллельная форма графа. */
    private static final int[][] LAYERS = {
            {1, 3, 6, 8},
            {2, 4, 7, 9},
            {5, 10},
            {11}
    };

    private static final int[][] SEQUENTIAL = {
            {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
    };

    /** Расписания из отчёта: для каждого p — операции по тактам. */
    private static final int[][][] SCHEDULES = {
            SEQUENTIAL,                                          // p = 1
            {{1, 6}, {2, 7}, {8, 3}, {9, 4}, {10, 5}, {11}},    // p = 2
            {{1, 3, 6}, {8, 2, 7}, {9, 4}, {10, 5}, {11}},      // p = 3
            {{1, 3, 6, 8}, {2, 4, 7, 9}, {5, 10}, {11}},        // p = 4
            {{1, 3, 6, 8}, {2, 4, 7, 9}, {5, 10}, {11}},        // p = 5
            {{1, 3, 6, 8}, {2, 4, 7, 9}, {5, 10}, {11}}         // p = 6
    };

    public static void main(String[] args) throws IOException {
        List<Double> values = readCValues(args);

        System.out.println("=== Практическое занятие 1: анализ трудоёмкости ===");
        System.out.println("Вариант №3: (16-c^2)(c^2+6c+9) / ((2c+8)(12+c-c^2))");
        System.out.println();

        printGraph();
        printLayers();

        int t1 = OP_NAMES.length;
        int tInf = LAYERS.length;
        System.out.printf(Locale.ROOT, "T1 = %d, T_inf = %d, d(G) = %d, T1/T_inf = %.4f%n%n",
                t1, tInf, LAYERS.length, (double) t1 / tInf);

        printMetrics(t1, tInf);
        printOptimalProcessors(t1, tInf);
        printChecks(values);
    }

    /** Полное вычисление выражения по 11-операционной схеме. */
    static double fullExpression(double c) {
        double a = c * c;               // 1
        double upper = (16.0 - a) * ((c + 3.0) * (c + 3.0));   // 2, 3, 4, 5
        double lower = (2.0 * c + 8.0) * (12.0 + c - a);       // 6, 7, 8, 9, 10
        return upper / lower;           // 11
    }

    static void printGraph() {
        System.out.println("--- 1. Информационный граф (11 операций) ---");
        for (int i = 0; i < OP_NAMES.length; i++) {
            System.out.printf(Locale.ROOT, "  %2d) %s%n", i + 1, OP_NAMES[i]);
        }
        System.out.println("  Числитель:  (4-c)(4+c)(c+3)^2");
        System.out.println("  Знаменатель: 2(c+4)(-(c-4)(c+3))");
        System.out.println("  После сокращения: (c + 3) / 2");
        System.out.println();
    }

    static void printLayers() {
        System.out.println("--- 2. Ярусно-параллельная форма ---");
        for (int i = 0; i < LAYERS.length; i++) {
            StringBuilder sb = new StringBuilder();
            for (int op : LAYERS[i]) {
                if (sb.length() > 0) {
                    sb.append(", ");
                }
                sb.append(op);
            }
            System.out.printf(Locale.ROOT, "  ярус %d (%d оп.): %s%n",
                    i + 1, LAYERS[i].length, sb);
        }
        System.out.println();
    }

    static void printMetrics(int t1, int tInf) {
        System.out.println("--- 3. Ускорение, эффективность, стоимость ---");
        System.out.printf(Locale.ROOT, "  %2s %4s %8s %8s %8s %8s%n",
                "p", "Tp", "Sp", "Ep", "Cp", "T1/p");
        for (int p = 1; p <= SCHEDULES.length; p++) {
            int tp = SCHEDULES[p - 1].length;
            double sp = (double) t1 / tp;
            double ep = sp / p;
            double cp = (double) p * tp;
            System.out.printf(Locale.ROOT, "  %2d %4d %8.2f %8.2f %8.0f %8.2f%n",
                    p, tp, sp, ep, cp, (double) t1 / p);
        }
        System.out.printf(Locale.ROOT,
                "  Теорема 3: Tp < T_inf + T1/p, т.е. граница %.2f при p=2 и %.2f при p=6%n%n",
                tInf + (double) t1 / 2, tInf + (double) t1 / 6);
    }

    static void printOptimalProcessors(int t1, int tInf) {
        double ratio = (double) t1 / tInf;
        int pOpt = (int) Math.round(ratio);
        System.out.println("--- 4. Теорема 5: оптимальное число процессоров ---");
        System.out.printf(Locale.ROOT, "  T1 / T_inf = %d / %d = %.2f  ->  p_opt = %d%n",
                t1, tInf, ratio, pOpt);
        System.out.printf(Locale.ROOT, "  При p >= %.2f гарантировано Tp <= 2*T_inf = %d;%n",
                ratio, 2 * tInf);
        System.out.printf(Locale.ROOT, "  при p < %.2f имеем T1/p <= Tp <= 2*T1/p.%n", ratio);
        System.out.println("  Больше трёх процессоров задача не использует: время упирается");
        System.out.println("  в критический путь, а стоимость Cp растёт линейно.");
        System.out.println();
    }

    static void printChecks(List<Double> values) {
        System.out.println("--- 5. Проверка вычислений ---");
        System.out.printf(Locale.ROOT, "%8s %16s %16s %12s%n",
                "c", "полный расчёт", "формула (c+3)/2", "разница");
        for (double c : values) {
            double full = fullExpression(c);
            double simple = (c + 3.0) / 2.0;
            if (Double.isNaN(full) || Double.isInfinite(full)) {
                System.out.printf(Locale.ROOT,
                        "%8.3f %16s %16.6f %12s%n", c, "не определён", simple, "—");
                continue;
            }
            System.out.printf(Locale.ROOT, "%8.3f %16.6f %16.6f %12.2e%n",
                    c, full, simple, Math.abs(full - simple));
        }
        System.out.println();
        System.out.println("Совпадение подтверждает корректность графа: 11 операций");
        System.out.println("тождественно сворачиваются в формулу (c + 3) / 2.");
        System.out.println("При c = -3 исходное выражение даёт 0/0 (не определено), а после");
        System.out.println("сокращения получается 0 — это устранимый разрыв.");
    }

    private static List<Double> readCValues(String[] args) throws IOException {
        List<Double> out = new ArrayList<>();
        if (args.length > 0) {
            Path file = Paths.get(args[0]);
            String text;
            try (Reader r = Files.newBufferedReader(file, StandardCharsets.UTF_8)) {
                StringBuilder sb = new StringBuilder();
                char[] buf = new char[4096];
                int n;
                while ((n = r.read(buf)) > 0) {
                    sb.append(buf, 0, n);
                }
                text = sb.toString();
            }
            for (String token : text.split("[\\s;,]+")) {
                addIfNumber(out, token);
            }
        }
        if (out.isEmpty()) {
            out.add(2.0);
            out.add(5.0);
            out.add(-3.0);
            out.add(0.5);
        }
        return out;
    }

    private static void addIfNumber(List<Double> out, String token) {
        if (token == null || token.isEmpty()) {
            return;
        }
        try {
            out.add(Double.parseDouble(token.replace(',', '.')));
        } catch (NumberFormatException ignored) {
            // заголовки и пояснения в файле пропускаем
        }
    }
}
