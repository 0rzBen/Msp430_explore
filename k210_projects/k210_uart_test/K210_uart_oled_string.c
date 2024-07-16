
#include <msp430.h>
#include <OLED.h>
#include <UART.h>

#define BUFFER_SIZE 128
u8 buffer[BUFFER_SIZE];
u8 buffer_index = 0;



volatile unsigned int i;


void delay()
{
    for(i=50000;i>0;i--);
}


int main(void)
{

    WDTCTL = WDTPW + WDTHOLD;                 // Stop WDT
    Uart_Init();
    OLED_Init();
    OLED_Clear();



    sendstring("hello world\r\n");

//  __bis_SR_register(LPM0_bits + GIE);       // Enter LPM0, interrupts enabled
//  __no_operation();                         // For debugger

    OLED_ShowString(0, 0, "Noooo", 8);

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

            //if (UCA0RXBUF == '@') buffer_index = 0;
            buffer[buffer_index] = UCA0RXBUF; // 读取接收的数据
            buffer_index++;

            //OLED_ShowChar(0, 2, UCA0RXBUF, 8); // 显示接收到的数据

            if (buffer[buffer_index-1] == '$') // '$' 标志结束
            {
                buffer[buffer_index-1] = '\0';

                //OLED_Clear();
                OLED_ShowString(0, 4, buffer, 8); // 显示接收到的数据


                buffer_index = 0; // 重置缓冲区索引
            }


            break;
        case 4:break;                             // Vector 4 - TXIFG
        default: break;
    }
}




