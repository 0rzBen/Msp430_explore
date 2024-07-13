#include <msp430.h>

int count;
int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;
    P1DIR = BIT0;
    TA0CCTL0 = CCIE;                          // 使能; 默认CAP=0(即比较模式)
    TA0CTL = TASSEL_2 + MC_1 + TACLR;         // SMCLK(1048576 Hz), 增计数, 清除TAR（保证从0开始计数）
    TA0CCR0 = 52428;                          // 1048576 / 20 = 52428.8

    _EINT();

     while(1)
        __no_operation();
}

#pragma vector=TIMER0_A0_VECTOR
__interrupt void TIMER0_A0_ISR(void)
{
    
        count++;
        // version 1
  /*      if(count==20)
        {
            P1OUT |= BIT0;
        }
        if(count==40)
        {
            P1OUT &= ~BIT0;
            count = 0;
        }
  */
        //version 2
        if(count == 20)    //  大约1s反转一次
        {
            if(P1OUT & BIT0) P1OUT &= ~BIT0;
            else P1OUT |= BIT0;

            count = 0;
        }

}

