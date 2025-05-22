---
title: Codon Documentation
template: homepage.html
---
# Welcome to Codon!

Codon is a high-performance Python implementation that compiles to native machine code without
any runtime overhead. Typical speedups over vanilla Python are on the order of 10-100x or more, on
a single thread. Codon's performance is typically on par with (and sometimes better than) that of
C/C++. Unlike Python, Codon supports native multithreading, which can lead to speedups many times
higher still.

*Think of Codon as Python reimagined for static, ahead-of-time compilation, built from the ground
up with best possible performance in mind.*

## Goals

- :bulb: **No learning curve:** Be as close to CPython as possible in terms of syntax, semantics and libraries
- :rocket: **Top-notch performance:** At *least* on par with low-level languages like C, C++ or Rust
- :computer: **Hardware support:** Full, seamless support for multicore programming, multithreading (no GIL!), GPU and more
- :chart_with_upwards_trend: **Optimizations:** Comprehensive optimization framework that can target high-level Python constructs
  and libraries
- :battery: **Interoperability:** Full interoperability with Python's ecosystem of packages and libraries

## Non-goals

- :x: *Drop-in replacement for CPython:* Codon is not a drop-in replacement for CPython. There are some
  aspects of Python that are not suitable for static compilation — we don't support these in Codon.
  There are ways to use Codon in larger Python codebases via its [JIT decorator](interop/decorator.md)
  or [Python extension backend](interop/pyext.md). Codon also supports
  calling any Python module via its [Python interoperability](interop/python.md).
  See also [*"Differences with Python"*](intro/differences.md) in the docs.

- :x: *New syntax and language constructs:* We try to avoid adding new syntax, keywords or other language
  features as much as possible. While Codon does add some new syntax in a couple places (e.g. to express
  parallelism), we try to make it as familiar and intuitive as possible.

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Set up in 1 minute__

    ---
    Run the following command to install Codon:
    ```bash
    /bin/bash -c "$(curl -fsSL https://exaloop.io/install.sh)"
    ```

    [:octicons-arrow-right-24: Getting started](/intro/intro.md)

-   :fontawesome-brands-python:{ .lg .middle } __It's Pythonic__

    ---

    Focus on your code and get amazing speedups

    [:octicons-arrow-right-24: Reference](/advanced/parallel.md)

-   :material-speedometer:{ .lg .middle } __Made to scale__

    ---

    Parallelism and Multithreading

    [:octicons-arrow-right-24: Read More](advanced/parallel.md)

-   :material-scale-balance:{ .lg .middle } __Open Source, Apache 2.0__

    ---

    Material for MkDocs is licensed under Apache 2.0  and available on [GitHub]

    [:octicons-arrow-right-24: License](#)

</div>