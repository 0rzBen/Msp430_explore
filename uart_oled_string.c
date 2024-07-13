
#include <msp430.h>
#include <OLED.h>


#define BUFFER_SIZE 128
u8 buffer[BUFFER_SIZE];
u8 buffer_index = 0;


volatile unsigned int i;


void senfchar(char s)
{
    UCA0TXBUF=s;
    while(!(UCA0IFG & UCTXIFG));
}

void sendstring(unsigned char *p)
{
    while(*p!='\0')
    {
        while(!(UCA0IFG & UCTXIFG));
        UCA0TXBUF=*p++;

    }
}
void delay()
{
    for(i=50000;i>0;i--);
}


int main(void)
{

    WDTCTL = WDTPW + WDTHOLD;                 // Stop WDT

    OLED_Init();
    OLED_Clear();

    P3SEL = BIT3+BIT4;                        // P3.3,4 = USCI_A0 TXD/RXD
    UCA0CTL1 |= UCSWRST;                      // **Put state machine in reset**
    UCA0CTL1 |= UCSSEL_2;                     // SMCLK
    UCA0BR0 = 6;                              // 1MHz 9600 (see User's Guide)
    UCA0BR1 = 0;                              // 1MHz 9600
    UCA0MCTL = UCBRS_0 + UCBRF_13 + UCOS16;   // Modln UCBRSx=0, UCBRFx=0,
                                            // over sampling
    UCA0CTL1 &= ~UCSWRST;                     // **Initialize USCI state machine**
    UCA0IE |= UCRXIE;                         // Enable USCI_A0 RX interrupt
    sendstring("hello world\r\n");
    _EINT();
//  __bis_SR_register(LPM0_bits + GIE);       // Enter LPM0, interrupts enabled
//  __no_operation();                         // For debugger


    while(1)
    {
        sendstring("hello world\r\n");
        delay();

    }

}


#pragma vector=USCI_A0_VECTOR
__interrupt void USCI_A0_ISR(void)
{
    switch(__even_in_range(UCA0IV,4))
    {
        case 0:break;                             // Vector 0 - no interrupt
        case 2:                                   // Vector 2 - RXIFG
            //while (!(UCA0IFG & UCTXIFG));       // Echo back RXed character, confirm TX buffer is ready first
            //UCA0TXBUF = UCA0RXBUF;


            buffer[buffer_index] = UCA0RXBUF; // 读取接收的数据
            buffer_index++;

            if (buffer[buffer_index-1] == '$') // '$' 标志结束
            {
                buffer[buffer_index-1] = '\0';
                
                OLED_Clear();
                OLED_ShowString(0, 4, buffer, 8); // 显示接收到的数据

                buffer_index = 0; // 重置缓冲区索引
            }


            break;
        case 4:break;                             // Vector 4 - TXIFG
        default: break;
    }
}




