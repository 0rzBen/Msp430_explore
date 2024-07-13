#ifndef __UART_H
#define __UART_H
 
#include <msp430.h>

void Uart_Init(void);
void senfchar(char s);
void sendstring(unsigned char *p);

#endif 
