

#include <UART.h>


void Uart_Init(void)
{
	
  	P3SEL = BIT3+BIT4;                        // P3.4,5 = USCI_A0 TXD/RXD
  	UCA0CTL1 |= UCSWRST;                      // **Put state machine in reset**
  	UCA0CTL1 |= UCSSEL_2;                     // SMCLK
  	UCA0BR0 = 6;                              // 1MHz 9600 (see User's Guide)
  	UCA0BR1 = 0;                              // 1MHz 9600
  	UCA0MCTL = UCBRS_0 + UCBRF_13 + UCOS16;   // Modln UCBRSx=0, UCBRFx=0,
                                            // over sampling
  	UCA0CTL1 &= ~UCSWRST;                     // **Initialize USCI state machine**
  	UCA0IE |= UCRXIE;                         // Enable USCI_A0 RX interrupt
  	_EINT();
//  __bis_SR_register(LPM0_bits + GIE);       // Enter LPM0, interrupts enabled
//  __no_operation();                         // For debugger

}

void senfchar(char s)
{
    UCA0TXBUF=s;
    while(!(UCA0IFG&UCTXIFG));
}

void sendstring(unsigned char *p)
{
    while(*p!='\0')
    {
        while(!(UCA0IFG&UCTXIFG));
        UCA0TXBUF=*p++;

    }
}





