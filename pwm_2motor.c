#include <msp430.h>

void set_pwm (int Motor ,int PWM)
{
    switch (Motor)
    {
        case 1:
            if(PWM > 0)
            {
                TA0CCR1 = PWM;
                TA0CCR2 = 0;
            }
            else
            {
                TA0CCR1 = 0;
                TA0CCR2 = -PWM;
            }
            break;

        case 2:
            if(PWM > 0)
            {
                TA0CCR3 = 0;
                TA0CCR4 = PWM;
            }
            else
            {
                TA0CCR3 = -PWM;
                TA0CCR4 = 0;
            }
            break;

        default:
            TA0CCR1 = 0;
            TA0CCR2 = 0;
            TA0CCR1 = 0;
            TA0CCR2 = 0;
            break;
    }
}

void PWM_Init(void)
{
    P1DIR |= BIT2 + BIT3 + BIT4 + BIT5;    //设置P1.2/3/4/5输出
    P1SEL |= BIT2 + BIT3 + BIT4 + BIT5;    //SEL用于启用IO口特殊功能，BIT2/3/4/5对应CCR1/2/3/4
    TA0CCR0 = 500 ;                        //设置为500，为约1MHz / 500 = 2KHz的PWM
    TA0CTL |= TASSEL_2 + MC_1 + TACLR;     //时钟为SMCLK；增计数；清0

    //设置PWM的输出模式为模式7(reset/set)
    TA0CCTL1 |= OUTMOD_7;
    TA0CCTL2 |= OUTMOD_7;
    TA0CCTL3 |= OUTMOD_7;
    TA0CCTL4 |= OUTMOD_7;
}

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;

    PWM_Init();

    int i;

    while(1)//test：呼吸灯
    {
        for(i=0; i <= 400 ; i++)
        {
            set_pwm(1,i);                        //PWM参数设在0-500; PWM/500即占空比
            __delay_cycles(2000);
        }
        for(i=400; i >= 0 ; i--)
        {
            set_pwm(1,i);                        //PWM参数设在0-500; PWM/500即占空比
            __delay_cycles(2000);
        }

    }
}



