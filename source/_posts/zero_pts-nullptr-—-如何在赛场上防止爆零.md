---
title: ZERO_PTS = nullptr — 如何在赛场上防止爆零
date: 2026-10-27 19:56:00
tags:
  - OI
categories:
  - OI
---
每年 CSP/NOIP 比赛上，我们总会发现这样的东西：


```cpp
//freopen("candy.in", "r", stdin);
```

```cpp
cout << "DEBUG a = " << a << endl;
```

这种东西出现在代码里的结局基本上是：

```
Wrong Answer 0/0
```

于是就有了这篇文章。

### 一：文件和路径

进考场的第一件事必须是看一下题目里有没有这些字眼：`子目录||目录名||子文件夹`，没有的话问老师，每年都有因为没开subdir爆零的。

即使你开了对应路径的文件，我还是建议你这样做：

```bash
# 根目录 -> 子目录
# Windows
C:/path/to/GD-Sxxxxx > mklink -h prob/prob.cpp prob.cpp
# Linux
/path/to/GD-Sxxxxx $ ln prob.cpp prob/prob.cpp

```

从子目录到根目录就反过来，这可以使你在忘记开字目录时有最基本的保险，但硬链接在移动文件后就会失效，请务必确认是否需要子目录，并且在对应目录中编辑文件。

对于任何从题面读取的文件名、字面量和输出信息，我们都强烈建议复制粘贴，而不是手动输入。

### 二：输入与输出


**前置知识**：使用如下的代码来控制编译结果：

```cpp
// 仅在 -DSTH 时编译
#ifdef STH
...
#endif

// 仅在 -DSTH 时跳过
#ifndef STH
...
#endif
```

在考场上手动注释/解除注释 `freopen()` 行是危险的，很容易忘记，推荐这样做：

```cpp
#ifndef DEBUG
freopen("name.in", "r", stdin);
freopen("name.out", "w", stdout);
#endif
```

如果你使用 IDE，在编译选项添加 `-DDEBUG`，如果你使用 CLI 编译，编译时添加 `-DDEBUG`。

在本地测试时，你可以通过这个命令来将标准 IO 重定向到文件：

```bash
# 通用，但请区分扩展名
./a.(exe/out) < prob.in > prob.out
```

这将从 prob.in 读入，输出到 prob.out

关于 IO 优化的内容，参见“时间和空间”。

### 三：域和数据类型

先记住几个数，它们在考场上比什么都重要：

| 类型 | 范围 | 大致 |
| --- | --- | --- |
| `int` | `-2^31 ~ 2^31-1` | `±2.1e9` |
| `unsigned int` | `0 ~ 2^32-1` | `4.3e9` |
| `long long` | `-2^63 ~ 2^63-1` | `±9.2e18` |
| `size_t` | `0 ~ 2^64-1`（64 位 Linux） | `1.8e19` |

爆 `int` 的高发场景，如果发生这几个之一就要开 long long：

1. 两个 `1e9` 相乘：`int a = 1e9; a * a`。
2. 前缀和 / 差分：`n = 1e5`，`a_i = 1e9`，`sum` 是 `1e14`。
3. 最短路 / DP 的代价累加。Dijkstra 的 `dist` 必须是 `long long`，`INF` 要用 `1e18` 而不是 `INT_MAX`。
4. 组合数 `C(n, m)` 的中间乘积。
5. 答案要取模，但中间过程没取。
6. `n * (n - 1) / 2` 在 `n = 1e5` 时是 `5e9`。
7. 答案本身没爆，但算答案的加法爆了。

```cpp
int a = 1e9;
long long b = a * a;             // 错：先按 int 乘，已经 UB，再转 long long 救不回来
long long c = 1ll * a * a;       // 对：显式提升
long long d = (long long)a * a;  // 对
```

规则：

- 拿不准就用 `long long`，代价只是内存翻倍和一点点常数。
- 但数组下标、循环变量、存边用 `int`，不要全上 `long long`：慢，而且容易 MLE。
- 转换要发生在计算之前，不是计算之后（见上）。
- 常量一律加后缀：`1ll << 60`、`4e18`、`0x3f3f3f3f3f3f3f3fll`。
- `INF` 用 `0x3f3f3f3f3f3f3f3f`，两个 `INF` 相加也不会溢出（约 `9.1e18`，仍小于 `9.2e18`）；不要用 `LLONG_MAX` 或 `INT_MAX` 去做加法。
- 输出用 `%lld` 或 `cout`。如果你使用 `#define int long long` 和 C 风格 IO，你需要时刻记住你的类型不是 `int`。
- `main()` 需要返回严格 `int`，使用 `signed` 以在 `#define int long long` 时访问这个类型。
- `abs(INT_MIN)` 是 UB。取绝对值前先转 `long long`，用 `llabs`。

无符号的坑：

```cpp
for (unsigned i = n - 1; i >= 0; --i)   // 死循环，i 永远 >= 0
s.size() - 1                            // 空串时回绕成 size_t 的最大值
```

`s.size()` 返回的是 `size_t`（`unsigned long long int`）。空串时 `s.size() - 1` 会回绕成 `size_t` 的最大值：**64 位评测机上是 `18446744073709551615`，而不是 `4294967295`**（后者只有 32 位平台才成立）。这个值拿去当数组下标，结果就是越界 RE，而且报错信息完全指不到这里。

`unsigned` 的减法回绕非常“合法”，编译器不会警告你，只会静静地错。

`char` 的坑：

- `char` 是否有符号是**实现定义**的（x86 上一般有符号，ARM 上可能无符号）。处理字节值请用 `unsigned char`。
- `isspace(c)`、`isdigit(c)` 传入负值 UB，先转 `(unsigned char)`。

浮点的坑：

- 不要用 `==` 比较，用 `fabs(x - y) < eps`。
- `1 / 2` 是 `0`，`1.0 / 2` 才是 `0.5`。
- C++ 向零取整（C++11 起标准明确规定）：`-5 / 2 == -2`，`-5 % 2 == -1`。涉及负数取模写 `(x % mod + mod) % mod`。
- `long double` 在 Linux x86 上是 80-bit，Windows/MinGW 上实现和 `printf` 支持都有差异，输出时转 `double` 或用 `cout`。

**不推荐使用 `__int128`！**

理由：

1. **没有标准 IO**。`cin` / `cout` / `printf` 都不支持，必须手写读入输出，写错就是 0 分。
2. **字面量麻烦**。只能写 `(__int128)1 << 100`，不能直接写 `1e30`（那是浮点）。
3. **支持不一**。一些老旧编译器也不支持；本地能编译不等于评测机能编译。
4. **慢**。加减只是多几条指令，但乘除和取模会调软件模拟的库函数，除法能慢一个数量级，卡常时雪上加霜。
5. **不好调试**。`cin` / `cout` / `printf` 都不认它，调试器里显示也麻烦，得自己写 `print128`。
6. **编译器 Bug**。使用 `__int128` 作为数组下标是严重的未定义行为。

真需要 128 位时，先想想是不是解法有问题：

- 需要取模的，就是忘了取模。
- 需要 `2^64` 哈希的，用 `unsigned long long` 自然溢出即可。
- 题目明确要求高精度的，用高精度模板。

### 四：时间和空间

#### IO 优化

```cpp
ios::sync_with_stdio(false);
cin.tie(nullptr);
```

这是基操。注意：

- 关闭同步之后，不要再混用 `printf` / `scanf` 和 `cin` / `cout`。两者的缓冲各管各的，标准不保证先后顺序（这不是 UB，但结果由实现决定），最后输出会乱。
- 用 `'\n'` 而不是 `endl`。`endl` 每次都会 flush，在 `1e6` 行输出里是致命的。
- 输出量特别大（百万行以上）时，考虑快读快写。

**`cout` 无需关流**。`cout.tie()` 本来就是 0，尽管很多人这么做，但给 `cout` 关流是无意义的。

#### 快读快写

```cpp
namespace fastio 
{
const int BUF = 1 << 20;
unsigned char ibuf[BUF];   // 必须是 unsigned char，见下面的说明
char obuf[BUF];
int ipos = 0, ilen = 0, opos = 0;

inline int gc() 
{
    if (ipos == ilen) 
    {
        ilen = (int)fread(ibuf, 1, BUF, stdin), ipos = 0;
        if (!ilen) return -1;
    }
    return ibuf[ipos++];
}

inline void flush() 
{
    if (opos) fwrite(obuf, 1, opos, stdout), opos = 0;
}

template <class T>
inline bool read(T &x) 
{
    int c = gc(), neg = 0;
    while (c != '-' && (c < '0' || c > '9')) 
    {
        if (c < 0) return false;
        c = gc();
    }
    if (c == '-') neg = 1, c = gc();
    unsigned long long u = 0;
    for (; c >= '0' && c <= '9'; c = gc()) u = u * 10 + (unsigned)(c - '0');
    x = neg ? (T)(0ull - u) : (T)u;
    return true;
}

template <class T>
inline void write(T x) 
    {
    unsigned long long u;
    if (x < 0) obuf[opos++] = '-', u = 0ull - (unsigned long long)x;
    else u = (unsigned long long)x;
    static char s[24];
    int n = 0;
    do s[n++] = char(u % 10 + '0'), u /= 10; while (u);
    while (n) obuf[opos++] = s[--n];
    obuf[opos++] = '\n';
    if (opos > BUF - 40) flush();
}
} // namespace fastio
```

注意几点：

1. **`ibuf` 必须是 `unsigned char`**。`char` 在 x86 上是有符号的，缓冲区里 `0x80` 以上的字节会被符号扩展成负数，然后被 `if (c < 0) return false;` 当成 EOF——程序会莫名其妙地提前停止读入。`gc()` 返回 `int` 也是同一个道理：`EOF` 是 `-1`，返回值必须是能表示 `-1` 的类型。
2. **`long long` 的最小值要特殊处理**。`-9223372036854775808` 取负会溢出，所以先按 `unsigned long long` 累加，最后 `0ull - u` 再转回去；`write` 同理。
3. `write` 用了缓冲，**退出前必须 `flush()`**，或者 `atexit(fastio::flush);`，否则最后一段输出会丢。
5. 不要用 `getchar_unlocked`，它是 POSIX 扩展，Windows 上没有。

另外，这套 `read` / `write` 只对**带符号**类型保证正确。`write` 里的 `x < 0` 判断对 `unsigned` 没有意义，别往里传 `unsigned`。

另外记住：**快读只能救常数，救不了算法**。`1e5` 的题不写快读也能过，`1e6` 的题写了快读也未必过。先把复杂度写对。

#### 复杂度估算

- 一秒大约 `1e8` 次基本操作。官方机可能快一些，但按 `1e8` 估不会错。
- `n = 1e5` 的 `O(n log n)` 约 `1.7e6`，随便过。
- `n = 1e6` 的 `O(n log n)` 约 `2e7`，稳。
- `n = 1e5` 的 `O(n sqrt n)` 约 `3e7`，可以。
- 纯 `1e9` 次操作基本就是 TLE，除非循环体极简。
- 递归、取模、内存随机访问、STL 都会让常数变大，估算时留 3~5 倍余量。

#### 空间估算

- `25MB ≈ 6e6` 个 `int`，或 `3e6` 个 `long long`。
- `256MB ≈ 6.7e7` 个 `int`。
- 二维数组是 `n × m × sizeof`。`1e3 × 1e3` 的 `int` 是 `4MB`，`1e4 × 1e4` 就是 `400MB`。
- 局部数组在栈上：Windows 默认只有 `1~2MB`（取决于工具链），很容易 RE；Linux 是 `8MB`。**大数组一律放全局或 `static`。**
- `vector` 的 `push_back` 先 `reserve`；`clear()` 不释放内存，多测时要小心。
- 递归深度 `1e5` 在 Windows 上会爆栈：加 `-Wl,--stack=67108864`，或者手写栈。
- `unordered_map` 的常数和内存都比你想的大，还可能被卡哈希。

### 五：调试和日志

**用 `cerr`，不要用 `cout`。**

```cpp
#ifdef DEBUG
#define dbg(...) fprintf(stderr, __VA_ARGS__)
#else
#define dbg(...) ((void)0)
#endif
```

为什么是 stderr：

1. `freopen("name.out", "w", stdout)` 之后，`cout` 的内容会进答案文件，`cerr` 不会，这一点能在忘记删调试代码时挽救程序。
2. `./a < name.in > name.out` 之后，`cerr` 的内容仍然打在屏幕上，而 `cout` 进了文件。

为什么“不要用 `cout`”：`cout` 是缓冲的，程序崩溃时缓冲区里没 flush 的内容全丢了，你看到的日志可能停在很久以前，直接误导判断。

但 `cerr` 很慢：循环里 `cerr` 打 `1e6` 次必然 TLE。所以要用 `#ifdef DEBUG` 关掉，而不是手动注释。

其他调试习惯：

- 本地编译开 `-Wall -Wextra -Wconversion -Wshadow`，能提前抓出一大片隐式转换和未使用变量的警告，也可以抓出 `for (int j = 1; j <= n; i++` 这种东西。
- 有条件再开 `-fsanitize=address,undefined`：ASan 在 MinGW 上基本用不了，要到 VirtualBox 的 Linux 里开，能提前抓出 UBSan 报的 UB。
- 不要 `system("pause")`、`system("cls")`：Linux 上根本没有，Windows 上也未必让用。
- 不要在提交的代码里留 `for (int i = 0; i < n; i++) cerr << a[i];`，这一行会让评测机 TLE——用宏关掉。
- 多测记得打印 case 编号，否则你根本不知道是第几组挂的。

### 六：数据和字面量

**再次提醒：考场上所有字面量请一定使用 ^C/^V 不要自己输入！！！**

#### 模数

```cpp
const int MOD = 1e9 + 7;      // 能编译，值也对，但不推荐
const int MOD = 1000000007;   // 推荐，一眼能对
#define MOD 1e9 + 7           // 灾难
```

- `1e9 + 7` 是 `double`。宏展开之后 `x % MOD` 变成 `x % 1e9 + 7`，`%` 不接受浮点操作数，**必定编译报错**——这还算好的，至少当场就发现了。真正隐蔽的是 `const int M = MOD;`、`memset(a, MOD, n)` 这类上下文：`double` 会被静默转成 `int`，错得无声无息。
- 常见模数背下来：`1000000007`（1e9+7）、`1000000009`（1e9+9）、`998244353`、`100000007`（1e8+7）。

#### 初始化和 memset

- `memset` 只能按**字节**赋值：`0` → `0x00000000`，`-1` → `0xffffffff`，`0x3f` → `0x3f3f3f3f`（常用来当 `INF`）。
- `memset(a, 1e9, sizeof a)` 是错的：`1e9` 被截成一个字节，恰好是 `0`，等于 `memset(a, 0, ...)`。
- `memset` 是 O(字节数) 的。`1e7` 个 `int` 要写 `4e7` 字节，多测时它也是常数开销。

#### 字面量和运算符优先级

- `1 << 31` 在 C++20 以前是 UB（有符号左移溢出），写 `1ll << 31` 或 `1u << 31`。评测大多还是 C++14/17，按 UB 处理就对了。
- `a & b == c` 是 `a & (b == c)`：位运算优先级低于比较。
- `a << 2 + 3` 是 `a << (2 + 3)`：加法优先级高于左移。
- `-5 / 2` 是 `-2`，`-5 % 2` 是 `-1`，C++ 向零取整。
- `'a'` 是字符，`"a"` 是字符串；`'\n'` 是字符，`"\n"` 是字符串。写 `map<char, ...>` 时别插 `"a"`。

#### 用管道测试本地数据

```bash
./a.out < prob.in > prob.out        # 从文件读
cat prob.in | ./a.out > prob.out    # 从管道读
./gen 1000 | ./a.out                # 现场造数据，不落盘
```

比对输出：

```bash
diff -w a.out b.out                     # -w：忽略所有空白差异（行首、行内、行尾）
diff -Z a.out b.out                     # -Z：只忽略行尾空白，行内空格不同照样报
diff --strip-trailing-cr -w a.out b.out # 一边是 CRLF 一边是 LF 时，先把 \r 剥掉
diff <(./a.out < in) exp.out            # 直接比，不用落地
```

`-w` 会把 “该有空格的地方没空格” 也放过去，对拍时它只负责帮你快速定位差异，最终还是要按原样比一遍。

Windows 上生成的数据是 CRLF，Linux 上是 LF。把 Windows 的 `.in` 拿到 VirtualBox 里测，程序可能把 `\r` 当成字符读进去，Linux 里这样解决：

```bash
sed -i 's/\r$//' prob.in
```

### 七：测试和提交

#### 在 VirtualBox 里测

- 评测机是 Linux（一般是 Ubuntu + GCC），Windows 上能过不代表 Linux 能过：栈大小、`long double`、**文件名大小写**、`-O2` 下的 UB 行为都可能不同。
- `bits/stdc++.h` 在 MinGW 和 Linux 的 GCC 上都有；但 MSVC 没有。
- 在 VirtualBox 里用 `g++ -O2 -std=c++14` 编译一遍，再用命令行跑一遍最大数据。

#### 从 VirtualBox 复制到 Windows

- 共享文件夹、剪贴板粘贴都可以，**但复制之后一定要重新验一遍文件内容**。
- 复制完对比两端哈希（`sha256sum file.cpp`），或者干脆打开文件确认最后一行没被截断。剪贴板粘贴丢最后一行是真实发生过的事。

#### 检查文件结构

```bash
tree        # 或者 ls -R
```

提交前确认：

- 题目要求子目录的，`subdir` 是否建好、目录名是否与题面一致（Linux 区分大小写）。
- 文件名的大小写：题目要求 `prob.cpp`，你写的是 `Prob.cpp`，Windows 不区分，Linux 评测机找不到。
- 扩展名不是隐藏的 `.cpp.txt`（Windows 默认隐藏扩展名，这是经典事故），在 Windows 下关闭 `文件夹和视图选项 -> 隐藏已知文件的扩展名`。
- 文件编码是 UTF-8 无 BOM；GBK 中文注释在 GCC 下可能直接报错，检查时用记事本打开，然后看右下角是否是 `UTF-8`。

#### 提交前 checklist

- [ ] `freopen` 的文件名与题面**完全一致**（大小写、扩展名）
- [ ] 目录名 / subdir 正确
- [ ] 调试输出已用 `#ifdef DEBUG` 关掉（或者更保险地注释掉），没有裸的 `cerr` / `cout` 调试语句
- [ ] 没有 `system("pause")`，没有硬编码的本地路径（注意不要 `freopen` 里写类似 `down/prob/prob.in` 这种）
- [ ] 用 `-O2 -std=c++14` 编译能过
- [ ] 用最大数据跑过一遍，`time` 在时限内（或者至少是能实现的部分）

### 后记

差不多就写这些了，希望大家 CSP/NOIP 考场上认真答题，远离爆零。
