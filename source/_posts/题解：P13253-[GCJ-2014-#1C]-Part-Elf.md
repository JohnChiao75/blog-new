---
title: 题解：P13253 Part Elf
date: 2026-05-16 11:05
tags: 洛谷
category: 题解
author: JohnChiao75
---



## 形式化题意

给定一个分数 $\frac{P}{Q}$，它是由若干个分数的平均值构成的。构造一个数列，其中每个数要么为 $1$（即 $\frac11$），要么为 $0$（即 $\frac00$），输出至少经过几次平均运算才能从这样的数列构造出 $\frac{P}{Q}$。

（注：因为 $\frac{P}{Q}$ 是由平均值得来的，所以 $0 \le \frac{P}{Q} \le 1$。）

### 示例

分数为 $\frac14$，可以由下式得出：
$$
\large{\frac{\frac{0}{1}+\frac{1}{2}}{2}}
$$

## 思路

由于目标分数是由多次平均值得出的，分母只通过通分运算和乘以 $\frac12$ 的运算改变，因此可以证明：有效的目标分数分母一定为 $2$ 的幂次。

如果分母不为 $2$ 的幂次，直接判否，输出 `impossible`。

同样可以证明：约分后的分子 $\frac{P}{\gcd(P,Q)}$ 为奇数（即不含因数 $2$）。

可以将这个题目想象为一棵二叉树，底部的每一对节点对目标分数的贡献相当于 $\log_2 n$。要得到分子 $P$，在每一层（作为叶子）需要的 $1$ 和 $0$ 的数量是恒定的，只需找到可以容纳这些数的最低层数 $k$ 即可。

## 代码

:::success[AC Code]
```cpp line-numbers
#include<bits/stdc++.h>
#define int long long

using namespace std;

signed main()
{
	int T;
	cin >> T;
	for (int i = 1; i <= T; i++)
	{
		int p, q;
		char _;
		cin >> p >> _ >> q;
		cout << "Case #" << i << ": ";
		int g = __gcd(p, q);
		p /= g;
		q /= g;
		int q1 = q;
		int j = 0;
		while (q1 % 2 == 0)
		{
			q1 /= 2;
			j++;
		}
		if (q1 != 1)
		{
			cout << "impossible" << endl;
			continue;
		}
		int ans = INT_MIN;
		for (int k = 1; k <= 40; k++)
			if (p * (1ll << k) >= q)
			{
				ans = k;
				break;
			}
		if (ans != INT_MIN)
			cout << ans << endl;
		else
			cout << "impossible"<<endl;
	}
	return 0;
}

```
:::
