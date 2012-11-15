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
#define ITR 1
volatile unsigned long long stsc;
volatile int done = 0;
FILE *irqbeforef = NULL;
unsigned long long timer_arr[ITR];
unsigned long long irq_arr[ITR];

void *
timer_thd(void *data)
{
  char irqbuf[]  = "cat /proc/interrupts | grep Local | awk '{ print $2+$3+$4+$5+$6+$7+$8+$9; }'";
  struct timespec timm;

  timm.tv_sec = 0;
  timm.tv_nsec = 500000000L;

  while(1) {
    irqbeforef = popen(irqbuf, "r");
    rdtscll(stsc);
    nanosleep(&timm, (struct timespec *)NULL);
    /*    
    if(irqbeforef == NULL)
      printf("before is null\n");
    else
      printf("before is NOT null\n");
    */
    if(done) {
      break;
    }
  }
  pthread_exit(NULL);
}

void *
get_irqs(void *data)
{
  int i = ITR, j = 0;
  unsigned long long endtsc;
  char cycbuf[100];
  char irqbuf[]  = "cat /proc/interrupts | grep Local | awk '{ print $2+$3+$4+$5+$6+$7+$8+$9; }'";
  FILE *irqafterf = NULL;
  char irqafter[100], irqbefore[100];

  while(i > 0) {
    irqafterf = popen(irqbuf, "r");
    if(irqafterf == NULL)
      printf("it's null\n");
    rdtscll(endtsc);

    printf("1\n");
    timer_arr[j] = endtsc - stsc;
    printf("2\n");
    
    if(irqafterf == NULL || irqbeforef == NULL) {
      sleep(10);
      continue;
    }

    if(fgets(irqafter, 30, irqafterf) == NULL) {
      perror("fgets irqafterf: ");
      exit(-1);
    }
    //printf("3\n");
    if(fgets(irqbefore, 30, irqbeforef) == NULL) {
      perror("fgets irqbeforef: ");
      exit(-1);
    }
    //printf("4\n");
    irq_arr[j] = 0;//atoi(irqafter) - atoi(irqbefore);
    
    printf("Iteration %d: ccyl(%llu) tirq(%llu)\n", j, timer_arr[j], irq_arr[j]);

    pclose(irqafterf);
    pclose(irqbeforef);
  
    i--;
    j++;
  }
  done = 1;
  pthread_exit(NULL);
}

int 
main(int argc, char *argv[])
{
  // thread stuff
  pthread_t tid_timer, tid_irq;
  struct sched_param sp_timer, sp_irq;
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
  
  // Set up the timer and create a thread for it
  sp_timer.sched_priority = (sched_get_priority_max(SCHED_RR) - 1);
  if(pthread_create(&tid_timer, NULL, timer_thd, NULL) != 0) {
    perror("pthread create timer: ");
    return -1;
  }
  
  if(pthread_setschedparam(tid_timer, SCHED_RR, &sp_timer) != 0) {
    perror("pthread setsched timer: ");
    return -1;
  }
  printf("timer priority: (%d)\n", sp_timer.sched_priority);

  // Set up processor affinity for both threads
  CPU_ZERO(&mask);
  CPU_SET(0, &mask);
  if(pthread_setaffinity_np(tid_timer, sizeof(mask), &mask ) == -1 ) {
    perror("setaffinity timer error: ");
    return -1;
  }
  printf("Set affinity for timer thread\n");

  CPU_ZERO(&mask);
  CPU_SET(0, &mask);
  if(pthread_setaffinity_np(tid_irq, sizeof(mask), &mask ) == -1 ) {
    perror("setaffinity irq error: ");
    return -1;
  }
  printf("Set affinity for irq thread\n");

  pthread_join(tid_timer, &thd_ret);
  pthread_join(tid_irq, &thd_ret);

  return 0;
}
