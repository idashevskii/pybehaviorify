Originally based on [behavior3/behavior3py](https://github.com/behavior3/behavior3py) (MIT license)

## Installation

Install using pip from GitHub:

```bash
pip install git+https://github.com/idashevskii/pybehaviorify.git
```

## Main features

- Based on the work of [(Marzinotto et al., 2014)](http://www.csc.kth.se/~miccol/Michele_Colledanchise/Publications_files/2013_ICRA_mcko.pdf), in which they propose a **formal**, **consistent** and **general** definition of Behavior Trees;

- **Optimized to control multiple agents**: you can use a single behavior tree instance to handle hundreds of agents;

- Several **composite, decorator and action nodes** available within the library. You still can define your own nodes, including composites and decorators;

- **Completely free**, the core module and the visual editor are all published under the MIT License, which means that you can use them for your open source and commercial projects;

- **Lightweight**!

## What was changed?

- **Async**. Now all ticks are asynchronous.
- **Typing**. Almost full coverage.
- **Python 3 support**. Yep, including tests.
