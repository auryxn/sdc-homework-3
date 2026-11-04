/*
 * Лабораторная работа №2 — Анатомия памяти процесса и указатели
 *
 * Программа разделена на этапы; нужный этап выбирается аргументом:
 *   ./lab2 1        — карта сегментов (ждёт Enter, чтобы посмотреть /proc/<PID>/maps)
 *   ./lab2 2        — рост стека до Segmentation Fault
 *   ./lab2 3        — побайтовый дамп числа (Little-Endian)
 *   ./lab2 4        — утечка памяти
 *   ./lab2 4 fixed  — та же программа, но с free()
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv);

/* .data — глобальная с инициализатором */
int global_init = 42;
/* .bss — глобальная без инициализатора */
int global_uninit;

/* ------------------------------------------------------------------ */
/* Этап 1. Карта памяти процесса                                      */
/* ------------------------------------------------------------------ */
void stage1(void)
{
    int local = 7;

    void *heap = malloc(100);
    if (heap == NULL) {
        perror("malloc");
        exit(1);
    }

    printf("PID:            %d\n", getpid());
    printf(".data (global_init): %p\n", (void *)&global_init);
    printf(".bss  (global_uninit): %p\n", (void *)&global_uninit);
    printf("heap  (malloc(100)):  %p\n", heap);
    printf("stack (local):        %p\n", (void *)&local);
    printf(".text (main):         %p\n", (void *)main);

    printf("\nEnter, чтобы завершить программу...\n");
    getchar();

    free(heap);
}

/* ------------------------------------------------------------------ */
/* Этап 2. Рост стека и переполнение                                  */
/* ------------------------------------------------------------------ */
void test_stack(int depth)
{
    char buffer[1024];

    /* чтобы компилятор не выбросил буфер и не «оптимизировал» рекурсию */
    buffer[0] = (char)depth;

    printf("depth = %5d, &buffer[0] = %p\n", depth, (void *)&buffer[0]);
    fflush(stdout);

    test_stack(depth + 1);
}

void stage2(void)
{
    printf("Начинаем рекурсию, стек: ulimit -s = 8192 КБ\n");
    test_stack(1);
}

/* ------------------------------------------------------------------ */
/* Этап 3. «Сырая» память и Little-Endian                             */
/* ------------------------------------------------------------------ */
void stage3(void)
{
    uint32_t x = 0x41424344;
    unsigned char *ptr = (unsigned char *)&x;

    printf("x = 0x%08X, sizeof(x) = %zu\n", x, sizeof(x));
    for (size_t i = 0; i < sizeof(x); i++) {
        printf("байт %zu: адрес %p  hex %02X  символ '%c'\n",
               i, (void *)(ptr + i), ptr[i],
               (ptr[i] >= 32 && ptr[i] < 127) ? ptr[i] : '.');
    }
}

/* ------------------------------------------------------------------ */
/* Этап 4. Утечка памяти                                              */
/* ------------------------------------------------------------------ */
void stage4(int fixed)
{
    const int n = 10;
    int *arr = malloc(n * sizeof(int));
    if (arr == NULL) {
        perror("malloc");
        exit(1);
    }

    for (int i = 0; i < n; i++) {
        arr[i] = i * i;
    }
    printf("arr[9] = %d\n", arr[9]);

    if (fixed) {
        free(arr);
        printf("free(arr) выполнен\n");
    } else {
        printf("free(arr) забыт — Valgrind должен найти утечку\n");
    }
}

/* ------------------------------------------------------------------ */
int main(int argc, char **argv)
{
    int stage = (argc > 1) ? atoi(argv[1]) : 1;

    switch (stage) {
    case 1:
        stage1();
        break;
    case 2:
        stage2();
        break;
    case 3:
        stage3();
        break;
    case 4:
        stage4(argc > 2 && strcmp(argv[2], "fixed") == 0);
        break;
    default:
        fprintf(stderr, "usage: %s {1|2|3|4 [fixed]}\n", argv[0]);
        return 1;
    }
    return 0;
}
