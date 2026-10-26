#include <stdio.h>

/* Объявление есть, определения нигде нет: ошибка должна возникнуть на компоновке. */
int does_not_exist(void);

int main(void) {
    printf("before\n");
    does_not_exist();
    printf("after\n");
    return 0;
}
