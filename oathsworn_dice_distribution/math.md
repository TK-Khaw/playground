## Number of probability distributions given a maximum number of rolls
Number of probability distributions given a maximum number of rolls $N$ and $n$ die choices is essentially the same as
finding $n + 1$ integers, $x_i, i \in \set{0,1, \cdots, n}, x_i \in \mathbb{Z}_0^+$ that sums up to $N$. The number 
of components is $n+1$ because we need to
consider cases where sum of dice is not equal to $N$, essentially the $+1$ is for "absence of die", if that make sense.

We can consider this problem as slicing a line of length $N$ for a number of times lesser than or equal
to $n$. 

$$
N = x_0 + x_1 + \cdots + x_n
$$

Now first let us consider cases where $x_i \in \mathbb{Z}^+$. The number of possible combinations, let's denote it as
$\nu_0$, is thus,

$$
\nu_0 = {}^{N-1}C_{n}
$$

where one can think of it as slicing up the line to $n+1$ lines of finite integer length.

Now, let us consider what happen if one of the component $x_i$ is zero. We now slice the line into only $n$ components. Thus,

$$
{}^{N-1}C_{n-1}
$$

But realize that we need to decide who is the "zero". There is $n+1$ ways of choosing the "zero". Generalizing the expression would
be to say that there ${}^{n+1}C_{1}$ ways of choosing the "zero". That is to say,

$$
\nu_1 = {}^{n+1}C_{1} \cdot {}^{N-1}C_{n-1}
$$

Looking back at $\nu_0$, we realize that 

$$
\nu_0 = {}^{n+1}C_{0} \cdot {}^{N-1}C_{n}
$$

Notice that this can be generalize to $\nu_i, i \in \set{0,1, \cdots, n}$

$$
\nu_i = {}^{n+1}C_{i} \cdot {}^{N-1}C_{n-i}
$$

Thus, the total number of probability distribution for a maximum number of rolls is,

$$
\nu = \nu_0 + \nu_1 + \cdots + \nu_n - 1
$$

$$
\nu = \sum_{i=0}^{n}{ {}^{n+1}C_{i} \cdot {}^{N-1}C_{n-i} } - 1
$$

Remember that there's one component that represents "absense of die", which we need to take out of the final number.
Nobody wants to roll zero number of die! ;)
