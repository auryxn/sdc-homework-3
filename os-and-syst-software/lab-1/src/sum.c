#include <stdio.h>

int add(int a, int b) {
    int result = a + b;
    return result;
}

int main(void) {
    int num1, num2, sum;

    printf("Введите первое число: ");
    scanf("%d", &num1);

    printf("Введите второе число: ");
    scanf("%d", &num2);

    sum = add(num1, num2);
    printf("Сумма: %d\n", sum);
    return 0;
}
