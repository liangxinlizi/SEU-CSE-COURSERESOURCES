# 操作系统选做实验报告——lottery
09022107 梁耀欣
## 实验目的
1. 进一步了解内核xv6
2. 熟悉调度程序
3. 将该调度程序改为lottery调度算法
4. 制作图表展示调度程序结果

## 实验内容
- 添加两个系统调用

添加两个系统调用，分别是设置票证数量（settickets）和获取进程信息（getpinfo）。在settickets中可以设置调用进程的票数，在默认情况下让每个进程获得一张票数，调用settickets可以让进程获得更多的票数（成功返回0，失败返回-1，传入的数字小于1也会返回-1）。在getpinfo中可以获取调用进程的pid、tickets数量、剩余时间、状态等信息。

- 增加一些结构和头文件

按照要求添加结构pstat，用来存储进程的状态，包括是否正在使用（inuse），拥有得票数（tickets），进程ID（pid），累计时钟周期数目（ticks），直接将readme中给出的代码粘贴到头文件中。除此之外，产生随机彩票数目的时候需要调用随机数种子，需要添加随机数的头文件。

- 修改schedule函数

修改proc.c中的函数，最主要的是schedule，修改为lottery调度算法。lottery调度算法是一种随机调度算法，其基本思想是：每次获取所有进程的彩票数目之和，生成一个随机数，运行这个随机数对应的进程。

- 在qemu中编译程序并记录数据

在xv6目录下执行make qemu，启动qemu，在shell中运行tester程序，记录程序运行结果。将运行结果粘贴到图标中。

## 实验代码

首先添加系统调用，和必做实验相似，在usys.S中添加系统调用号，在syscall.c中添加系统调用函数，在syscall.h中添加系统调用号，在sysproc.c中添加系统调用处理函数。

/user.h
```c
int settickets(int);
int getpinfo(struct pstat*);
```

/usys.S
```
SYSCALL(settickets)
SYSCALL(getpinfo)
```

/syscall.c
```c
extern int sys_settickets(void);
extern int sys_getpinfo(void);
```
```
[SYS_settickets]  sys_settickets,
[SYS_getpinfo]  sys_getpinfo,
```

/syscall.h
```c
#define SYS_settickets 22
#define SYS_getpinfo 23
```

在sysproc.c中添加系统调用处理函数：

/sysproc.c
```c
// 系统调用：设置进程的彩票数量
int sys_settickets(void) {
  int tickets_num;
  // 从用户空间获取参数：彩票数量
  if (argint(0, &tickets_num) < 0)
    return -1;
  // 确保彩票数量为正数
  if (tickets_num <= 0)
    return -1;
  acquire(&ptable.lock);
  // 设置当前进程的彩票数量
  myproc()->tickets=tickets_num;
  release(&ptable.lock);
  cprintf("Process %d set tickets to %d\n", myproc()->pid, tickets_num);
  return 0;
}

// 系统调用：获取进程信息
int sys_getpinfo(void) {
  struct pstat *curproc;
  // 从用户空间获取参数：目标结构体指针
  if (argptr(0, (void*)&curproc, sizeof(*curproc)) < 0)
    return -1;
  if (!curproc)
    return -1;
  struct proc *p;
  acquire(&ptable.lock);
  for (p = ptable.proc; p < &ptable.proc[NPROC]; ++p) {
    const int index = p - ptable.proc;
    if (p->state != UNUSED) {
      curproc->pid[index] = p->pid; // 进程ID
      curproc->ticks[index] = p->ticks; // 已运行时钟滴答数
      curproc->inuse[index] = p->state != UNUSED ? 1 : 0; // 进程是否正在使用
      curproc->tickets[index] = p->tickets; // 进程彩票数量
    }
  }
  release(&ptable.lock);
  return 0;
}
```
由于在运行过程中更改了spinlock的内容，我们用它来保护进程表，出现了bug的原因是源文件没有防止重定义，我们添加：

/spinlock.h
```c
#pramga once
```

/pstat.h
```c
#ifndef _PSTAT_H_
#define _PSTAT_H_
#include"param.h"

struct pstat{
    int inuse[NPROC];//每个进程是否在使用
    int tickets[NPROC];//彩票数量
    int pid[NPROC];
    int ticks[NPROC];//每个进程当累计CPU时间
};

#endif // _PSTAT_H_
```
学习一种生成随机数的算法并粘贴到rand函数中：

/rand.h
```c
#ifndef RAND_H
#define RAND_H

void srand(unsigned int seed);
int rand(void);

#endif /* RAND_H */
```

/rand.c
```c
#include "rand.h"

static unsigned long next = 1;

void srand(unsigned int seed) {
    next = seed;
}

int rand(void) {
    next = next * 1103515245 + 12345;
    return (unsigned int)(next/65536) % 32768;
}
```
proc文件就是操作系统管理进程的文件了，本实验主要要求更改的代码是创建代码即allocproc函数，调度代码即scheduler函数，创建子进程代码即fork函数，退出进程代码即exit函数。

/proc.h
```c
struct proc {
  uint sz;                     // Size of process memory (bytes)
  pde_t* pgdir;                // Page table
  char *kstack;                // Bottom of kernel stack for this process
  enum procstate state;        // Process state
  int pid;                     // Process ID
  struct proc *parent;         // Parent process
  struct trapframe *tf;        // Trap frame for current syscall
  struct context *context;     // swtch() here to run process
  void *chan;                  // If non-zero, sleeping on chan
  int killed;                  // If non-zero, have been killed
  struct file *ofile[NOFILE];  // Open files
  struct inode *cwd;           // Current directory
  char name[16];               // Process name (debugging)

  int inuse;
  int tickets;
  int ticks;
};

struct ptable_t
{
  struct spinlock lock;
  struct proc proc[NPROC];
};

extern struct ptable_t ptable;
```
修改最多的部分就是scheduler函数，主要实现内容是建立一个总票数（通过遍历可执行的进程票数并加和得到），然后随机生成一个数字（调用随机数生成函数），将这个数字与总票数比较，依次找到区间，让这个数字对应进程运行。

/proc.c
```c
struct ptable_t ptable={{0}};//将ptable结构体所有成员初始化为0
static struct proc *initproc;

int nextpid = 1;

...

int total_tickets;//存储所有进程的总票数
int lucky;//存储彩票数字

...

// 在allocproc函数增加：
 p->tickets=1;

// 在fork函数中增加：
struct proc *np; // np代表new process
struct proc *curproc = myproc();

np->tickets=curproc->tickets;

// 在exit函数中增加：
curproc->tickets=0;

// 在scheduler函数中修改为：
void
scheduler(void)
{
  struct proc *p;
  struct cpu *c = mycpu();
  c->proc = 0;//无运行指针

  srand(12345);
  
  for(;;){
    // Enable interrupts on this processor.
    sti();

  
    int total_ticks = 0;

    acquire(&ptable.lock);
    for(p = ptable.proc; p < &ptable.proc[NPROC]; ++p) {
      if(p->state == RUNNABLE) {
        total_tickets += p->tickets;
      }
      total_ticks += p->ticks;
    }
    
    lucky = rand() % (total_tickets + 1);
    total_tickets = 0;

    for(p = ptable.proc; p < &ptable.proc[NPROC]; ++p) {
      if(p->state != RUNNABLE) {
        continue;
      }
      total_tickets += p->tickets;
      if(total_tickets >= lucky) {
        if(total_ticks % 1000 <= 80) {
          cprintf("tick %d, pid %d, total_ticks %d \n", total_ticks, p->pid, p->ticks);
        }
        c->proc = p;
        switchuvm(p);
        p->state = RUNNING;

        p->inuse = 1;
        const int tickstart = ticks;
        swtch(&(c->scheduler), p->context);

        p->ticks += ticks - tickstart;//从启动到执行的时间长度

        switchkvm();
        c->proc = 0;
        break;
      } else {
        continue;
      }
    }
    release(&ptable.lock);
    }
}
```

最终写一个tester函数来测试我们添加的系统调用和调度算法：

/tester.c
```c
#include "types.h"
#include "stat.h"
#include "user.h"
#include "pstat.h"

// 打印进程信息
void print_pinfo(struct pstat *ps) {
    for (int i = 0; i < NPROC; i++) {
        if (ps->inuse[i]) {
            printf(1, "PID: %d, Tickets: %d, Ticks: %d\n", ps->pid[i], ps->tickets[i], ps->ticks[i]);
        }
    }
    printf(1, "\n");
}

int main(int argc, char* airgv[]) {
    // 设置主进程的彩票数为10
    //if (settickets(10) < 0) {
       // printf(1, "Error: settickets failed\n");
      //  exit();
    //}

    int tickets[] = {30,40, 50, 60, 70, 80, 90}; // 7个进程的彩票数

    // 创建八个子进程
    for (int i = 0; i < 7; i++) {
        int pid = fork();
        if (pid < 0) {
            printf(1, "Error: fork failed\n");
            exit();
        } else if (pid == 0) {
            // 子进程，设置彩票数并进入死循环
            if (settickets(tickets[i]) < 0) {
                printf(1, "Error: settickets failed\n");
                exit();
            }
            while (1);
        }
    }

    // 主进程每隔一段时间获取并打印进程信息
    struct pstat ps;
    for (int i = 0; i < 20; i++) {
        sleep(50); // 等待100个时钟周期
        if (getpinfo(&ps) < 0) {
            printf(1, "Error: getpinfo failed\n");
            exit();
        }
        printf(1, "Process Info at time %d:\n", i * 50);
        print_pinfo(&ps);
    }

    // 等待所有子进程结束
    for (int i = 0; i < 7; i++) {
        wait();
    }

    exit();
}
``` 

/makefile
```
UPROGS = tester
OBJS = rand.o
```

## 实验结果
在xv6目录下执行make qemu，启动qemu，在shell中运行tester程序，记录程序运行结果。
![alt text](<屏幕截图 2024-05-31 214752-1.png>)

可以看到，程序运行结果符合预期，子进程的票数和运行时间都被调度算法调度到合适的位置。
输出统计结果：
![alt text](<屏幕截图 2024-05-31 215156-1.png>)

可以看出在每个进程刚开始创建的时候初始化票数为1，然后我们在tester里创建几个子进程，分别赋予不同票数，然后主进程每隔一段时间获取进程信息，并打印进程信息。可以看到，进程分配的票数越多，运行时间越长，越可能被调度。

把彩票数目分别为30、60、90的进程结果存储到表格中：

| Time | PID 4 (Tickets: 30) | PID 7 (Tickets: 60) | PID 10 (Tickets: 90) |
|------|----------------------|----------------------|-----------------------|
| 50   | 113                  | 199                  | 238                   |
| 100  | 180                  | 345                  | 461                   |
| 150  | 239                  | 476                  | 645                   |
| 200  | 318                  | 658                  | 876                   |
| 250  | 380                  | 781                  | 1047                  |
| 300  | 430                  | 851                  | 1175                  |
| 350  | 525                  | 1051                 | 1500                  |
| 400  | 581                  | 1141                 | 1654                  |
| 450  | 618                  | 1226                 | 1772                  |
| 500  | 671                  | 1353                 | 1956                  |
| 550  | 765                  | 1547                 | 2224                  |
| 600  | 912                  | 1868                 | 2662                  |
| 650  | 1052                 | 2119                 | 3092                  |
| 700  | 1095                 | 2214                 | 3210                  |
| 750  | 1135                 | 2291                 | 3364                  |
| 800  | 1251                 | 2503                 | 3700                  |
| 850  | 1312                 | 2612                 | 3850                  |
| 900  | 1416                 | 2860                 | 4188                  |
| 950  | 1481                 | 2965                 | 4379                  |
