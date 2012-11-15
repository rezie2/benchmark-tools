#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h> 
#include <error.h>
#include <sched.h>

#include <sys/time.h>
#include <sys/resource.h>
#include <unistd.h>

#define rdtscll(val) \
  __asm__ __volatile__("rdtsc" : "=A" (val))
#define unlikely(x)     __builtin_expect(!!(x), 0)
#define ITR 500
#define THRESHOLD 10
unsigned long long irq_arr[ITR];
unsigned long long time_arr[ITR];

void *
get_irqs(void *data)
{
  int i = 0;
  unsigned long long tsc, endtsc, lastirq = 0, interirq;
  
  sleep(1);
  rdtscll(tsc);

  // while(i < ITR) {
  for(i = 0; i < ITR; i++) {
    rdtscll(endtsc);
    if((endtsc - tsc) > THRESHOLD) {
      if(unlikely(lastirq != 0)) {
	interirq = tsc - lastirq;
	irq_arr[i] = interirq;
      }
      lastirq = tsc;
      time_arr[i] = endtsc - tsc;
    }
    tsc = endtsc;
    //i++;
  }
  
  for(i = 0; i < ITR; i++) {
    printf("Iteration %d: Cycles Duration(%llu) Time Between Last Event(%llu)\n", i, time_arr[i], irq_arr[i]);
  }

  pthread_exit(NULL);
}

int 
main(int argc, char *argv[])
{
  // thread stuff
  pthread_t tid_irq;
  struct sched_param sp_irq;
  struct rlimit rl;
  cpu_set_t mask;
  void *thd_ret;

  rl.rlim_cur = RLIM_INFINITY;
  rl.rlim_max = RLIM_INFINITY;
  if(setrlimit(RLIMIT_CPU, &rl)) {
    perror("set rlimit: ");
    return -1;
  }
  printf("CPU limit removed\n");

  // Set up the irq logger and create a thread for it
  sp_irq.sched_priority = (sched_get_priority_max(SCHED_RR));
  if(pthread_create(&tid_irq, NULL, get_irqs, NULL) != 0) {
    perror("pthread create irq: ");
    return -1;
  }
  if(pthread_setschedparam(tid_irq, SCHED_RR, &sp_irq) != 0) {
      perror("pthread setsched irq: ");
      return -1;
  }
  printf("irq priority: (%d)\n", sp_irq.sched_priority);
  
  // Set up processor affinity for both threads
  CPU_ZERO(&mask);
  CPU_SET(0, &mask);
  if(pthread_setaffinity_np(tid_irq, sizeof(mask), &mask ) == -1 ) {
    perror("setaffinity irq error: ");
    return -1;
  }
  printf("Set affinity for irq thread\n");

  pthread_join(tid_irq, &thd_ret);

  return 0;
}
