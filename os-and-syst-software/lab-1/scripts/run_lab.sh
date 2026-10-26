#!/usr/bin/env bash
# Lab 1 (OS And Syst Software): environment, build stages, debugging.
#
# Linux (recommended):  bash scripts/run_lab.sh
# macOS (fallback):     bash scripts/run_lab.sh
#
# On Linux the script uses gcc + gdb; on macOS it uses Apple clang + lldb,
# because macOS has no native gcc/gdb (see README, section "Окружение").

set -u
cd "$(dirname "$0")/.."

OUT=artifacts/lab-output.txt
mkdir -p artifacts build
: > "$OUT"

OS=$(uname -s)
if [ "$OS" = "Darwin" ]; then
  CC=${CC:-clang}
  DBG=${DBG:-lldb}
  DBG_SCRIPT=scripts/lldb_script.txt
else
  CC=${CC:-gcc}
  DBG=${DBG:-gdb}
  DBG_SCRIPT=scripts/gdb_script.txt
fi

section() {
  { echo; echo "==================================================================="
    echo "$*"
    echo "==================================================================="; } | tee -a "$OUT"
}

run() {
  { echo; echo "\$ $*"; } | tee -a "$OUT"
  "$@" 2>&1 | tee -a "$OUT"
  echo "[exit code: ${PIPESTATUS[0]}]" | tee -a "$OUT"
}

section "1. Окружение"
run uname -a
{ echo; echo "\$ $CC --version"; } | tee -a "$OUT"
"$CC" --version 2>&1 | head -3 | tee -a "$OUT"
{ echo; echo "\$ $DBG --version"; } | tee -a "$OUT"
"$DBG" --version 2>&1 | head -3 | tee -a "$OUT"
{ echo; echo "\$ make --version"; } | tee -a "$OUT"
make --version 2>&1 | head -1 | tee -a "$OUT"

section "2. Сборка hello.c из командной строки"
run cat src/hello.c
run "$CC" -g -O0 src/hello.c -o build/hello
run ./build/hello
{ echo; echo "\$ echo \$?"; } | tee -a "$OUT"
./build/hello >/dev/null; echo $? | tee -a "$OUT"

section "3. Программа «сумма двух чисел»"
run cat src/sum.c
run "$CC" -g -O0 src/sum.c -o build/sum
{ echo; echo "\$ printf '12\\n30\\n' | ./build/sum"; } | tee -a "$OUT"
printf '12\n30\n' | ./build/sum 2>&1 | tee -a "$OUT"

section "4. Стадии сборки: препроцессор, компиляция, компоновка"
run "$CC" -E src/hello.c -o build/hello.i
run "$CC" -c src/hello.c -o build/hello.o
run "$CC" build/hello.o -o build/hello_linked
run ./build/hello_linked
{ echo; echo "\$ wc -l src/hello.c build/hello.i"; } | tee -a "$OUT"
wc -l src/hello.c build/hello.i 2>&1 | tee -a "$OUT"
{ echo; echo "\$ file build/hello.o build/hello"; } | tee -a "$OUT"
file build/hello.o build/hello 2>&1 | tee -a "$OUT"

section "5. Отладка: точка останова, Step Over и Step Into"
{ echo; echo "\$ $DBG --batch -s $DBG_SCRIPT build/sum"; } | tee -a "$OUT"
if [ "$DBG" = "lldb" ]; then
  lldb --batch -s "$DBG_SCRIPT" build/sum 2>&1 | tee -a "$OUT"
else
  gdb --batch -x "$DBG_SCRIPT" build/sum 2>&1 | tee -a "$OUT"
fi
echo "[exit code: ${PIPESTATUS[0]}]" | tee -a "$OUT"

section "6. Намеренная ошибка: без #include <stdio.h>"
run cat src/noinclude.c
run "$CC" -g -O0 src/noinclude.c -o build/noinclude

section "7. Намеренная ошибка: вызов функции без определения"
run cat src/badcall.c
run "$CC" -g -O0 src/badcall.c -o build/badcall

section "Готово"
echo "Полный лог сохранён в $OUT" | tee -a "$OUT"
